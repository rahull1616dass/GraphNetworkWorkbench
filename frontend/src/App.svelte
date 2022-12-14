<script lang="ts">
  import { MenuItem } from "./definitions/menuItem"
  import NetworkListItem from "./components/common/NetworkListItem.svelte"
  import Home from "./components/pages/Home.svelte"
  import Plot from "./components/pages/Workbench/Plot/Plot.svelte"
  import Register from "./components/pages/Register.svelte"
  import Login from "./components/pages/Login.svelte"
  import Experiments from "./components/pages/Workbench/Experiments.svelte"
  import Reports from "./components/pages/Workbench/Reports.svelte"
  import {
    selectedMenuItem,
    authUserStore,
    loginUserStore,
    networksList,
    selectedNetworkIndex,
  } from "./stores"
  import { getAuth } from "firebase/auth"
  import {
    loginUser,
    getNetworks as getNetworksFromFirestore,
  } from "./api/firebase"
  import { ProgressBarData } from "./definitions/progressBarData"
  import { ProgressBar } from "carbon-components-svelte"
  import { onMount } from "svelte"

  /* ---- PAGE LOAD AND LOGIN ---- */
  let progressBarData: ProgressBarData = new ProgressBarData(true, "Loading...")
  let isLoggedIn: boolean = false
  onMount(() => {
    /*
    If there is a loginUserStore already in the localstorage, try to login with that user from Firebase Auth.
    If Firebase Auth succeeds, the user is logged in and his networks are fetched.
    */
    if ($loginUserStore) {
      loginUser($loginUserStore)
        .then((user) => checkForLoggedIn())
        .catch((error) => {
          console.log(error)
          progressBarData.isPresent = false
        })
    } else progressBarData.isPresent = false
  })

  // Should update after the user manually logins or registers
  $: $authUserStore, checkForLoggedIn()

  function checkForLoggedIn() {
    isLoggedIn = $authUserStore !== undefined && getAuth().currentUser !== null
    if (isLoggedIn && $networksList.length === 0) {
      progressBarData.text = "Fetching networks..."
      getNetworksFromFirestore()
        .then(() => (progressBarData.isPresent = false))
        .catch(() => (progressBarData.isPresent = false))
    }
  }

  const performLogout = () => {
    progressBarData.text = "Logging out..."
    progressBarData.isPresent = true
    getAuth()
      .signOut()
      .then(() => {
        console.log("User signed out")
        isLoggedIn = false
        $authUserStore = undefined
        $loginUserStore = undefined
        $networksList = []
        progressBarData.isPresent = false
      })
      .catch((error) => {
        console.log(`Error while signing out: ${error}`)
        progressBarData.isPresent = false
      })
  }

  /* ---- My Networks ---- */
  let isHoveringMyNetworks: boolean = false
  let isHoveringNetworksList: boolean = false

  $: $selectedNetworkIndex, selectNetwork()

  function selectNetwork() {
    if ($selectedNetworkIndex === undefined) return
    isHoveringMyNetworks = false
    isHoveringNetworksList = false
    $selectedMenuItem = MenuItem.PLOT
  }
</script>

{#if progressBarData.isPresent}
  <div class="main_progress_bar">
    <ProgressBar helperText={progressBarData.text} />
  </div>
{:else}
  {#if isLoggedIn}
    <ul id="menu">
      <li>
        <a href="/" on:click|preventDefault={performLogout}>Logout</a>
      </li>
      <li>
        <div
          class:my_networks_open={isHoveringMyNetworks}
          class:my_networks={!isHoveringMyNetworks}
          on:mouseenter={() => (isHoveringMyNetworks = true)}
          on:mouseleave={() => /*(isHoveringMyNetworks = false)*/ null}
        >
          My Networks
        </div>
      </li>
      {#if $selectedNetworkIndex !== undefined}
        <li>
          <a
            href="/"
            on:click|preventDefault={() => ($selectedMenuItem = MenuItem.PLOT)}
            >Visualize</a
          >
        </li>
        <li>
          <a
            href="/"
            on:click|preventDefault={() =>
              ($selectedMenuItem = MenuItem.EXPERIMENTS)}>Experiments</a
          >
        </li>
        <li>
          <a
            href="/"
            on:click|preventDefault={() =>
              ($selectedMenuItem = MenuItem.REPORTS)}>Reports</a
          >
        </li>
      {/if}
    </ul>
  {/if}
  <div class="root">
    {#if $selectedMenuItem === MenuItem.HOME}
      <Home />
    {:else if $selectedMenuItem === MenuItem.LOGIN}
      <Login />
    {:else if $selectedMenuItem === MenuItem.REGISTER}
      <Register />
    {:else if $selectedMenuItem === MenuItem.PLOT}
      <Plot />
    {:else if $selectedMenuItem === MenuItem.EXPERIMENTS}
      <Experiments />
    {:else if $selectedMenuItem === MenuItem.REPORTS}
      <Reports />
    {/if}
  </div>
  {#if isHoveringMyNetworks || isHoveringNetworksList}
    <div
      class="networks_list"
      on:mouseenter={() => (isHoveringNetworksList = true)}
      on:mouseleave={() => (isHoveringNetworksList = false)}
    >
      <div class="networks_list_header">
        <p>Networks</p>
      </div>
      <div class="networks_list_items">
        {#each $networksList as network, index}
          <NetworkListItem
            {network}
            {index}
            selected={$selectedNetworkIndex == index}
            on:selectItem={(event) => {
              $selectedNetworkIndex = event.detail.selectedIndex
            }}
          />
        {/each}
      </div>
    </div>
  {/if}
{/if}

<style>
  .main_progress_bar {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  .root {
    overflow: auto;
    background-color: whitesmoke;
  }

  .my_networks_open {
    line-height: 40px;
    display: inline-block;
    width: 100%;
    color: white;
    height: 100%;
    background-color: #0f62fe;
  }
  .my_networks {
    line-height: 40px;
    display: inline-block;
    width: 100%;
    color: white;
    height: 100%;
  }

  .networks_list {
    position: absolute;
    top: 7%;
    left: 20%;
    width: 20%;
    right: 0;
    background-color: white;
    border: 1px solid #e0e0e0;
    border-top: none;
    z-index: 1;
  }

  .networks_list_header {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }

  ul#menu {
    width: 100%;
    display: inline-block;
  }
</style>
