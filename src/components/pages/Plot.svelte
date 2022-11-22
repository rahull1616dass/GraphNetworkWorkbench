<script lang="ts">
  import MiserablesData from "../../data/VisSpec"
  import SampleNetwork from "../../data/SampleNetwork"
  import { default as vegaEmbed } from "vega-embed"
  import { networksList } from "../../stores"

  if ($networksList.length > 0) {
    /*
    Remove the default data from the Miserables Network that is stored in the url key
    data[0] = nodes, data[1] = links
    */
    SampleNetwork.data[0].values = $networksList[0].nodes
    SampleNetwork.data[1].values = $networksList[0].links
    vegaEmbed("#viz", SampleNetwork, { actions: false }).catch((error) =>
      console.log(error)
    )
  } else {
    // Refer https://www.koderhq.com/tutorial/svelte/json-storage/
    /*
    delete MiserablesData.data[0].url
    delete MiserablesData.data[1].url
    MiserablesData.data[0].values = $networksList[0].nodes
    MiserablesData.data[1].values = $networksList[0].links
     */

    vegaEmbed("#viz", MiserablesData, { actions: false }).catch((error) =>
      console.log(error)
    )
  }

  console.log("x")
</script>

<main>
  {#if $networksList.length == 0}
    <div class="no_networks">
      <h1>
        No networks to display. Displaying the default Miserables network 🥺
      </h1>
    </div>
  {:else}
    <div class="networks" />
  {/if}

  <div id="viz" />
</main>

<style>
</style>
