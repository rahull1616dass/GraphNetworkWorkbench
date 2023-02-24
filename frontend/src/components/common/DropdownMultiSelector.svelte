<script lang="ts">
  import { MultiSelect } from "carbon-components-svelte"
  import type {
    MultiSelectItem,
    MultiSelectItemId,
  } from "carbon-components-svelte/types/MultiSelect/MultiSelect.svelte"
  import { selectedNetworkIndex, networksList } from "../../stores"
  import { createEventDispatcher } from "svelte"

  export let items: string[] = []
  const dispatcher = createEventDispatcher()
</script>

<MultiSelect
  size="xl"
  titleText="Contact"
  label="Select contact methods..."
  items={items.map((item) => {
    return { id: item, text: item }
  })}
  on:select={(e) =>
    dispatcher("onSelectChanged", { selectedColumns: e.detail.selectedIds })}
/>

<style lang="scss">
</style>
