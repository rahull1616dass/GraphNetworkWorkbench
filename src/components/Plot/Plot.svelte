<script lang="ts">
  import { onMount } from "svelte"
  import MiserablesData from "../../data/VisSpec"
  import SampleNetwork from "../../data/SampleNetwork"
  import { default as vegaEmbed } from "vega-embed"
  import { networksList } from "../../stores"
  import { ModalData } from "../../definitions/errorData"
  import NodeDetailModal from "./NodeDetailModal.svelte"
  import type { Node } from "../../definitions/network"
  import NetworkListItem from "../common/NetworkListItem.svelte"

  function loadNetwork() {
    if ($networksList && $networksList.length > 0) {
      console.log("changing to ", selectedNetworkIndex)
      SampleNetwork.data[0].values = $networksList[selectedNetworkIndex].nodes
      SampleNetwork.data[1].values = $networksList[selectedNetworkIndex].links
      createVegaEmbed(SampleNetwork)
    } else createVegaEmbed(MiserablesData)
  }

  function createVegaEmbed(embeddedNetwork: any) {
    vegaEmbed("#viz", embeddedNetwork, { actions: false })
      .then((result) => {
        result.view.addEventListener("click", function (event, item) {
          console.log("CLICK", item)
          modalProps = item.datum
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

  let selectedNetworkIndex: number = 0
  // Anytime the selected network index from the menu changes, we need to update the vegaEmbed
  $: selectedNetworkIndex, loadNetwork()

  // Props to pass to the modal anytime user clicks on a node from the vegaEmbed
  let modalProps: any = undefined
  // Anytime the user clicks on a node, modalProps will be updated. This will trigger the modal to open
  $: modalProps, (modalData.isOpen = true)

  // Anytime the user updates a node in the modal, update the network
  let updatedNode: Node = undefined
  $: updatedNode,
    () => {
      console.log("Updated node: ", updatedNode)
      networksList.update((networks) => {
        networks[0].nodes[updatedNode.index] = updatedNode
        return networks
      })
    }
</script>

<main>
  {#if $networksList.length == 0}
    <div class="no_networks">
      <h1>
        No networks to display. Displaying the default Miserables network 🥺
      </h1>
    </div>
  {:else}
    <div class="networks" />
  {/if}

  <div id="viz" />
  {#if modalData.isOpen && modalProps != undefined}
    <NodeDetailModal
      bind:open={modalData.isOpen}
      bind:node={updatedNode}
      bind:modalProps
    />
  {/if}

  <!-- Define a right menu where each item is a NetworkListItem-->
  <div class="networks_list">
    <div class="networks_list_header">
      <p>Networks</p>
    </div>
    <div class="networks_list_items">
      {#each $networksList as network, index}
        <NetworkListItem
          {network}
          {index}
          selected={selectedNetworkIndex == index}
          on:selectItem={(event) => {
            selectedNetworkIndex = event.detail.selectedIndex
          }}
        />
      {/each}
    </div>
  </div>
</main>

<style>
  .networks_list_header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }
  .networks_list {
    margin-top: 5%;
    overflow-y: scroll;
    overflow-x: hidden;
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 150px;
    background-color: #f5f5f5;
  }
</style>
