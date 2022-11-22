<script lang="ts">
  import MiserablesData from "../../data/VisSpec"
  import { default as vegaEmbed } from "vega-embed"
  import { networksList } from "../../stores"

  if ($networksList.length > 0) {
    // Remove the default data from the Miserables Network that is stored in the url key
    delete MiserablesData["data"]["node-data"]["url"]
    delete MiserablesData["data"]["link-data"]["url"]
    
    MiserablesData["data"]["node-data"]["values"] = $networksList[0].nodes
    MiserablesData["data"]["link-data"]["values"] = $networksList[0].links
  } else {
    // Refer https://www.koderhq.com/tutorial/svelte/json-storage/
    vegaEmbed("#viz", MiserablesData, { actions: false }).catch((error) =>
      console.log(error)
    )
  }
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
