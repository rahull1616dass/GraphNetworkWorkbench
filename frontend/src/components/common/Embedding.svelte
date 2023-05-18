<script lang="ts">
  import EmbeddingVisSpec from "../../data/EmbeddingVisSpec";
  import { onMount } from "svelte";
  import { default as vegaEmbed } from "vega-embed";
  import { createEventDispatcher } from "svelte";
  import type { Task } from "../../definitions/task";

  export let task: Task = undefined;
  let id = `embedding-${Math.random().toString(36).substring(2, 15)}`;

  const dispatcher = createEventDispatcher();
  loadEmbedding();

  onMount(() => {
    loadEmbedding();
  });

  function loadEmbedding() {
    // @ts-ignore
    EmbeddingVisSpec.data.values = Object.values(task.embeddings).map(
      ([x, y]) => ({ x, y })
    );
    vegaEmbed("#" + id, EmbeddingVisSpec).then((result) => {
      dispatcher("plotLoaded", result.view);
    });
  }
</script>

<div {id} />
