<script lang="ts">
  import EmbeddingVisSpec from "../../data/EmbeddingVisSpec";
  import { onMount } from "svelte";
  import { default as vegaEmbed } from "vega-embed";
  import { createEventDispatcher } from "svelte";
  import type { Task } from "../../definitions/task";
  import cloneDeep from "lodash.clonedeep";

  export let task: Task = undefined;
  let id = `embedding-${Math.random().toString(36).substring(2, 15)}`;

  const dispatcher = createEventDispatcher();
  loadEmbedding();

  onMount(() => {
    loadEmbedding();
  });

  function loadEmbedding() {
    // Create a deep copy of EmbeddingVisSpec
    let EmbeddingVisSpecCopy = cloneDeep(EmbeddingVisSpec);

    // Modify the copy instead of the original
    // @ts-ignore
    EmbeddingVisSpecCopy.data.values = Object.values(task.embeddings).map(
      ([x, y]) => ({ x, y })
    );
    vegaEmbed("#" + id, EmbeddingVisSpecCopy).then((result) => {
      dispatcher("plotLoaded", result.view);
    });
  }
</script>

<div id={id} />
