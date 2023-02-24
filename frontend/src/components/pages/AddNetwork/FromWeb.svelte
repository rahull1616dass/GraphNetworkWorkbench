<script lang="ts">
  import { onMount } from "svelte"
  import { netzschleuderNetworkNames } from "../../../stores"
  import { SideNavItems } from "carbon-components-svelte"
  import FetchableAccordionItem from "../../common/FetchableAccordionItem.svelte"
  import { Accordion } from "carbon-components-svelte"
  import request from "../../../api/request"
  import decompressResponse from "decompress-response"
  import { parseReadableStream } from "../../../util/networkParserUtil"
  import { parse } from "vega"
  import { selectedMenuItem } from "../../../stores"
  import { MenuItem } from "../../../definitions/menuItem"
  import JSZip from 'jszip'
  import { browserLocalPersistence } from "firebase/auth";
  import { uploadNetworkToStorage } from "../../../api/firebase"
  import { Network } from "../../../definitions/network"
  import type { Link, Metadata, Node } from "../../../definitions/network"
  import {onFetchNetwork, uploadedNetworkStatus} from "../AddNetwork/ImportNetwork"


  onMount(async () => {
    /*
    Once the user selects an import type from the modal, the selectedImportType is changed to 
    something other than NONE.
    At this point, the selectedMenuItem must be set to NONE so that the root div is not rendered
    on top of the import pages
    */
    $selectedMenuItem = MenuItem.FROM_WEB
    netzschleuderNetworkNames.set(
      await request("https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetworks")
    )
  })
  
  
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
              isNetworkUploaded={uploadedNetworkStatus}
              title={networkName}
              endpoint={`https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetowrkDescription?networkName=${networkName}`}
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
