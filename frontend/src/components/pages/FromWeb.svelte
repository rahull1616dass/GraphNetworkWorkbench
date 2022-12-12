<script lang="ts">
  import { Endpoints } from "../../definitions/constants"
  import { onMount } from "svelte"
  import { netzschleuderNetworkNames } from "../../stores"
  import { SideNavItems } from "carbon-components-svelte"
  import FetchableAccordionItem from "../common/FetchableAccordionItem.svelte"
  import { Accordion } from "carbon-components-svelte"
  import request from "../../api/request"
  import decompressResponse from 'decompress-response'
  import { parseReadableStream }  from "./UploadNetwork/networkParser"
  import { parse } from "vega"


  onMount(async () => {
    console.log(`${Endpoints.NETZSCHELEUDER}${Endpoints.NETZSCHELEUDER_NETS}`)
    //const response = await request(`${Endpoints.NETZSCHELEUDER}${Endpoints.NETZSCHELEUDER_NETS}`)
    netzschleuderNetworkNames.set(
      await request("https://networks.skewed.de/api/nets")
    )
  })

  async function onFetchNetwork(event) {
    const response = await request(
      `https://networks.skewed.de/net/${event.detail.networkName}/files/${event.detail.networkName}.csv.zip`,
      undefined,
      false
    )
    // Extract the zipped file on response.body to a REadableStream
    const readableStream = decompressResponse(response).body

    parseReadableStream(readableStream, undefined)
    // https://stackoverflow.com/a/61013504/11330757
    console.log(response)
  }
</script>

<main>
  <h1>Network Names</h1>
  {#if $netzschleuderNetworkNames}
    <Accordion>
      <div class="networks">
        {#each $netzschleuderNetworkNames as networkName}
          <FetchableAccordionItem
            title={networkName}
            endpoint={`${Endpoints.NETZSCHELEUDER}${Endpoints.NETZSCLEUDER_NET}${networkName}`}
            on:fetchNetwork={onFetchNetwork}
          />
        {/each}
      </div>
    </Accordion>
  {:else}
    <p>Fetching networks...</p>
  {/if}
</main>

<style lang="scss">
  main {
    padding: 1rem;
  }

  .networks {
    padding: 1rem;
    display: flex;
    flex-direction: column;
  }
</style>
