<script lang="ts">
  import PlotDatasetSplitter from "../common/PlotDatasetSplitter.svelte"
  import PlotPrediction from "../common/PlotPrediction.svelte"
  import DropdownMultiSelector from "../common/DropdownMultiSelector.svelte"
  import { networksList, selectedNetworkIndex } from "../../stores"

  let seed = 0
  let trainPercentage = 0.8
  let columns: string[] = Object.keys($networksList[$selectedNetworkIndex].nodes[0])
  let selectedColumns: string[] = []
</script>

<!--
<PlotDatasetSplitter {seed} {trainPercentage}/>

<PlotPrediction/>
--> 
<DropdownMultiSelector
  items={columns}
  on:selectChanged={(e) => {
    selectedColumns = e.detail.selectedColumns
    console.log(selectedColumns, " in test")
  }}
/>

<style lang="scss">
</style>
