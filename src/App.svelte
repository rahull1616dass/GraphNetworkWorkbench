<script lang="ts">
    import { MenuItem } from "./definitions/menuItem"
    import Main from "./components/pages/Main.svelte"
    import Plot from  "./components/pages/Plot/Plot.svelte"
    import { selectedMenuItem } from "./stores"
</script>

<ul id="menu">
    <li>
        <a
            href="/"
            on:click|preventDefault={() => ($selectedMenuItem = MenuItem.HOME)}
            >Home</a
        >
    </li>
    |
    <li>
        <a
            href="/"
            on:click|preventDefault={() => ($selectedMenuItem = MenuItem.PLOT)}
            >Plot</a
        >
    </li>
</ul>

{#if $selectedMenuItem === MenuItem.HOME}
    <Main />
{:else if $selectedMenuItem === MenuItem.PLOT}
    <Plot />
{/if}


<style>
    ul#menu{
        width: 100%;
        display: inline-block;
    }
</style>
