<button on:click="{() => dispatch('click')}" class="arrow-button">&lt;</button>
<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();
</script>
<style>
  .arrow-button {
    font-size: 2rem;
    background-color: transparent;
    border: none;
    cursor: pointer;
    padding: 0.5rem;
    color: var(--wueblue);
  }

  .arrow-button:hover {
    color: #ccc;
  }
</style>
