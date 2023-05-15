<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import CustomButton from "./CustomButton.svelte";
  import ComparisonSingleView from "./ComparisonSingleView.svelte";

  const dispatch = createEventDispatcher();

  export let selectedRowIds
  export let tasks;
  export let currentNetwork;

</script>



<CustomButton type="secondary" on:click={() => dispatch("back")}
  >Back to Reports Page</CustomButton
>

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
  .comparison-container {
    display: grid;
    grid-template-columns: 1fr 1fr; /* Creates 2 equal-width columns */
    gap: 10px; /* Optional: Adds some space between the columns */
  }
</style>

