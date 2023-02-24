<script lang="ts">
  import { onMount } from "svelte";
  import { netzschleuderNetworkNames } from "../../../stores";
  import { SideNavItems } from "carbon-components-svelte";
  import FetchableAccordionItem from "../../common/FetchableAccordionItem.svelte";
  import { Accordion } from "carbon-components-svelte";
  import request from "../../../api/request";
  import decompressResponse from "decompress-response";
  import { parseReadableStream } from "../../../util/networkParserUtil";
  import { parse } from "vega";
  import { selectedMenuItem } from "../../../stores";
  import { MenuItem } from "../../../definitions/menuItem";
  import JSZip from "jszip";
  import { browserLocalPersistence } from "firebase/auth";
  import { uploadNetworkToStorage } from "../../../api/firebase";
  import { Network } from "../../../definitions/network";
  import type { Link, Metadata, Node } from "../../../definitions/network";
  import { fade, slide, scale, fly } from "svelte/transition";

  onMount(async () => {
    /*
    Once the user selects an import type from the modal, the selectedImportType is changed to 
    something other than NONE.
    At this point, the selectedMenuItem must be set to NONE so that the root div is not rendered
    on top of the import pages
    */
    $selectedMenuItem = MenuItem.FROM_WEB;
    netzschleuderNetworkNames.set(
      await request(
        "https://us-central1-graphlearningworkbench.cloudfunctions.net/getNetworks"
      )
    );
  });

  async function onFetchNetwork(event) {
    fetch(
      `https://us-central1-graphlearningworkbench.cloudfunctions.net/downloadNetworkFile?networkName=${event.detail.networkName}`
    )
      .then((response) => response.blob())
      .then((blob) => {
        return JSZip.loadAsync(blob);
      })
      .then((zip) => {
        let edgeFile;
        let nodeFile;
        edgeFile = zip.files["edges.csv"].async("text");
        nodeFile = zip.files["nodes.csv"].async("text");
        return Promise.all([edgeFile, nodeFile]);
      })
      .then((alltext) => {
        let nodesString = removeCSVColumns(alltext[1].replace("# ", ""), [
          " name",
          " _pos",
        ]);
        let edgesString = alltext[0].replace("# ", "");
        let network = new Network();
        network.metadata.name = event.detail.networkName;
        network.metadata.description = event.detail.content.description;
        network.metadata.id = event.detail.networkName;
        network.metadata.color = "";
        return UploadTheData(nodesString, edgesString, network);
      })
      .then((url) => {
        console.log(`Network uploaded to ${url}`);
        uploadedNetwotk = true;
      });
  }
  let uploadedNetwotk: boolean;
  function UploadTheData(nodes, edges, network) {
    console.log(nodes);
    console.log(edges);
    let nodesFile = new File([nodes], "Nodes.csv", { type: "text/csv" });
    let edgesFile = new File([edges], "Edges.csv", { type: "text/csv" });

    network.nodes = <Node[]>JSON.parse(JSON.stringify(nodes));
    network.links = <Link[]>JSON.parse(JSON.stringify(edges));
    return uploadNetworkToStorage(network.metadata, nodesFile, edgesFile);
  }
  function removeCSVColumns(csvData, columnsToRemove) {
    const rows = csvData.split("\n").map((row) => {
      const cells = [];
      let cell = "";
      let insideQuote = false;
      for (const char of row) {
        if (char === '"') {
          insideQuote = !insideQuote;
        } else if (char === "," && !insideQuote) {
          cells.push(cell);
          cell = "";
        } else {
          cell += char;
        }
      }
      cells.push(cell);
      return cells;
    });
    const header = rows[0];
    let indicesToRemove = [];
    if (Array.isArray(columnsToRemove)) {
      for (const col of columnsToRemove) {
        const index = header.indexOf(col);
        if (index !== -1) {
          indicesToRemove.push(index);
        }
      }
    }
    return rows
      .map((row) => {
        return row.filter((_, i) => !indicesToRemove.includes(i));
      })
      .map((row) => row.join(","))
      .join("\n");
  }
  let searchTerm = "";
  $: filteredItems = $netzschleuderNetworkNames.filter((item) =>
    item.includes(searchTerm)
  );
</script>

<main
  in:fly={{ y: -50, duration: 350, delay: 300 }}
  out:fly={{ y: -50, duration: 350 }}
>
  <h1>Network Names</h1>
  {#if $netzschleuderNetworkNames}
    <Accordion>
      <input type="text" bind:value={searchTerm} placeholder="Search..." />
      <div class="OuterContailer">
        <div class="networks">
          {#each filteredItems as networkName}
            <FetchableAccordionItem
              isNetworkUploaded={uploadedNetwotk}
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
  .OuterContailer {
    overflow: auto;
    width: 100%;
  }
</style>
