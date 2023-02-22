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

  export let networkName: string
  let endpoint: string = undefined
  $: endpoint = `https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetowrkDescription?networkName=${networkName}`
  let content = undefined
  let state: FetchableAccordionState = FetchableAccordionState.ACCORDION_CLOSED

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
          console.log(content.description)
        })
        .catch((error) => {
          state = FetchableAccordionState.FETCH_ERROR
        })
    }
  }

  async function uploadNetwork(){
    fetch(
      `https://us-central1-graphlearningworkbench.cloudfunctions.net/downloadNetworkFile?networkName=${networkName}`
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
        ])
        let edgesString = alltext[0].replace("# ", "")
        let network = new Network(
          new Metadata(
            networkName,
            networkName,
            content.description,
            "",
          ),
          new Node(nodesString), // TODO: Parsing here
          new Link(edgesString)
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
  {:else if state === FetchableAccordionState.FETCHED || state === FetchableAccordionState.UPLOADED}
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
    {#if state === FetchableAccordionState.FETCHED}
      <div class="import_button">
        <Button
          on:click={() => {
            state = FetchableAccordionState.UPLOADING
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
