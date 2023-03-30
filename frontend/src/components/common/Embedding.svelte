<script lang="ts">
import EmbeddingVisSpec from "../../data/EmbeddingVisSpec"
import { onMount } from "svelte"
import { default as vegaEmbed } from "vega-embed"
import { createEventDispatcher } from "svelte"
import { Task } from "../../definitions/task"

export let task: Task = undefined
const dispatcher = createEventDispatcher()
loadEmbedding()


onMount(() => {
    loadEmbedding()
})

function loadEmbedding(){
    //EmbeddingVisSpec.data.values = embedding.map(([x, y]) => ({ x, y }));
    vegaEmbed("#embedding", EmbeddingVisSpec).then((result) => {
        dispatcher("plotLoaded", result.view)
    })
}

</script>

<div id="embedding"></div>

<style lang="scss">

</style>