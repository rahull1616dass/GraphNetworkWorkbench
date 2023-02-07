<script lang="ts">
  import {
    networksList,
    selectedNetworkIndex,
    selectedMenuItem,
  } from "../../../stores"
  import NetworkListItem from "../../common/NetworkListItem.svelte"
  import { MenuItem } from "../../../definitions/menuItem"
  import CustomModal from "../../common/CustomModal.svelte"
  import CustomButton from "../../common/CustomButton.svelte"
  import { ModalData } from "../../../definitions/modalData"
  import { deleteNetwork } from "../../../api/firebase"
  import { ProgressBarData } from "../../../definitions/progressBarData"
  import { ProgressBar } from "carbon-components-svelte"

  $: selectNetwork()
  let tabchange
  let index = undefined
  let networkIndexToDelete = undefined
  let deleteNetworkProgressData = new ProgressBarData(false, "Deleting Network")
  let deleteModalData = new ModalData(
    undefined,
    "Delete Network",
    "Are you sure you want to delete this network?",
    false
  )
  let deleteResultModalData = new ModalData(
    undefined,
    "Delete Network",
    undefined,
    false
  )

  console.log("TAB CHANGE: ", tabchange)

  function selectNetwork() {
    if (tabchange === undefined) return
    $selectedMenuItem = MenuItem.PLOT
  }

  function onDeleteNetwork() {
    deleteNetwork($networksList[networkIndexToDelete].metadata.id)
      .then(() => {
        deleteNetworkProgressData.isPresent = false
        deleteModalData.isOpen = false
        deleteResultModalData.messageBody = `Network ${$networksList[networkIndexToDelete].metadata.name} 
        deleted successfully!`
        deleteResultModalData.isOpen = true
        $networksList = $networksList.filter(
          (_, i) => i !== networkIndexToDelete
        )
        networkIndexToDelete = undefined
      })
      .catch((error) => {
        deleteNetworkProgressData.isPresent = false
        deleteModalData.isOpen = false
        console.log(error)
        deleteResultModalData.messageBody = `Network ${$networksList[networkIndexToDelete].metadata.name} 
        could not be deleted!. Error: ${error}`
        deleteResultModalData.isOpen = true
      })
  }
</script>

<div class="explanation-title">
  <p>
    This page shows the networks list you uploaded. Please select a network from
    the list to visualize its nodes and edged and play with it!
  </p>
</div>

<div
  class="networks_list_items"
  style="--height: {$networksList.length * 120}px;"
>
  {#each $networksList as network, index}
    <NetworkListItem
      {network}
      {index}
      selected={$selectedNetworkIndex == index}
      on:selectItem={(event) => {
        $selectedNetworkIndex = event.detail.selectedIndex
        tabchange = event.detail.selectedIndex
      }}
      on:deleteItem={(event) => {
        networkIndexToDelete = event.detail.selectedIndex
        deleteModalData.isOpen = true
      }}
    />
  {/each}
</div>

{#if deleteModalData.isOpen}
  <CustomModal on:close={() => (deleteModalData.isOpen = false)}>
    <h4 slot="header">
      {deleteModalData.messageHeader}
    </h4>
    <div slot="body">
      {deleteModalData.messageBody}
    </div>

    <div slot="footer">
      {#if deleteNetworkProgressData.isPresent}
        <ProgressBar labelText={deleteNetworkProgressData.text} />
      {:else}
        <CustomButton
          type={"primary"}
          inverse={true}
          on:click={() => {
            deleteModalData.isOpen = false
          }}
        >
          No
        </CustomButton>

        <CustomButton
          type={"secondary"}
          inverse={false}
          on:click={() => {
            onDeleteNetwork()
          }}
        >
          Yes
        </CustomButton>
      {/if}
    </div>
  </CustomModal>
{/if}

{#if deleteResultModalData.isOpen}
  <CustomModal on:close={() => (deleteResultModalData.isOpen = false)}>
    <h4 slot="header">
      {deleteResultModalData.messageHeader}
    </h4>
    <div slot="body">
      {deleteResultModalData.messageBody}
    </div>

    <div slot="delete_modal">
      <CustomButton
        type={"primary"}
        inverse={true}
        on:click={() => {
          deleteResultModalData.isOpen = false
        }}
      >
        OK
      </CustomButton>
    </div>
  </CustomModal>
{/if}

<style lang="scss">
  .networks_list_items {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    overflow: auto;
  }

  p {
    font-size: 16px;
    font-weight: bold;
    color: var(--lightblack);
    margin-top: 2%;
  }
</style>
