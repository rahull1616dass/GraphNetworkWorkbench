<script lang="ts">
  import { DataTable } from "carbon-components-svelte"

  

</script>

<DataTable
  expandable
  headers={[
    { key: "name", value: "Name" },
    { key: "protocol", value: "Protocol" },
    { key: "port", value: "Port" },
    { key: "rule", value: "Rule" },
  ]}>


</DataTable>

<style lang="scss">
</style>
