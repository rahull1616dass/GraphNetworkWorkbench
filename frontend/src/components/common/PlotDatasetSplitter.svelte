<script lang="ts">
import { selectedNetworkIndex, networksList } from "../../stores"
import { default as vegaEmbed } from "vega-embed"
import VisSpec from "../../data/VisSpec"
import { updateVisSpec, setColorKey } from "../../helper/VisSpecUtil"
import { onMount } from "svelte"


export let seed: number = 0
export let trainPercentage: number = 0.8



// Run an onMount function to initialize the plot
onMount(() => {

    setColorKey(VisSpec, "train_test")
    // Anytime the networksList store value is updated, update the network
    loadNetwork()
  })

function loadNetwork(){

}
</script>

<style lang="scss">

</style>