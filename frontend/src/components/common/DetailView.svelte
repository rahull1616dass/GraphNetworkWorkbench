<script>
  export let task;
  export let selectedNetworkIndex;
  import { createEventDispatcher } from "svelte";
  import ExperimentResults from "./ExperimentResults.svelte";
  import CustomButton from "./CustomButton.svelte";
  const dispatch = createEventDispatcher();

  let forReport = false;
</script>

<CustomButton type="secondary" inverse={true} on:click={() => dispatch("back")}
  >Back to Reports Page</CustomButton
>

<ExperimentResults {task} currentNetwork={selectedNetworkIndex} />
