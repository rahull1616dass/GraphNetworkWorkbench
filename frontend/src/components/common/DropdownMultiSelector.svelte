<script lang="ts">
  import { MultiSelect } from "carbon-components-svelte"
  import { createEventDispatcher } from "svelte"

  export let items: string[] = []
  export let titleText: string = ""
  export let label: string = ""
  const dispatcher = createEventDispatcher()
</script>

<MultiSelect
  size="xl"
  {titleText}
  {label}
  items={items.map((item) => {
    return { id: item, text: item }
  })}
  on:select={(e) =>
    dispatcher("selectChanged", { selectedColumns: e.detail.selectedIds })}
/>

<style lang="scss">
</style>
