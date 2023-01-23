<script lang="ts">
  loadNetwork
  import { onMount } from "svelte"
  import MiserablesData from "../../../../data/MiserablesVisSpec"
  import VisSpec from "../../../../data/VisSpec"
  import { default as vegaEmbed } from "vega-embed"
  import {
    networksList,
    selectedNetworkIndex,
    selectedMenuItem,
  } from "../../../../stores"
  import { ModalData } from "../../../../definitions/modalData"
  import { HoverData } from "../../../../definitions/hoverData"
  import NodeDetailModal from "./NodeDetailModal.svelte"
  import { Link, Node } from "../../../../definitions/network"
  import Hover from "./Hover.svelte"
  import statsIcon from "../../../../assets/stats.svg"
  import { HoverType } from "../../../../definitions/hoverType"
  import { MenuItem } from "../../../../definitions/menuItem"
  import { Toggle, Modal } from "carbon-components-svelte"
  import CustomModal from "../../../common/CustomModal.svelte"
  import CustomButton from "../../../common/CustomButton.svelte"
  import { toCSVFile } from "../../AddNetwork/UploadNetwork/networkParser"
  import { uploadNetworkToStorage } from "../../../../api/firebase"
  import type { Network } from "../../../../definitions/network"
  import { UploadedFileType } from "../../../../definitions/uploadedFileType"
  import UploadNetwork from "../../AddNetwork/UploadNetwork/UploadNetwork.svelte"
  import { ProgressBar } from "carbon-components-svelte"
  import { ProgressBarData } from "../../../../definitions/progressBarData"
  //import JSON from "json-strictify" 
  import cloneDeep from 'lodash.clonedeep'

  function loadNetwork(isNodeUpdate: boolean) {
    if (isNodeUpdate) {
      loadNetworkValues(currentNetwork)
    } else {
      if ($networksList && $networksList.length > 0) {
        console.log("changing to ", $selectedNetworkIndex)
        /*
        Note that structuredClone does not work on the svelte store.
        Same goes for JSON.stringify and JSON.parse which throws circular reference error.
        Hence the usage of lodash.clonedeep
        */
        currentNetwork = cloneDeep($networksList[$selectedNetworkIndex]) 
        loadNetworkValues(currentNetwork)
      } else createVegaEmbed(MiserablesData)
    }
  }

  function loadNetworkValues(network: Network) {
    VisSpec.data[0].values = network.nodes
    VisSpec.data[1].values = network.links
    createVegaEmbed(VisSpec)
  }

  function createNewVega() {
    const edges = [
      { source: "A", target: "B", weight: 1 },
      { source: "B", target: "C", weight: 2 },
      { source: "C", target: "D", weight: 3 },
      { source: "D", target: "E", weight: 4 },
      { source: "E", target: "F", weight: 5 },
    ]
    // Create a new Vega view and initialize it with the edge data.
    const view = {
      // Use the directed-edge mark type to draw the edges.
      mark: "directed-edge",

      // Map the edge weight attribute to the thickness of the edge line.
      encoding: {
        thickness: { field: "weight" },
      },

      // Use the edge data for the visual marks.
      data: { values: edges },
    }
    createVegaEmbed(view)
  }

  function createVegaEmbed(embeddedNetwork: any) {
    vegaEmbed("#viz", embeddedNetwork, { actions: false })
      .then((result) => {
        result.view.addEventListener("click", function (event, item) {
          console.log("CLICK", item)
          if (!isEditMode) {
            editModeRequiredModalData.isOpen = true
            return
          }
          detailedNode = new Node(
            item.datum.name,
            undefined,
            item.datum.group,
            item.datum.index,
            undefined
          )
          nodeDetailModalData.isOpen = true
        })
        result.view.addEventListener("mouseover", function (event, item) {
          console.log("MOUSEOVER", item)
          if (item != undefined && item.datum != undefined) {
            // @ts-ignore
            if (item != undefined && item.path != undefined) {
              // @ts-ignore
              console.log(item.path)
              hoverData = new HoverData(
                HoverType.LINK,
                new Link(
                  item.datum.source.datum.name,
                  item.datum.target.datum.name,
                  item.datum.value
                ),
                undefined,
                // @ts-ignore
                event.clientX,
                // @ts-ignore
                event.clientY
              )
            } else {
              hoverData = new HoverData(
                HoverType.NODE,
                undefined,
                new Node(
                  item.datum.name,
                  undefined,
                  item.datum.group,
                  item.datum.index,
                  undefined
                ),
                // @ts-ignore
                event.clientX,
                // @ts-ignore
                event.clientY
              )
            }
          }
        })
      })
      .catch((error) => console.log(error))
  }

  async function updateNetworkInFirebaseStorage() {
    const nodeFile = toCSVFile(
      UploadedFileType.NODE_FILE,
      Object.keys(new Node()),
      currentNetwork.nodes
    )
    const edgeFile = toCSVFile(
      UploadedFileType.EDGE_FILE,
      Object.keys(new Link()),
      currentNetwork.links.map((link) => {
        return {
          // @ts-ignore
          source: link.source.index,
          // @ts-ignore
          target: link.target.index,
          value: link.value,
        }
      })
    )
    await uploadNetworkToStorage(currentNetwork.metadata, nodeFile, edgeFile)
      .then(() => {
        console.log("Uploaded network to storage")
        $networksList[$selectedNetworkIndex] = currentNetwork
        loadNetwork(true)
        progressBarData.isPresent = false
      })
      .catch((error) => {
        progressBarData.isPresent = false
        console.log("Error uploading network to storage", error)
        uploadingNetworkErrorModalData.isOpen = true
      })
  }

  // Run an onMount function to initialize the plot
  onMount(() => {
    // Anytime the networksList store value is updated, update the network
    loadNetwork(false)
  })

  let currentNetwork: Network = undefined // Will be set in onMount()
  let nodeDetailModalData: ModalData = new ModalData()
  let uploadingNetworkErrorModalData: ModalData = new ModalData(
    undefined,
    "Error Uploading Network",
    `There was an error uploading the network to storage. Please try again. If the problem persists, please contact the developers.`,
    false
  )

  let editModeRequiredModalData: ModalData = new ModalData(
    undefined,
    "Edit Mode Required",
    `
  You need to be in edit mode to edit nodes. Please toggle the edit
  mode button. Then you can click on nodes to edit their attributes.
  Once complete, click the save button to save your changes.
  `,
    false
  )
  let progressBarData: ProgressBarData = new ProgressBarData(
    false,
    "Updating the network..."
  )
  let hoverData: HoverData = undefined
  let detailedNode: Node = undefined
  let isEditMode: boolean = false

  // Anytime the user updates a node in the modal, update the network
  function updateNode(event: CustomEvent) {
    console.log("updating node", event.detail.newNode)
    let newNode: Node = event.detail.newNode
    currentNetwork.nodes[newNode.index] = newNode
    loadNetwork(true)
  }
