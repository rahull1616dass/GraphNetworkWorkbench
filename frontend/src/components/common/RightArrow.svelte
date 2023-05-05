<script lang="ts">
  import { createEventDispatcher } from "svelte";
  const dispatch = createEventDispatcher();
</script>

<button on:click={() => dispatch("click")} class="arrow-button">&gt;</button>

<style>
  .arrow-button {
    position: fixed;
    right: 15%;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1000;
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
