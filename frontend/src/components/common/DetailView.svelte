<script>
  import { createEventDispatcher } from "svelte";
  import ExperimentResults from "./ExperimentResults.svelte";
  import CustomButton from "./CustomButton.svelte";

  const dispatch = createEventDispatcher();

  export let task;
  let forReport = false;
</script>

<CustomButton type="secondary" inverse={true} on:click={() => dispatch("back")}
  >Back to Reports Page</CustomButton
>

<ExperimentResults {task} forReport={true} />
