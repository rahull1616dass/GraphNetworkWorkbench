<script lang="ts">
  import { onMount } from "svelte";
  import { default as vegaEmbed } from "vega-embed";
  import LossVisSpec from "../../data/LossVisSpec";
  import { createEventDispatcher } from "svelte";
  import cloneDeep from "lodash.clonedeep";

  let id = `loss-${Math.random().toString(36).substring(2, 15)}`;

  const dispatcher = createEventDispatcher();
  export let losses: number[] = undefined;

  onMount(() => {
    if (losses === undefined) {
      return;
    }

    // Create a deep copy of LossVisSpec
    let LossVisSpecCopy = cloneDeep(LossVisSpec);

    // Modify the copy instead of the original
    LossVisSpecCopy.data.values = losses.map((l, i) => ({ epoch: i + 1, loss: l }));
    LossVisSpecCopy.signals = [{ name: "losses", value: losses }];
    vegaEmbed("#" + id, LossVisSpecCopy).then((result) => {
      dispatcher("plotLoaded", result.view);
    });
  });
</script>

<div id={id} />
