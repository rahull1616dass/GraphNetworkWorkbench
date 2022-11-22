<script lang="ts">
    import { MenuItem } from "./definitions/menuItem";
    import Main from "./components/Main.svelte";
    import Plot from "./components/Plot/Plot.svelte";

    let selectedMenuItem: MenuItem = MenuItem.HOME;
</script>

<ul id="menu">
    <li>
        <a
            href="/"
            on:click|preventDefault={() => (selectedMenuItem = MenuItem.HOME)}
            >Home</a
        >
    </li>
    |
    <li>
        <a
            href="/"
            on:click|preventDefault={() => (selectedMenuItem = MenuItem.PLOT)}
            >Plot</a
        >
    </li>
</ul>

{#if selectedMenuItem === MenuItem.HOME}
    <Main />
{:else if selectedMenuItem === MenuItem.PLOT}
    <Plot />
{/if}


<style>
    ul#menu li {
        display: inline;
    }
</style>
