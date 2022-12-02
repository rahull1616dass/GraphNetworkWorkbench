<script lang="ts">
    import { MenuItem } from "./definitions/menuItem"
    import Main from "./components/pages/Main.svelte"
    import Plot from  "./components/pages/Plot/Plot.svelte"
    import Register from "./components/pages/Register.svelte"
    import { selectedMenuItem } from "./stores"
    import { addDocument } from "./api/firebase"

    //addDocument()

</script>

<ul id="menu">
    <li>
        <a
            href="/"
            on:click|preventDefault={() => ($selectedMenuItem = MenuItem.REGISTER)}
            >Register</a
        >
    </li>
    <li>
        <a
            href="/"
            on:click|preventDefault={() => ($selectedMenuItem = MenuItem.HOME)}
            >Home</a
        >
    </li>
    <li>
        <a
            href="/"
            on:click|preventDefault={() => ($selectedMenuItem = MenuItem.PLOT)}
            >Plot</a
        >
    </li>
</ul>

<div class="root">

{#if $selectedMenuItem === MenuItem.HOME}
    <Main />
{:else if $selectedMenuItem === MenuItem.REGISTER}
    <Register />
{:else if $selectedMenuItem === MenuItem.PLOT}
    <Plot />
{/if}
</div>

<style>
    .root {
        overflow: auto;
        background-color: whitesmoke;
    }
    ul#menu{
        width: 100%;
        display: inline-block;
    }
</style>
