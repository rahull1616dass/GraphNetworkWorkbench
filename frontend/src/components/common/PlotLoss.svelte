<script lang="ts">
  import { onMount } from "svelte";
  import { default as vegaEmbed } from "vega-embed";
  import type { VisualizationSpec } from "vega-embed";
  import LossVisSpec from "../../data/LossVisSpec";
  import { createEventDispatcher } from "svelte";

  let id = `loss-${Math.random().toString(36).substring(2, 15)}`;

  const dispatcher = createEventDispatcher();
  export let losses: number[] = undefined;

  onMount(() => {
    if (losses === undefined) {
      return;
    }
    // @ts-ignore
    LossVisSpec.data.values = losses.map((l, i) => ({ epoch: i + 1, loss: l }));
    // @ts-ignore
    LossVisSpec.signals = [{ name: "losses", value: losses }];
    vegaEmbed("#" + id, LossVisSpec).then((result) => {
      dispatcher("plotLoaded", result.view);
    });
  });
</script>

<div {id} />
