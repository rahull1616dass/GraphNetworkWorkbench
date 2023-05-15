<script lang="ts">
  loadNetwork
  import { onMount } from "svelte"
  import MiserablesData from "../../../../data/MiserablesVisSpec"
  import VisSpec from "../../../../data/VisSpec"
  import { default as vegaEmbed } from "vega-embed"
  import {
    updateVisSpec,
    updateLinkDistance,
  } from "../../../../util/visSpecUtil"
  import {
    networksList,
    selectedNetworkIndex,
    maxNumberOfNodesForPlot,
  } from "../../../../stores"
  import { ModalData } from "../../../../definitions/modalData"
  import { HoverData } from "../../../../definitions/hoverData"
  import PlotDetailModal from "./PlotDetailModal.svelte"
  import { Link, Node } from "../../../../definitions/network"
  import Hover from "./Hover.svelte"
  import statsIcon from "../../../../assets/stats.svg"
  import { HoverType } from "../../../../definitions/hoverType"
  import { Toggle, Modal } from "carbon-components-svelte"
  import CustomButton from "../../../common/CustomButton.svelte"
  import { toCSVFile } from "../../../../util/networkParserUtil"
  import { uploadNetworkToStorage } from "../../../../api/firebase"
  import type { Network } from "../../../../definitions/network"
  import { UploadedFileType } from "../../../../definitions/uploadedFileType"
  import { ProgressBar } from "carbon-components-svelte"
  import { ProgressBarData } from "../../../../definitions/progressBarData"
  import { fade, slide, scale, fly } from "svelte/transition"

  //import JSON from "json-strictify"
  import cloneDeep from "lodash.clonedeep"
  import InfoBox from "../../../common/InfoBox.svelte"

  let infoBoxContent =
    "<p>View and customize the nodes and edges of the selected network. Enter edit mode to modify the node group and other properties, then save the changes and run experiments.</p>"
  $: isInfoModalOpen = false

  function loadNetwork(isItemUpdated: boolean) {
    if (isItemUpdated) {
      loadNetworkValues(currentNetwork, true)
    } else {
      // No item in the Plot is updated by the user, reload the plot without updating VisSpec
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

  function loadNetworkValues(network: Network, resetVegaId: boolean = false) {
    updateVisSpec(network, VisSpec, resetVegaId)
    createVegaEmbed(VisSpec)
  }
  function createVegaEmbed(embeddedNetwork: any) {
    vegaEmbed("#viz", embeddedNetwork, { actions: false })
      .then((result) => {
        viz = result.view

        result.view.addSignalListener("linkDistance", (value, val) => {
          console.log(parentWidth)
          if (
            parentWidth <
            (currentNetwork.nodes.length + val) * DYNAMIC_VEGA_CANVAS_CONSTANT
          ) {
            parentStyle = parentStyleFlexStart
          } else {
            parentStyle = parentStyleCentered
          }

          result.view.width(
            (currentNetwork.nodes.length + val) * DYNAMIC_VEGA_CANVAS_CONSTANT
          )
          result.view.height(
            (currentNetwork.nodes.length + val) * DYNAMIC_VEGA_CANVAS_CONSTANT
          )
        })

        result.view.addEventListener("click", function (_, item) {
          console.log("CLICK", item)
          if (!isEditMode) {
            editModeRequiredModalData.isOpen = true
            return
          }
          // @ts-ignore
          detailedItem = item.datum
          hoverData = undefined
          plotDetailModalData.isOpen = true
        })
        result.view.addEventListener("mouseover", function (event, item) {
          console.log("MOUSEOVER", item)
          const container = document.getElementById("viz")
          const containerRect = container.getBoundingClientRect()

          // console.log(window.)
          if (item != undefined && item.datum != undefined) {
            // @ts-ignore
            if (item != undefined && item.path != undefined) {
              // @ts-ignore
              console.log(item.datum)
              hoverData = new HoverData(
                HoverType.LINK,
                item.datum,
                undefined,
                // @ts-ignore
                event.pageX,
                // @ts-ignore
                event.pageY
              )
            } else {
              hoverData = new HoverData(
                HoverType.NODE,
                undefined,
                item.datum,
                // @ts-ignore
                event.pageX,
                // @ts-ignore
                event.pageY
              )
            }
          }
        })
        result.view.addEventListener("mouseout", function (_, item) {
          console.log("MOUSEOUT", item)
          hoverData = undefined
        })
        console.log(currentNetwork.links.length)
        
        // changing the size of the graph
        result.view.signal('linkDistance', Math.max(Math.min(currentNetwork.links.length/4, currentNetwork.nodes.length/2),15));
        // updateLinkDistance(VisSpec,currentNetwork.nodes.length)
        // viz.width((currentNetwork.links.length + 15) * dynamicVegaCanvasConstant);
        // viz.height((currentNetwork.links.length + 15) * dynamicVegaCanvasConstant);
      })
      .catch((error) => console.log(error))
  }

  async function updateNetworkInFirebaseStorage() {
    const nodeFile = toCSVFile(
      UploadedFileType.NODE_FILE,
      Object.keys(currentNetwork.nodes[0]),
      currentNetwork.nodes
    )
    const edgeFile = toCSVFile(
      UploadedFileType.EDGE_FILE,
      Object.keys(currentNetwork.links[0]),
      currentNetwork.links
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
    //currentNetwork = cloneDeep($networksList[$selectedNetworkIndex])
    isPlottable =
      $networksList[$selectedNetworkIndex].nodes.length <
      $maxNumberOfNodesForPlot

    // Anytime the networksList store value is updated, update the network
    if (isPlottable) loadNetwork(false)

    const parentElement = document.querySelector(`.${parentClass}`)
    parentWidth = parseInt(
      getComputedStyle(parentElement).getPropertyValue("width"),
      10
    )
    // vegaEmbed("#viz", VisSpec, { actions: false })
    //   .then((result) => {

    //   result.view.width((currentNetwork.nodes.length+startNodeDistance)*dynamicVegaCanvasConstant)
    //   result.view.height((currentNetwork.nodes.length+startNodeDistance)*dynamicVegaCanvasConstant)
    // })
  })

  let viz = undefined
  let currentNetwork: Network = undefined // Will be set in onMount()
  let plotDetailModalData: ModalData = new ModalData()
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
  You need to be in edit mode to edit nodes or edges. Please toggle the edit
  mode button. Then you can click on specific nodes or edges to edit their attributes.
  Once complete, click the save button to save your changes.
  `,
    false
  )
  let progressBarData: ProgressBarData = new ProgressBarData(
    false,
    "Updating the network..."
  )
  let hoverData: HoverData = undefined
  let detailedItem: object = undefined
  let isEditMode: boolean = false
  let isPlottable: boolean = true
  $: isPlottable = $networksList[0].nodes.length < $maxNumberOfNodesForPlot
  // Anytime the user updates a node or a link in the modal, update the network

  const DYNAMIC_VEGA_CANVAS_CONSTANT = 8
  const startNodeDistance = 15
  let parentStyle = `background: white; display: flex; flex-direction: column; align-items: center; flex-wrap: nowrap; justify-content: space-between;`
  const parentClass = "mainContent"
  let parentStyleCentered = `background: white; display: flex; flex-direction: column; align-items: center; flex-wrap: nowrap; justify-content: space-between;`
  let parentStyleFlexStart = `background: white; display: flex; flex-direction: column; align-items: flex-start; flex-wrap: nowrap; justify-content: space-between;`
  let parentWidth = 0

  function updateItem(event: CustomEvent) {
    let updatedItem: object = event.detail.updatedItem
    console.log("updating item", updatedItem)
    if (updatedItem.source != null) {
      currentNetwork.links.forEach((link, index) => {
        if (
          new Link(
            // @ts-ignore
            link.source.datum.name,
            // @ts-ignore
            link.target.datum.name,
            link.value
          ).equals(updatedItem as Link)
        ) {
          // @ts-ignore
          currentNetwork.links[index].value = updatedItem.value
        }
      })
    } else {
      currentNetwork.nodes[updatedItem.index] = updatedItem
    }
    loadNetwork(true)
  }

  let index: number = $selectedNetworkIndex
  let placeholder: string = "Please select a network from the list"
</script>

<div class="info">
  <InfoBox
    bind:isInfoModalOpen
    headerText="Network Visualization Guide"
    bodyText={infoBoxContent}
  />
</div>

<div
  class={parentClass}
  style={parentStyle}
  in:fly={{ y: -50, duration: 250, delay: 300 }}
>
  <div class="dropdown">
    <select
      class="select"
      bind:value={index}
      on:change={() => {
        $selectedNetworkIndex = index
        loadNetwork(false)
      }}
    >
      <option>{placeholder}</option>
      {#each $networksList as network, index}
        <option class="optionDropdown" value={index}>
          {network.metadata.name} --- Nodes: {network.nodes.length} , Edges: {network
            .links.length}
        </option>
      {/each}
    </select>
  </div>

  {#if currentNetwork != undefined}
    <div class="stats_content_container">
      <div class="stats">
        <details>
          <summary>
            <div class="stats_header">
              <img src={statsIcon} class="stats_icon" alt="Stats Icon" />
              <h5>Network Stats</h5>
            </div>
          </summary>
          <div class="stats_content">
            <p>Name: {currentNetwork.metadata.name}</p>
            <!-- <p>
	citation: {currentNetwork.metadata.}
  </p> -->
            <p>Nodes: {currentNetwork.nodes.length}</p>
            <p>Edges: {currentNetwork.links.length}</p>
            {#each Object.entries(currentNetwork.metadata) as [key, value]}
              <p>{key}: {value}</p>
            {/each}
          </div>
        </details>
      </div>
    </div>
  {/if}

  <div class="content">
    {#if currentNetwork === undefined}
      <div class="no_networks">
        <h1>
          No networks to display. Displaying the default Miserables network 🥺
        </h1>
      </div>
    {:else}
      {#if !isEditMode}
        <CustomButton
          type={"secondary"}
          fontsize={100}
          on:click={() => (isEditMode = true)}>Enter Edit Mode</CustomButton
        >
      {:else if progressBarData.isPresent}
        <ProgressBar helperText={progressBarData.text} />
      {:else}
        <CustomButton
          type={"secondary"}
          fontsize={100}
          on:click={async () => {
            isEditMode = false
            progressBarData.isPresent = true
            updateNetworkInFirebaseStorage()
          }}>Save Changes</CustomButton
        >
        <CustomButton
          type={"secondary"}
          fontsize={100}
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
    {/if}
  </div>

  {#if isPlottable}
    <div id="viz" style="background-color: white;" />
  {:else}
    {$networksList[$selectedNetworkIndex].metadata.name} is too large to be plotted,
    for performance reasons. Currently, it has {$networksList[
      $selectedNetworkIndex
    ].nodes.length} nodes and {$networksList[$selectedNetworkIndex].links
      .length} edges. The limit for plotting is set at {$maxNumberOfNodesForPlot}
  {/if}

  {#if plotDetailModalData.isOpen}
    <!--
    The assumption is that the names of the nodes will not change. Also it is not possible to
    add/remove nodes in the edit mode. For this, the user has to change the network itself via
    uploading a new nodes file.
      -->
    <PlotDetailModal
      bind:open={plotDetailModalData.isOpen}
      on:closeModal={() => (plotDetailModalData.isOpen = false)}
      {detailedItem}
      on:updateItem={updateItem}
    />
  {/if}

  {#if hoverData !== undefined}
    <Hover {hoverData} />
  {/if}
</div>

<style lang="scss">
  details {
    background-color: #f5f5f5;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    margin-bottom: 10px;
  }

  summary {
    list-style: none;
    cursor: pointer;
    outline: none;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stats_header {
    width: 100%;
  }

  .stats_summary {
    display: flex;
    justify-content: space-around;
    width: 100%;
    padding: 0.5rem;
  }

  .stats_content {
    padding: 0.5rem;
  }

  .select {
    width: 60%;
    height: 100%;
    font-family: var(font-family);
    font-size: 14px;
    font-weight: 400;
    background-color: white;
    padding: 1%;
    margin: 2%;
    cursor: pointer;
    border-radius: 1px;
    border-color: whitesmoke;
    box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.2);
  }
  .optionDropdown {
    font-family: var(font-family);
    font-size: 14px;
    font-weight: 500;
    color: var(--lightblack);
    background-color: white;
    cursor: pointer;
    cursor:hover {
      background-color: red;
    }
  }

  .content {
    padding-top: 10px;
    align-self: center;
  }
  .stats {
    padding-top: 10px;
    align-self: center;
  }

  .stats_header {
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: var(--wueblue);
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

  .dropdown {
    padding-top: 10px;
    align-self: center;
  }
  .selectDropdown {
    width: 95%;
    height: 100%;
    font-family: var(font-family);
    font-size: 16px;
    font-weight: 800;
    color: var(--lightblack);
    color-scheme: #4a4a56;
    background-color: white;
    padding: 1%;
    margin: 2%;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }
  .optionDropdown {
    font-family: var(font-family);
    font-size: 14px;
    font-weight: 500;
    color: var(--lightblack);
    color-scheme: #4a4a56;
    background-color: white;
    cursor: pointer;
    cursor:hover {
      background-color: red;
    }
  }
  hr {
    display: block;
    margin: 1em;
    width: 90%;
    content: "";
    margin-left: 5%;
    background-color: whitesmoke;
  }
</style>
