<!--
    An accordion that when opened, fetches its content from a URL.
-->
<script lang="ts">
  import { AccordionItem, Button, ProgressBar } from "carbon-components-svelte"
  import request from "../../api/request"
  import { createEventDispatcher } from "svelte"
  import { getAuth } from "firebase/auth"
  import { ProgressBarData } from "../../definitions/progressBarData"
  import { UploadResult } from "../../definitions/uploadResult"
  import { FetchableAccordionState } from "../../definitions/fetchableAccordionState"
  import { maxNodeLimit, networksList, paletteColors } from "../../stores"
  import JSZip from "jszip"
  import {
    parseNetwork,
    blobToFile,
    JSZipObjectToFile,
  } from "../../util/networkParserUtil"
  import { Node, Link, Metadata, Network } from "../../definitions/network"
  import {
    uploadNetworkToStorage,
    getNetworkFromStorage,
  } from "../../api/firebase"
  import MultipleNetworkPopup from "./MultipleNetworkPopup.svelte"
  import type ParseResult from "papaparse"
  import { FetchableNetwork } from "../../definitions/fetchableNetwork"
  import { UploadedFileType } from "../../definitions/uploadedFileType"
  // import fs from "fs"

  export let accordionTitle: string = undefined
  let fetchableNetwork: FetchableNetwork = new FetchableNetwork()
  $: fetchableNetwork.networkName = accordionTitle
  let state: FetchableAccordionState = FetchableAccordionState.ACCORDION_CLOSED
  let progressBarData: ProgressBarData = new ProgressBarData(
    true,
    "Fetching network details..."
  )
  const zip = new JSZip()

  function showPopup() {
    state = FetchableAccordionState.SHOW_MULTIPLE_NETWORK
  }

  function hidePopup() {
    state = FetchableAccordionState.HIDE_MULTIPLE_NETWORK
  }



  const onAccordionClick = async (event: MouseEvent) => {
    if (state === FetchableAccordionState.ACCORDION_CLOSED) {
      /*
      The assumption is that the id of a network imported this way will be equal to the name of the network.
      */
      if (
        $networksList.find(
          (network) => network.metadata.id === fetchableNetwork.getNetworkName()
        ) !== undefined
      ) {
        state = FetchableAccordionState.NETWORK_EXISTS
      } else fetchNetwork()
    } else state = FetchableAccordionState.ACCORDION_CLOSED
  }

  async function fetchNetwork() {
    state = FetchableAccordionState.FETCHING
    if (fetchableNetwork.content === undefined) {
      request(fetchableNetwork.getNetworkContentEndpoint())
        .then((response) => {
          state = FetchableAccordionState.FETCHED
          fetchableNetwork.content = response

          // @ts-ignore
          if (fetchableNetwork.content.nets.length > 1) {
            // Filter out the subnetworks that already exist in user's network list
            const currentNetworkIds: string[] = $networksList.map(
              (network) => network.metadata.id
            )
            // @ts-ignore
            fetchableNetwork.content.nets =
              fetchableNetwork.content.nets.filter(
                (subNetworkName) =>
                  !currentNetworkIds.includes(
                    `${fetchableNetwork.networkName}_${subNetworkName}}`
                  )
              )
            showPopup()
          }
          console.log(fetchableNetwork.content)
        })
        .catch((error) => {
          console.log(error)
          state = FetchableAccordionState.FETCH_ERROR
        })
    } else state = FetchableAccordionState.FETCHED // This network has alraedy been fetched and is stored in content
  }

  async function uploadNetwork() {
    state = FetchableAccordionState.UPLOADING
    progressBarData.text = "Downloading network from source..."
    fetch(fetchableNetwork.getDownloadEndpoint())
      .then((response) => response.blob())
      .then((blob) => {
        progressBarData.text = "Network downloaded. Parsing the network..."
        return JSZip().loadAsync(blob)
      })
      .then(async (zip) => {
        progressBarData.text = "Cleaning the parsed fields and uploading the network. This may take some time."
        let nodeFile: File = await JSZipObjectToFile(zip.files['nodes.csv'])
        let edgeFile: File = await JSZipObjectToFile(zip.files['edges.csv'])
        /*
        At this point, one can directly upload these files to the storage. However,
        we would like to clean the parsed fields before uploading the network to the storage.
        As such the following parsing is also necessary.
        */
        let network: Network = await filesToCleanedNetwork(nodeFile, edgeFile)
        if (network.nodes.length > $maxNodeLimit) {
          state = FetchableAccordionState.MAX_NODE_LIMIT_ERROR
          return
        }
        const files = network.toFiles()
        uploadNetworkToStorage(
          network.metadata,
          files.nodes,
          files.links
        )
          .then(() => {
            progressBarData.text =
              "Network uploaded to storage. Parsing the network..."
            getNetworkFromStorage(network.metadata)
              .then((network) => {
                $networksList = [...$networksList, network]
                state = FetchableAccordionState.UPLOADED
              })
              .catch((error) => {
                console.log(error)
                state = FetchableAccordionState.UPLOAD_ERROR
              })
          })
          .catch((error) => {
            console.log(error)
            state = FetchableAccordionState.UPLOAD_ERROR
          })
      }).catch((error) => {
        console.log(error)
        state = FetchableAccordionState.UPLOAD_ERROR
      })
  }

  async function filesToCleanedNetwork(nodeFile: File, edgeFile: File): Promise<Network>{
    return new Promise((resolve, reject) => {
    let network: Network = new Network(new Metadata(
          fetchableNetwork.getNetworkName(),
          fetchableNetwork.getNetworkName(),
          fetchableNetwork.content.description,
          $paletteColors[Math.floor(Math.random() * $paletteColors.length)]
        ))
    parseNetwork(nodeFile).then(parsedNodes =>{
      parseNetwork(edgeFile).then(parsedEdges => {
        network.nodes = parsedNodes.data
        network.links = parsedEdges.data
        resolve(network)
      }).catch(error => {
        reject(error)
      })
    }).catch(error => {
      reject(error)
    })
  })
}
</script>

