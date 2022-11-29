<script lang="ts">
    import type { HoverData } from "../../../definitions/hoverData"
    export let hoverData: HoverData = undefined
</script>


<main>
    {#if hoverData != undefined}
        <div class="root" style="--x: {hoverData.x}px; --y: {hoverData.y*2}px;">
            {hoverData.nodeName} {hoverData.x} {hoverData.y}
        </div>
    {/if}

</main>

<style lang="scss">
    .root {
        position:absolute;
        top: var(--y);
        left: var(--x);
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 10px;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        margin: 10px;
    }
</style>