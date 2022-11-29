<script lang="ts">
  import MiserablesData from "../../data/VisSpec"
  import SampleNetwork from "../../data/SampleNetwork"
  import { default as vegaEmbed } from "vega-embed"
  import { networksList } from "../../stores"
  import { ModalData } from "../../definitions/errorData"
  import NodeDetailModal from "./NodeDetailModal.svelte"
  import type { Node } from "../../definitions/network"
  import NetworkListItem  from "../common/NetworkListItem.svelte"
  let modalData: ModalData = new ModalData()

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

  // Anytime the networksList is updated, update the network
  if ($networksList && $networksList.length > 0) {
    /*
    Remove the default data from the Miserables Network that is stored in the url key
    data[0] = nodes, data[1] = links
    */
    SampleNetwork.data[0].values = $networksList[0].nodes
    SampleNetwork.data[1].values = $networksList[0].links
    vegaEmbed("#viz", SampleNetwork, { actions: false })
      .then((result) => {
        result.view.addEventListener("click", function (event, item) {
          console.log("CLICK", item)
          modalProps = item.datum
        })
      })
      .catch((error) => console.log(error))
  } else {
    // Refer https://www.koderhq.com/tutorial/svelte/json-storage/
    /*
    delete MiserablesData.data[0].url
    delete MiserablesData.data[1].url
    MiserablesData.data[0].values = $networksList[0].nodes
    MiserablesData.data[1].values = $networksList[0].links
     */

    vegaEmbed("#viz", MiserablesData, { actions: false }).catch((error) =>
      console.log(error)
    )
  }

  console.log("x")
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
      {#each $networksList as network}
        <NetworkListItem network={network} />
      {/each}
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
