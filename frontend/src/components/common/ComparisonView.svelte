<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import DetailView from './DetailView.svelte'; 

    export let selectedRowIds;

    const dispatch = createEventDispatcher();
</script>
  
<p>Comparison view for rows:</p>
  
{#each selectedRowIds as rowId}
  <DetailView selectedRowId={rowId} /> 
{/each}
  
<button on:click={() => dispatch('back')}>Back to table</button>


  