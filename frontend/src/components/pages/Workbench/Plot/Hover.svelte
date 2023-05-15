<script lang="ts">
  import type { HoverData } from "../../../../definitions/hoverData"
  import { HoverType } from "../../../../definitions/hoverType"
  export let hoverData: HoverData = undefined
  console.log("x")
</script>

<main>
  {#if hoverData?.type === HoverType.NODE}
  <div class="node" style="--x: {hoverData?.x}px; --y: {hoverData?.y}px;">
    {hoverData?.node?.name ?? hoverData?.node?.index}<br />
    {#each Object.entries(hoverData?.node) as [key, value]}
      {@html key !== "is_train" && key !== "name" && key !== "index" ? `<br>${key}: ${value ?? "No data"}` : ""}
      {@html key === "is_train" && value != null ? `<br>In the ${value ? "Train" : "Test"} set` : ""}
    {/each}
  </div>
  
  {:else if hoverData?.type === HoverType.LINK}
    <div class="link" style="--x: {hoverData?.x}px; --y: {hoverData?.y}px;">
      {hoverData?.link?.source?.datum?.name ||
      hoverData?.link?.target?.datum?.name
        ? `${hoverData?.link?.source?.datum?.name?.toString()} -> ${
            hoverData?.link?.target?.datum?.name
          }`
        : hoverData?.link?.source?.datum?.index ||
          hoverData?.link?.target?.datum?.index
        ? `Node_${hoverData?.link?.source?.datum?.index} -> Node_${hoverData?.link?.target?.datum?.index}`
        : "No node names defined"}<br />
      <br />
      {#each Object.entries(hoverData?.link) as [key, value]}
        {@html key !== "source" && key !== "target"
          ? `${key}: ${value}<br />`
          : ""}
      {/each}
    </div>
  {/if}
</main>

<style lang="scss">
  .node {
    position: absolute;
    top: var(--y);
    left: var(--x);
    border-radius: 5px;
    padding: 10px;
    cursor: pointer;
    background-color: lightgreen;
    transition: background-color 0.2s ease-in-out;
    margin: 10px;
  }
  .link {
    position: absolute;
    top: var(--y);
    left: var(--x);
    border-radius: 5px;
    padding: 10px;
    background-color: lightcyan;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    margin: 10px;
  }
</style>
