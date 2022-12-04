<script lang="ts">
  import { MenuItem } from "./definitions/menuItem"
  import Main from "./components/pages/Main.svelte"
  import Plot from "./components/pages/Plot/Plot.svelte"
  import Register from "./components/pages/Register.svelte"
  import Login from "./components/pages/Login.svelte"
  import { selectedMenuItem, userStore, networksList } from "./stores"
  import { getAuth } from "firebase/auth"
  import { getNetworks } from "./api/firebase"
  import { ProgressBarData } from "./definitions/progressBarData"
  
  let progressBarData: ProgressBarData = new ProgressBarData(false, "Fetching networks...")
  let isLoggedIn: boolean = false
  $: {
    isLoggedIn = $userStore !== undefined && getAuth().currentUser !== null
    if (isLoggedIn && $networksList.length === 0) {
      getNetworks()
    }
  }
</script>

<ul id="menu">
  <li>
    {#if !isLoggedIn}
      <a
        href="/"
        on:click|preventDefault={() => ($selectedMenuItem = MenuItem.LOGIN)}
        >Login</a
      >
    {/if}
  </li>
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
  {:else if $selectedMenuItem === MenuItem.LOGIN}
    <Login />
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
  ul#menu {
    width: 100%;
    display: inline-block;
  }
</style>
