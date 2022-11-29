<script lang="ts">
  import { createEventDispatcher } from "svelte"
  import type { Network } from "../../definitions/network"
  import networkIcon from "../../assets/network.svg"

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
</div>

<style lang="scss">
  .root {
    background-color: #f5f5f5;
    border-radius: 5px;
    padding: 10px;
    margin: 10px;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    margin: 10px;
    text-align: left;
    &.selected {
      background-color: #e5e5e5;
    }
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
</style>
