<script lang="ts">
import EmbeddingVisSpec from "../../data/EmbeddingVisSpec"
import { onMount } from "svelte"
import { default as vegaEmbed } from "vega-embed"

loadEmbedding()

function loadEmbedding(){
    vegaEmbed("#embedding", EmbeddingVisSpec)
}

</script>

<div id="embedding"></div>

<style lang="scss">

</style>