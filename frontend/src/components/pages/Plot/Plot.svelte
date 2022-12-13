<script lang="ts">
  import { onMount } from "svelte"
  import MiserablesData from "../../../data/MiserablesVisSpec"
  import VisSpec from "../../../data/VisSpec"
  import { default as vegaEmbed } from "vega-embed"
  import { networksList, selectedNetworkIndex } from "../../../stores"
  import { ModalData } from "../../../definitions/modalData"
  import { HoverData } from "../../../definitions/hoverData"
  import NodeDetailModal from "./NodeDetailModal.svelte"
  import { Link, Node } from "../../../definitions/network"
  import NetworkListItem from "../../common/NetworkListItem.svelte"
  import Hover from "./Hover.svelte"
  import statsIcon from "../../../assets/stats.svg"
  import { HoverType } from "../../../definitions/hoverType"

  function loadNetwork() {
    if ($networksList && $networksList.length > 0) {
      console.log("changing to ", $selectedNetworkIndex)
      VisSpec.data[0].values = $networksList[$selectedNetworkIndex].nodes
      VisSpec.data[1].values = $networksList[$selectedNetworkIndex].links
      createVegaEmbed(VisSpec)
    } else createVegaEmbed(MiserablesData)
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
          modalProps = item.datum
          modalData.isOpen = true
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

  // Run an onMount function to initialize the plot
  onMount(() => {
    // Anytime the networksList store value is updated, update the network
    loadNetwork()
  })

  let modalData: ModalData = new ModalData()
  let hoverData: HoverData = undefined

  // Anytime the selected network index from the menu changes, we need to update the vegaEmbed
  $: $selectedNetworkIndex, loadNetwork()

  // Props to pass to the modal anytime user clicks on a node from the vegaEmbed
  let modalProps: any = undefined

  // Anytime the user updates a node in the modal, update the network
  function updateNode(event: CustomEvent) {
    console.log("updating node", event.detail.newNode)
    let newNode: Node = event.detail.newNode
    networksList.update((networksList) => {
      networksList[$selectedNetworkIndex].nodes[newNode.index] = newNode
      return networksList
    })
    loadNetwork()
  }
</script>

<main>
  <!-- Define a left menu where each item is a NetworkListItem-->
  <div class="networks_list">
    <div class="networks_list_header">
      <p>Networks</p>
    </div>
    <div class="networks_list_items">
      {#each $networksList as network, index}
        <NetworkListItem
          {network}
          {index}
          selected={$selectedNetworkIndex == index}
          on:selectItem={(event) => {
            $selectedNetworkIndex = event.detail.selectedIndex
          }}
        />
      {/each}
    </div>
  </div>
  <div class="content">
    {#if $networksList.length == 0}
      <div class="no_networks">
        <h1>
          No networks to display. Displaying the default Miserables network 🥺
        </h1>
      </div>
    {:else}
      <div class="stats">
        <div class="stats_header">
          <img src={statsIcon} class="stats_icon" alt="Stats Icon" />
          <h3>Network Stats</h3>
        </div>
        <div class="stats_content">
          <p>Name: {$networksList[$selectedNetworkIndex].metadata.name}</p>
          <p>
            Description: {$networksList[$selectedNetworkIndex].metadata
              .description}
          </p>
          <p>Nodes: {$networksList[$selectedNetworkIndex].nodes.length}</p>
          <p>Edges: {$networksList[$selectedNetworkIndex].links.length}</p>
        </div>
      </div>
    {/if}

    <div id="viz" />
    {#if modalData.isOpen}
      <NodeDetailModal
        bind:open={modalData.isOpen}
        {modalProps}
        on:closeModal={() => (modalData.isOpen = false)}
        on:updateNode={updateNode}
      />
    {/if}
  </div>
  <Hover {hoverData} />
</main>

<style lang="scss">
  .content {
    border: 1px solid #e5e5e5;
    border-radius: 5px;
    background-color: white;
    margin-left: 20%;
    display: flex;
    flex-direction: column;
    align-items: center;
    right: 0;
    width: 50%;
    height: 20%;
  }
  .networks_list_header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }
  .networks_list {
    margin-top: 5.6%;
    overflow-y: scroll;
    overflow-x: hidden;
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 20%;
    background-color: #f5f5f5;
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
</style>
