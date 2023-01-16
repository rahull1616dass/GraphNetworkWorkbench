<script lang="ts">
    import { networksList, selectedNetworkIndex, selectedMenuItem } from "../../../stores";
    import NetworkListItem from "../../common/NetworkListItem.svelte";
    import { MenuItem } from "../../../definitions/menuItem";

    $: selectNetwork()
    let tabchange
    let index = undefined

    console.log("TAB CHANGE: ", tabchange)

    function selectNetwork() {
      if (tabchange === undefined) return
      $selectedMenuItem = MenuItem.PLOT
    }

  </script>
  
  <div class="explanation-title"> 

    <p> This page shows the networks list you uploaded. Please select a network from the list to visualize its nodes and edged and play with it!</p>  
    
  </div>

    <div class="networks_list_items" style="--height: {$networksList.length * 120}px;">
      {#each $networksList as network, index}
        <NetworkListItem
          {network}
          {index}
          selected={$selectedNetworkIndex == index}
          on:selectItem={(event) => {
            $selectedNetworkIndex = event.detail.selectedIndex
            tabchange = event.detail.selectedIndex
          }}
        />
      {/each}
    </div>
  
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