<AccordionItem
  on:click={(e) => {
    onAccordionClick(e)
  }}
  bind:title={accordionTitle}
>
  {#if state === FetchableAccordionState.ACCORDION_CLOSED}
    closed
  {:else if state === FetchableAccordionState.FETCHING || state === FetchableAccordionState.UPLOADING}
    <div class="progress_bar">
      <ProgressBar helperText={progressBarData.text} />
    </div>
  {:else if state === FetchableAccordionState.FETCH_ERROR}
    Error fetching the network from the source.
  {:else if state === FetchableAccordionState.MAX_NODE_LIMIT_ERROR}
    Error uploading network to your list of networks. The network has more than {$maxNodeLimit} nodes, 
    which is the maximum allowed nodes in a given graph within our system.
  {:else if state === FetchableAccordionState.UPLOAD_ERROR}
    Error uploading network to your list of networks.
  {:else if state === FetchableAccordionState.NETWORK_EXISTS}
    <p>
      This network <i>probably</i> exists in your list of networks, given that
      you have a network with name {fetchableNetwork.getNetworkName()}. If you
      think that your network is different from this one you are trying to
      download, please delete the old one first.
    </p>
  {:else if state === FetchableAccordionState.FETCHED || state === FetchableAccordionState.UPLOADED || state == FetchableAccordionState.HIDE_MULTIPLE_NETWORK}
    <div class="content">
      <b>Title:</b>
      {fetchableNetwork.content.title} <br />
      <b>Description:</b>
      {fetchableNetwork.content.description} <br />
      <b>Nodes:</b>
      {fetchableNetwork.content.analyses.num_nodes} <br />
      <b>Edges:</b>
      {fetchableNetwork.content.analyses.num_edges} <br />
      <b>Is directed:</b>
      {fetchableNetwork.content.analyses.is_directed} <br />
      <b>Average Degree:</b>
      {fetchableNetwork.content.analyses.average_degree} <br />
    </div>
    {#if state === FetchableAccordionState.FETCHED || state == FetchableAccordionState.HIDE_MULTIPLE_NETWORK}
      <div class="import_button">
        <Button
          on:click={() => {
            uploadNetwork()
          }}
          size="small"
          on:click>Import Network</Button
        >
      </div>
    {:else if state === FetchableAccordionState.UPLOADED}
      <p>Upload complete</p>
    {/if}
  {/if}
</AccordionItem>
{#if state === FetchableAccordionState.SHOW_MULTIPLE_NETWORK}
  <MultipleNetworkPopup
    subNetworks={fetchableNetwork.content.nets}
    on:submit={(e) => {
      fetchableNetwork.subNetworkName = e.detail.selectedNetwork
      hidePopup()
      uploadNetwork()
    }}
    on:close={hidePopup}
  />
{/if}

<style lang="scss">
  .content {
    text-align: left;
    padding: 1rem;
  }

  .import_button {
    right: 0;
    margin: 1rem;
  }
</style>
