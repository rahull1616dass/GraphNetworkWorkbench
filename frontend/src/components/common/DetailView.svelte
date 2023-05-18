<script>
  import { createEventDispatcher } from "svelte";
  import ExperimentResults from "./ExperimentResults.svelte";
  import CustomButton from "./CustomButton.svelte";
  const dispatch = createEventDispatcher();

  export let task;
  let forReport = false;
</script>

<div class="arrow-button">
  <CustomButton
    type="secondary"
    inverse={true}
    on:click={() => dispatch("back")}>&lt;&lt;Back</CustomButton
  >
</div>
<ExperimentResults {task} forReport={true} />

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
</style>
