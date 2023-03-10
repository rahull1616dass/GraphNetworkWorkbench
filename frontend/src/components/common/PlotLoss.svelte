<script lang="ts">
  import { onMount } from "svelte"
  import { default as vegaEmbed } from "vega-embed"
  import type { VisualizationSpec } from "vega-embed"
  import LossVisSpec from "../../data/LossVisSpec";

  export let losses: number[] = undefined

  onMount(() => {
    // @ts-ignore
    LossVisSpec.data.values = losses.map((l, i) => ({ epoch: i + 1, loss: l }))
    // @ts-ignore
    LossVisSpec.signals = [{ name: "losses", value: losses }]
    vegaEmbed("#embedding", LossVisSpec)
  })
</script>

<div id="embedding" />

<style lang="scss">
  /* Your styling here */
</style>
