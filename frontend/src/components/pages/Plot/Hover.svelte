<script lang="ts">
  import type { HoverData } from "../../../definitions/hoverData"
  import { HoverType } from "../../../definitions/hoverType"
  export let hoverData: HoverData = undefined
</script>

<main>
  {#if hoverData != undefined}
    {#if hoverData.type === HoverType.NODE}
      <div class="node" style="--x: {hoverData.x}px; --y: {hoverData.y}px;">
        {hoverData.node.name}<br />
        Group: {hoverData.node.group}
      </div>
    {:else if hoverData.type === HoverType.LINK}
      <div class="link" style="--x: {hoverData.x}px; --y: {hoverData.y}px;">
        {hoverData.link.source} -> {hoverData.link.target}<br />
        Value: {hoverData.link.value}
      </div>
    {/if}
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
