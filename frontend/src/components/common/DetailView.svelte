<script>
  import { createEventDispatcher } from "svelte";
  import ExperimentResults from "./ExperimentResults.svelte";
  import CustomButton from "./CustomButton.svelte";

  const dispatch = createEventDispatcher();

  export let task;
  export let selectedNetworkIndex;

</script>

<CustomButton type="secondary" inverse={true} on:click={() => dispatch("back")}
  >Back to Reports Page</CustomButton
>

<ExperimentResults {task} currentNetwork={selectedNetworkIndex} />
