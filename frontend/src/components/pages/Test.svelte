<script lang="ts">
  import PlotDatasetSplitter from "../common/PlotDatasetSplitter.svelte"

  let seed = 0
  let trainPercentage = 0.8
</script>

<PlotDatasetSplitter {seed} {trainPercentage}/>

<style lang="scss">
</style>
