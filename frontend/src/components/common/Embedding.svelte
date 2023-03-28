<script lang="ts">
import EmbeddingVisSpec from "../../data/EmbeddingVisSpec"
import { onMount } from "svelte"
import { default as vegaEmbed } from "vega-embed"
import { createEventDispatcher } from "svelte"

const dispatcher = createEventDispatcher()
loadEmbedding()

function loadEmbedding(){
    vegaEmbed("#embedding", EmbeddingVisSpec).then((result) => {
        dispatcher("plotLoaded", result.view)
    })
}

</script>

<div id="embedding"></div>

<style lang="scss">

</style>