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

  <div class="container">
    <ol class="content">
      <li class="network_name">
        {network.metadata.name}
      </li>

      <li class="network_details">
        <img src={networkIcon} class="network_icon" alt="Network Icon" />
        {network.nodes.length} nodes, {network.links.length} edges
      </li>

      
    </ol>

    <div class="delete">
      <ImageButton
        on:click={() => {
          dispatch("deleteItem", { selectedIndex: index });
        }}
        defaultImageSource={deleteIcon}
        styleClass="deleteButtonClass"
      />
    </div>
  </div>
  
</div>


<style lang="scss">
  .container {
  display: flex;
  align-items: flex-start;
}

.content {
  flex: 1;
}

.delete {
  position: sticky ;
  top: 0;
  right: 0;
}

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
