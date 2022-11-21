<script lang="ts">
  import { Endpoints } from "../../constants"
  import { onMount } from "svelte"
  import { netzschleuderNetworkNames } from "../../stores"
  import { SideNavItems } from "carbon-components-svelte"

  onMount(async () => {
    const res = await fetch(Endpoints.NETZSCHLEUDER_NETWORK_NAMES, {
      mode: "no-cors"
    })
    .then((resp) => {
        /*if (!resp.ok) {
          throw `Server error: [${resp.status}] [${resp.statusText}] [${resp.url}]`
        }*/
        console.log(resp)
        return resp.text()
      })
      .then((data) => {
        //console.log("Received data: " + JSON.stringify(data))
        console.log(`${data} is the text`)
        //netzschleuderNetworkNames.set(data)
      })
      .catch((error) => {
        console.log(error)
        return new Array()
      })
  })
</script>

<main>
  <h1>Network Names</h1>
  <ul>
    {#each $netzschleuderNetworkNames as name}
      <li>{name}</li>
    {:else}
      <p>Geting network names...</p>
    {/each}
  </ul>
</main>
