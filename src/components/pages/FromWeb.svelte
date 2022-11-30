<script lang="ts">
  import { Endpoints } from "../../definitions/constants"
  import { onMount } from "svelte"
  import { netzschleuderNetworkNames } from "../../stores"
  import { SideNavItems } from "carbon-components-svelte"
  import request from "../../request"

  onMount(async () => {
    console.log(`${Endpoints.NETZSCHELEUDER}${Endpoints.NETZSCHELEUDER_NETS}`)
    //const response = await request(`${Endpoints.NETZSCHELEUDER}${Endpoints.NETZSCHELEUDER_NETS}`)
    const response = await request("https://networks.skewed.de/api/nets")
    netzschleuderNetworkNames.set(response)
  })
</script>

<main>
  <h1>Network Names</h1>
    {#each $netzschleuderNetworkNames as name}
      {name}<br>
    {:else}
      <p>Geting network names...</p>
    {/each}
</main>
