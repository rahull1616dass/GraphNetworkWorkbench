<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import CustomButton from "./CustomButton.svelte";
  import ComparisonSingleView from "./ComparisonSingleView.svelte";

  const dispatch = createEventDispatcher();

  export let selectedRowIds
  export let tasks;
  export let currentNetwork;

</script>



<div  class="arrow-button">
  <CustomButton type="secondary" inverse={true} on:click={() => dispatch("back")}
    >&lt;&lt;Back</CustomButton
  >
  </div>

<div>

  <div class="comparison-container">
{#each selectedRowIds as id}
  {#each tasks as task}
    {#if task.id === id}
    
      <ComparisonSingleView {task} {currentNetwork} />
    
    {/if}
  {/each}
{/each}
</div>
</div>

<style>
  .arrow-button {
    position: flex;
    z-index: 1000;
    font-size: 1rem;
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    color: var(--wueblue);
  }

  .arrow-button:hover {
    color: #ccc;
  }
  .comparison-container {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Creates 2 equal-width columns */
    gap: 10px; /* Optional: Adds some space between the columns */
  }
</style>

