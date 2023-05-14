<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import DetailView from "./DetailView.svelte";
  import CustomButton from "./CustomButton.svelte";

  export let selectedRowIds;

  const dispatch = createEventDispatcher();
</script>

{#each selectedRowIds as rowId}
  <!-- <DetailView selectedRowId={rowId} />  -->
{/each}

<CustomButton type="secondary" inverse={true} on:click={() => dispatch("back")}
  >Back to Reports Page</CustomButton
>
