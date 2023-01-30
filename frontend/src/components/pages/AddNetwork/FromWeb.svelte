<script lang="ts">
  import { Endpoints } from "../../../definitions/constants"
  import { onMount } from "svelte"
  import { netzschleuderNetworkNames } from "../../../stores"
  import { SideNavItems } from "carbon-components-svelte"
  import FetchableAccordionItem from "../../common/FetchableAccordionItem.svelte"
  import { Accordion } from "carbon-components-svelte"
  import request from "../../../api/request"
  import decompressResponse from "decompress-response"
  import { parseReadableStream } from "./UploadNetwork/networkParser"
  import { parse } from "vega"
  import { selectedMenuItem } from "../../../stores"
  import { MenuItem } from "../../../definitions/menuItem"

  onMount(async () => {
    /*
    Once the user selects an import type from the modal, the selectedImportType is changed to 
    something other than NONE.
    At this point, the selectedMenuItem must be set to NONE so that the root div is not rendered
    on top of the import pages
    */
    $selectedMenuItem = MenuItem.FROM_WEB
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
  let searchTerm = "";
  $: filteredItems = $netzschleuderNetworkNames.filter(item => item.includes(searchTerm));
</script>

<main>
  <h1>Network Names</h1>
  {#if $netzschleuderNetworkNames}
    <Accordion>
      <input type="text" bind:value={searchTerm} placeholder="Search..." />
      <div class ="OuterContailer">
        <div class="networks">
          {#each filteredItems as networkName}
            <FetchableAccordionItem
              title={networkName}
              endpoint={`${Endpoints.NETZSCHELEUDER}${Endpoints.NETZSCLEUDER_NET}${networkName}`}
              on:fetchNetwork={onFetchNetwork}
            />
          {/each}
        </div>
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
    max-height: 400px;
    flex-wrap: nowrap;
    justify-content: flex-start;
    overflow: scroll;
  }
  .OuterContailer{
    overflow: auto;
    width: 100%;
  }
</style>
