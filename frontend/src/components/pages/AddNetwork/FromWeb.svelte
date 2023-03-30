<script lang="ts">
  import { onMount } from "svelte"
  import { netzschleuderNetworkNames } from "../../../stores"
  import { ProgressBar } from "carbon-components-svelte"
  import FetchableAccordionItem from "../../common/FetchableAccordionItem.svelte"
  import { Accordion } from "carbon-components-svelte"
  import request from "../../../api/request"
  import { selectedMenuItem } from "../../../stores"
  import { MenuItem } from "../../../definitions/menuItem"
  import { ProgressBarData } from "../../../definitions/progressBarData"
  import InfoBox from "../../common/InfoBox.svelte";
  import InfoText from "../../common/InfoText.svelte";

  let infoBoxContent = "Networks are the building blocks of the workbench. You can create a network by uploading a file or by importing a network from the web by clicking on the 'Create Network' button.";
  $: isInfoModalOpen = false

  onMount(async () => {
    /*
    Once the user selects an import type from the modal, the selectedImportType is changed to 
    something other than NONE.
    At this point, the selectedMenuItem must be set to NONE so that the root div is not rendered
    on top of the import pages
    */
    $selectedMenuItem = MenuItem.FROM_WEB
    netzschleuderNetworkNames.set(
      await request(
        "https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetworks"
      )
    )
    progressBarData.isPresent = false
  })
  
  let searchTerm = ""
  let progressBarData: ProgressBarData = new ProgressBarData(
    true,
    "Fetching networks..."
  )
  $: filteredItems = $netzschleuderNetworkNames.filter((item) =>
    item.includes(searchTerm)
  )
</script>

<div class="info">
  <InfoBox
    bind:isInfoModalOpen
    headerText="My Networks Guide"
    bodyText={infoBoxContent}
  />
</div>

<main>
  {#if progressBarData.isPresent}
    <div class="progress_bar">
      <ProgressBar helperText={progressBarData.text} />
    </div>
  {:else}
    <InfoText margintop={0} marginbottom={2}>Here are the networks from Netzschleuder, you can choose network to import</InfoText>
    <Accordion>
      <input class="search-input" type="text" bind:value={searchTerm} placeholder="Search..." />
      <div class="OuterContailer">
        <div class="networks">
          {#each filteredItems as networkName}
            <FetchableAccordionItem
              accordionTitle={networkName}
            />
          {/each}
        </div>
      </div>
    </Accordion>
  {/if}
</main>

<style lang="scss">

.search-input {
    font-size: 1rem;
    padding: 0.5rem 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: white;
    transition: all 0.2s ease-in-out;
    outline: none;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .search-input:focus {
    border-color: var(--wueblue);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .search-input::placeholder {
    color: #888;
    font-style: italic;
  }
  
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
  .OuterContailer {
    overflow: auto;
    width: 100%;
  }

  .progress_bar {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
</style>
