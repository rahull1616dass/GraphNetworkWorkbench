<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import type { Network } from "../../definitions/network"
  import networkIcon from "../../assets/network.svg"
  import deleteIcon from "../../assets/delete.svg"
  import ImageButton from "./ImageButton.svelte"

  const dispatch = createEventDispatcher()

  export let network: Network = undefined
  export let index: number = undefined
  export let selected: boolean = false


</script>

<div
  on:click={() => dispatch("selectItem", { selectedIndex: index })}
  on:keydown={() => {}}
  class="root"
  class:selected
>
  <div class="network_color" style="--bg-color: {network.metadata.color}">

  </div>
  <div class="content">
    <div class="network_name">
      {network.metadata.name}
    </div>
    <div class="network_description">
      {network.metadata.description}
    </div>
    <div class="network_details">
      <img src={networkIcon} class="network_icon" alt="Network Icon" />
      {network.nodes.length} nodes, {network.links.length} edges
    </div>
  <div class="delete">
    <ImageButton on:click={() => {
      dispatch("deleteItem", { selectedIndex: index })
    }} defaultImageSource={deleteIcon} styleClass = "deleteButtonClass"/>
  </div>
  </div>
</div>

<style lang="scss">
  .root {
    display: flex;
    border-radius: 5px;
    padding: 10px;
    cursor: pointer;
    margin: 10px;
    &.selected {
      background-color: var(--wueblue);
      color: white;
    }
  }

  .delete{
    margin-left: auto;
    margin-right: 10px;
  }
  
  .content{
    display: flex;
    text-align: left;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: center;
    align-items: center;
  }
  .network_color {
    width: 10px;
    height: 50px;
    background-color: var(--bg-color);
    margin-right: 10px;
  }
  .network_details {
    font-size: 0.8rem;
    display: flex;
    flex-direction: row;
    align-items: center;
  }
  .network_icon {
    width: 1.5rem;
    height: 1.5rem;
  }
  div{
    padding-right: 10px;
  }
</style>