</script>

<main>
  <div class="content">
    {#if currentNetwork === undefined}
      <div class="no_networks">
        <h1>
          No networks to display. Displaying the default Miserables network 🥺
        </h1>
      </div>
    {:else}
      {#if !isEditMode}
        <CustomButton type={"secondary"} on:click={() => (isEditMode = true)}
          >Enter Edit Mode</CustomButton
        >
      {:else if progressBarData.isPresent}
        <ProgressBar helperText={progressBarData.text} />
      {:else}
        <CustomButton
          type={"secondary"}
          on:click={async () => {
            isEditMode = false
            progressBarData.isPresent = true
            updateNetworkInFirebaseStorage()
          }}>Save Changes</CustomButton
        >
        <CustomButton
          type={"secondary"}
          on:click={() => {
            isEditMode = false
            loadNetwork(false)
          }}>Discard</CustomButton
        >
      {/if}
      {#if editModeRequiredModalData.isOpen}
        <Modal
          passiveModal
          bind:open={editModeRequiredModalData.isOpen}
          modalHeading={editModeRequiredModalData.messageHeader}
          on:open
          on:close
        >
          <p>{editModeRequiredModalData.messageBody}</p>
        </Modal>
      {/if}
      <div class="stats">
        <div class="stats_header">
          <img src={statsIcon} class="stats_icon" alt="Stats Icon" />
          <h3>Network Stats</h3>
        </div>
        <div class="stats_content">
          <p>Name: {currentNetwork.metadata.name}</p>
          <p>
            Description: {currentNetwork.metadata.description}
          </p>
          <p>Nodes: {currentNetwork.nodes.length}</p>
          <p>Edges: {currentNetwork.links.length}</p>
        </div>
      </div>
    {/if}
  </div>
  <div id="viz" />
  {#if nodeDetailModalData.isOpen}
    <NodeDetailModal
      bind:open={nodeDetailModalData.isOpen}
      {detailedNode}
      on:closeModal={() => (nodeDetailModalData.isOpen = false)}
      on:updateNode={updateNode}
    />
  {/if}

  <Hover {hoverData} />
</main>

<style lang="scss">
  .content {
    /*border: 1px solid #e5e5e5;
    border-radius: 5px;*/
    background-color: white;
    //margin-left: 20%;
    margin: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    right: 0;
    width: 80%;
    height: 20%;
  }
  .stats {
    position: absolute;
    right: 10%;
    background-color: white;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }

  .stats_header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: burlywood;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }

  .stats_content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }

  .stats_icon {
    width: 1rem;
    height: 1rem;
  }
  .viz {
    width: 100%;
    height: 100%;
  }
</style>
