<script lang="ts">
  import { onMount } from "svelte"
  import { default as vegaEmbed } from "vega-embed"
  import type { VisualizationSpec } from "vega-embed"
  import LossVisSpec from "../../data/LossVisSpec";

  export let loss: number[] = undefined

  onMount(() => {
    // @ts-ignore
    LossVisSpec.data.values = loss.map((l, i) => ({ epoch: i + 1, loss: l }))
    // @ts-ignore
    LossVisSpec.signals = [{ name: "loss", value: loss }]
    vegaEmbed("#embedding", LossVisSpec)
  })
</script>

<div id="embedding" />

<style lang="scss">
  /* Your styling here */
</style>
