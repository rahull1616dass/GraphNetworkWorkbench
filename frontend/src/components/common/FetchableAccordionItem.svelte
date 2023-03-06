<!--
    An accordion that when opened, fetches its content from a URL.
-->
<script lang="ts">
  import { AccordionItem, Button, ProgressBar } from "carbon-components-svelte"
  import request from "../../api/request"
  import { createEventDispatcher } from "svelte"
  import { getAuth } from "firebase/auth"
  import { networkExists, getExperimentTasks } from "../../api/firebase"
  import { ProgressBarData } from "../../definitions/progressBarData"
  import { UploadResult } from "../../definitions/uploadResult"
  import { FetchableAccordionState } from "../../definitions/fetchableAccordionState"
  import { networksList } from "../../stores"
  import JSZip from "jszip"
  import { removeCSVColumns } from "../../util/networkParserUtil"
  import { Node, Link, Metadata, Network } from "../../definitions/network"
  import { uploadNetworkToStorage } from "../../api/firebase"
  import MultipleNetworkPopup from "./MultipleNetworkPopup.svelte"

  export let networkName: string
  let subNetworkName: string
  let endpoint: string = undefined
  $: endpoint = `https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetworkDescription?networkName=${networkName}`
  let content = undefined
  let state: FetchableAccordionState = FetchableAccordionState.ACCORDION_CLOSED

  let multipleNetworks: string[]
  let existMultipleNetworks: boolean[] = []

  function showPopup() {
    state = FetchableAccordionState.SHOW_MULTIPLE_NETWORK
  }

  function hidePopup() {
    state = FetchableAccordionState.HIDE_MULTIPLE_NETWORK
  }

  const handlePopupSubmit = (event) => {
    // Do something with the result here
    console.log(event.detail);
    subNetworkName = event.detail;
    hidePopup()
    uploadNetwork()
  }


  const onAccordionClick = async (event: MouseEvent) => {
    if (state === FetchableAccordionState.ACCORDION_CLOSED) {
      /*
    The assumption is that the id of a network imported this way will be equal to the name of the network.
    */
      if (
        $networksList.find((network) => network.metadata.id === networkName) !==
        undefined
      ) {
        state = FetchableAccordionState.NETWORK_EXISTS
      } else fetchNetwork()
    } else state = FetchableAccordionState.ACCORDION_CLOSED
  }

  async function fetchNetwork() {
    state = FetchableAccordionState.FETCHING
    if (content === undefined) {
      console.log(endpoint)
      request(endpoint)
        .then((response) => {
          state = FetchableAccordionState.FETCHED
          content = response
          /*
        If there is more than one network in a given network content, then just take
        the first one to show the details of, and ignore the rest.
        */
          if (Object.keys(content.analyses).length > 1) {
            content.analyses =
              content.analyses[Object.keys(content.analyses)[0]]
          }
          if(content.nets.length>1){
            let flag: boolean
            flag = true;
            multipleNetworks = content.nets
            for(let key in multipleNetworks ){
              if ($networksList.find((network) => network.metadata.id === `${networkName}_${multipleNetworks[key]}`) !==
                  undefined) {
                    existMultipleNetworks.push(true)
                }
                else{
                  existMultipleNetworks.push(false)
                  flag = false
                }
            }
            if(flag == true)
            {
              state = FetchableAccordionState.NETWORK_EXISTS
            }
          }
          console.log(content.description)
        })
        .catch((error) => {
          console.log(error)
          state = FetchableAccordionState.FETCH_ERROR
        })
    }
    else
    {
      state = FetchableAccordionState.FETCHED
    }
  }
  function checkForSubnetwork(){
    if(multipleNetworks === undefined)
    {
      subNetworkName =networkName;
      uploadNetwork()
    }
    else if(multipleNetworks.length>1)
    {
      state = FetchableAccordionState.SHOW_MULTIPLE_NETWORK
    }
    else
    {
      subNetworkName =networkName;
      uploadNetwork()
    }
  }
  async function uploadNetwork(){
    
    state = FetchableAccordionState.UPLOADING
    console.log(`https://us-central1-graphlearningworkbench.cloudfunctions.net/downloadNetworkFile?networkName=${networkName}&netName=${subNetworkName}`)
    fetch(
      `https://us-central1-graphlearningworkbench.cloudfunctions.net/downloadNetworkFile?networkName=${networkName}&netName=${subNetworkName}`
    )
      .then((response) => response.blob())
      .then((blob) => {
        return JSZip.loadAsync(blob)
      })
      .then((zip) => {
        let edgeFile
        let nodeFile
        edgeFile = zip.files["edges.csv"].async("text")
        nodeFile = zip.files["nodes.csv"].async("text")
        return Promise.all([edgeFile, nodeFile])
      })
      .then((alltext) => {
        let nodesString = removeCSVColumns(alltext[1].replace("# ", ""), [
          " name",
          " _pos",
        ]).replace(", ",",").replace("label","name")
        let edgesString = alltext[0].replace("# ", "")
        console.log(nodesString)
        let network = new Network(
          new Metadata(
            networkName,
            networkName,
            content.description,
            "",
          ),
          <Node[]>(
            JSON.parse(nodesString)
          ),
          <Link[]>(
            JSON.parse(edgesString)
          )
        )
        const files = network.toFiles()
        uploadNetworkToStorage(network.metadata, files.nodes, files.links).then(() => {
          state = FetchableAccordionState.UPLOADED
        }).catch((error) => {
          state = FetchableAccordionState.UPLOAD_ERROR
        })
  })
}

</script>

<AccordionItem
  on:click={(e) => {
    onAccordionClick(e)
  }}
  bind:title={networkName}
>
  {#if state === FetchableAccordionState.ACCORDION_CLOSED}
    closed
  {:else if state === FetchableAccordionState.FETCHING}
    <div class="progress_bar">
      <ProgressBar helperText="Fetching network..." />
    </div>
  {:else if state === FetchableAccordionState.UPLOADING}
    <div class="progress_bar">
      <ProgressBar helperText="Uploading network to your list of networks..." />
    </div>
  {:else if state === FetchableAccordionState.FETCH_ERROR}
    Error fetching the network from the source.
  {:else if state === FetchableAccordionState.UPLOAD_ERROR}
    Error uploading network to your list of networks
  {:else if state === FetchableAccordionState.NETWORK_EXISTS}
    <p>
      This network <i>probably</i> exists in your list of networks, given that
      you have a network with name {networkName}. If you think that your network
      is different from this one you are trying to download, please delete the
      old one first.
    </p>
  {:else if state === FetchableAccordionState.FETCHED || state === FetchableAccordionState.UPLOADED || state == FetchableAccordionState.HIDE_MULTIPLE_NETWORK}
    <div class="content">
      <b>Title:</b>
      {content.title} <br />
      <b>Description:</b>
      {content.description} <br />
      <b>Nodes:</b>
      {content.analyses.num_nodes} <br />
      <b>Edges:</b>
      {content.analyses.num_edges} <br />
      <b>Is directed:</b>
      {content.analyses.is_directed} <br />
      <b>Average Degree:</b>
      {content.analyses.average_degree} <br />
    </div>
    {#if state === FetchableAccordionState.FETCHED|| state == FetchableAccordionState.HIDE_MULTIPLE_NETWORK}
      <div class="import_button">
        <Button
          on:click={() => {
            checkForSubnetwork()
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
    <MultipleNetworkPopup {multipleNetworks} {existMultipleNetworks} on:submit={handlePopupSubmit} on:close={hidePopup}/>
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
