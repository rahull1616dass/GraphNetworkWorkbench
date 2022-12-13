<script lang="ts">
  import { MenuItem } from "./definitions/menuItem"
  import NetworkListItem from "./components/common/NetworkListItem.svelte"
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
    selectedNetworkIndex
  } from "./stores"
  import { getAuth } from "firebase/auth"
  import {
    loginUser,
    getNetworks as getNetworksFromFirestore,
  } from "./api/firebase"
  import { ProgressBarData } from "./definitions/progressBarData"
  import { ProgressBar } from "carbon-components-svelte"

  let progressBarData: ProgressBarData = new ProgressBarData(true, "Loading...")
  let isLoggedIn: boolean = false
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

  let isMyNetworksMenuOpen: boolean = false
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
          class:my_networks_open={isMyNetworksMenuOpen}
          class:my_networks={!isMyNetworksMenuOpen}
          on:mouseenter={() => {
            console.log("enter")
            isMyNetworksMenuOpen = true
          }}
          on:mouseleave={() => {
            console.log("leave")
            isMyNetworksMenuOpen = false
          }}
        >
          My Networks
        </div>
      </li>
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
          on:click|preventDefault={() => ($selectedMenuItem = MenuItem.REPORTS)}
          >Reports</a
        >
      </li>
    </ul>
  {/if}
  {#if isMyNetworksMenuOpen}
    <div class="networks_list">
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
  <div class="root">
    {#if $selectedMenuItem === MenuItem.LOGIN}
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

  .networks_list_header {
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #f5f5f5;
    border-bottom: 1px solid #e0e0e0;
    padding: 0.5rem;
  }
  .networks_list {
    margin-top: 5.6%;
    overflow-y: scroll;
    overflow-x: hidden;
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 20%;
    background-color: #f5f5f5;
  }
  
  ul#menu {
    width: 100%;
    display: inline-block;
  }
</style>
