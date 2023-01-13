<script lang="ts">
  import { networksList, selectedNetworkIndex } from "../../../stores";

  export let index: number = undefined
  let placeholder: string = "Please select a network from the list"

  function selected (index) {
    if (typeof index !== "number") {
      return
    }
    $selectedNetworkIndex = index
  }
</script>


<div class="dropdown">

<select class="selectDropdown" bind:value={index} on:click={() => selected(index)}>
    {#if placeholder}
    <option >{placeholder}</option>
    {/if}
    {#each $networksList as network, index}
        <option class="optionDropdown" value={index}>
            {network.metadata.name} ---
            Nodes: {network.nodes.length} , Edges: {network.links.length} 
        </option>
    {/each}
      
</select>


</div>

<hr/>

<div>

</div>




<style lang="scss">
    .train_box {
        width: 100%;
        height: 100%;
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 10px;
        margin: 10px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        margin: 10px;
    }
    .dropdown {
        position: flex;
        width: 50%;
        background-color: whitesmoke;
        margin-left: 25%;
        margin-top: 1%;
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

    option:hover {
    background-color: yellow;
    }

    
</style>
