<script lang="ts">
  import PlotDatasetSplitter from "../common/PlotDatasetSplitter.svelte"
  import PlotPrediction from "../common/PlotPrediction.svelte"
  let seed = 0
  let trainPercentage = 0.8
</script>

<!--
<PlotDatasetSplitter {seed} {trainPercentage}/>
--> 
<PlotPrediction/>

<style lang="scss">
</style>
