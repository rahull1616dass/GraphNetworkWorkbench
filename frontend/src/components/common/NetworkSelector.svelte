<script lang="ts">
import { networksList, selectedNetworkIndex } from "../../stores"

export let placeholderNetwork: string = "Select a network"
export let placeholderModel: string = "Select a model"
</script>

<div class="dropdown">

    <select class="selectNetwork">
        {#if placeholderNetwork}
        <option >{placeholderNetwork}</option>
        {/if}
        {#each $networksList as network, networkIndex}
            <option class="optionDropdown" value={networkIndex} on:click={() => {$selectedNetworkIndex = networkIndex
            console.log("Selected network index", $selectedNetworkIndex)
            }}>
                {network.metadata.name} ---
                Nodes: {network.nodes.length} , Edges: {network.links.length} 
            </option>
        {/each}
          
    </select>
    
    </div>

<style lang="scss">

.dropdown {
        position: flex;
        width: 50%;
        margin-left: 25%;
        margin-top: 1%;
        background-color: whitesmoke;
        border-radius: 15px;
        box-shadow: 1px 2px 3px rgba(0,0,0,0.1);
    }

.selectNetwork {
        width: 95%;
        height: 100%;
        font-family: var(font-family);
        font-size: 16px;
        font-weight: 800;
        color: var(--lightblack);
        background-color: white;
        padding: 1%;
        margin: 2%;
        cursor: pointer;
        border-radius: 10px;
        box-shadow: 2px 3px 4px rgba(0,0,0,0.2);
    }

</style>