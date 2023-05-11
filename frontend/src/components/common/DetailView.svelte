<script>
    export let selectedRowId;
    import { createEventDispatcher } from 'svelte';
    const dispatch = createEventDispatcher();
  </script>
  
  <p>Detail view for row {selectedRowId}</p>
  
  <button on:click={() => dispatch('back')}>Back to table</button>
  