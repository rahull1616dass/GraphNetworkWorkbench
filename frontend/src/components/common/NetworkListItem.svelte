<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import type { Network } from "../../definitions/network";
  import networkIcon from "../../assets/network.svg";
  import deleteIcon from "../../assets/delete.svg";
  import ImageButton from "./ImageButton.svelte";

  const dispatch = createEventDispatcher();

  export let network: Network = undefined;
  export let index: number = undefined;
  export let selected: boolean = false;
</script>

<div
  on:click={() => dispatch("selectItem", { selectedIndex: index })}
  on:keydown={() => {}}
  class="root"
  class:selected
>
  <div class="network_color" style="--bg-color: {network.metadata.color}" />

  <ol class="content">
    <li class="network_name">
      {network.metadata.name}
    </li>
    <!-- <li class="network_description">
      {network.metadata.description}
    </li> -->
    <li class="network_details">
      <img src={networkIcon} class="network_icon" alt="Network Icon" />
      {network.nodes.length} nodes, {network.links.length} edges
    </li>
    <div class="delete">
      <ImageButton
        on:click={() => {
          dispatch("deleteItem", { selectedIndex: index });
        }}
        defaultImageSource={deleteIcon}
        styleClass="deleteButtonClass"
      />
    </div>
  </ol>
</div>

<style lang="scss">
  .root {
    display: flex;
    width: 80%;
    background-color: #f5f5f5;
    border-radius: 5px;
    padding: 10px;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    margin: 10px;
    &.selected {
      background-color: var(--wueblue);
      color: white;
    }
  }

  .delete {
    margin-left: 10%;
    // margin-left: auto;
    // margin-right: 10%;
    align-items: right;
    justify-self: right;
  }

  .content {
    display: flex;
    text-align: left;
    // flex-direction: row;
    // flex-wrap: nowrap;
    // justify-content: center;
    // align-items: center;
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
  div {
    //padding-right: 10px;
    align-content: center;
  }
</style>
