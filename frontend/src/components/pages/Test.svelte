<script lang="ts">
  import PlotDatasetSplitter from "../common/PlotDatasetSplitter.svelte"
  import PlotPrediction from "../common/PlotPrediction.svelte"
  import PlotLoss from "../common/PlotLoss.svelte"
  import DropdownMultiSelector from "../common/DropdownMultiSelector.svelte"
  import { networksList, selectedNetworkIndex } from "../../stores"
  import Countup from "svelte-countup"

  let seed = 0
  let trainPercentage = 0.8
  let columns: string[] = Object.keys($networksList[$selectedNetworkIndex].nodes[0])
  let selectedColumns: string[] = []

  let losses = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
</script>

<!--
<PlotDatasetSplitter {seed} {trainPercentage}/>

<PlotPrediction/>

<DropdownMultiSelector
  items={columns}
  on:selectChanged={(e) => {
    selectedColumns = e.detail.selectedColumns
    console.log(selectedColumns, " in test")
  }}
/>
--> 

<PlotLoss {losses}/>

<style lang="scss">
</style>
