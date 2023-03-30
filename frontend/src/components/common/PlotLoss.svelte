<script lang="ts">
  import { onMount } from "svelte"
  import { default as vegaEmbed } from "vega-embed"
  import type { VisualizationSpec } from "vega-embed"
  import LossVisSpec from "../../data/LossVisSpec"
  import { createEventDispatcher } from "svelte"

  const dispatcher = createEventDispatcher()
  export let losses: number[] = undefined

  onMount(() => {
    if (losses === undefined) {
      return
    }
    // @ts-ignore
    LossVisSpec.data.values = losses.map((l, i) => ({ epoch: i + 1, loss: l }))
    // @ts-ignore
    LossVisSpec.signals = [{ name: "losses", value: losses }]
    vegaEmbed("#loss", LossVisSpec).then((result) => {
      dispatcher("plotLoaded", result.view)
    })
  })
</script>

<div id="loss" />

<style lang="scss">
  /* Your styling here */
</style>
