<script lang="ts">
    import { MenuItem } from "./components/MenuItem";
    import Main from "./components/Main.svelte";
    import Plot from "./components/Plot/Plot.svelte";
    import { testStoreValue } from "./stores";

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

<p>Imported store value is = {$testStoreValue}</p>
<button on:click|preventDefault={() => ($testStoreValue += "!")}
    >Change store value</button
>

<style>
    ul#menu li {
        display: inline;
    }
</style>
