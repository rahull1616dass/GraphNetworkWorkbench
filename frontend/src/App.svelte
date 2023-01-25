<script lang="ts">
  import { MenuItem } from "./definitions/menuItem"
  import NetworkListItem from "./components/common/NetworkListItem.svelte"
  import Home from "./components/pages/Home.svelte"
  import Plot from "./components/pages/Workbench/Plot/Plot.svelte"
  import Register from "./components/pages/Register.svelte"
  import Login from "./components/pages/Login.svelte"
  import Profile from "./components/pages/Profile.svelte"
  import Experiments from "./components/pages/Workbench/Experiments.svelte"
  import Reports from "./components/pages/Workbench/Reports.svelte"
  import FromWeb from "./components/pages/AddNetwork/FromWeb.svelte"
  import UploadNetwork from "./components/pages/AddNetwork/UploadNetwork/UploadNetwork.svelte"
  import Header from "./components/common/Header.svelte"
  import Footer from "./components/common/Footer.svelte"
  import Tabs from "./components/common/Tabs.svelte"
  import CustomModal from "./components/common/CustomModal.svelte"
  import Networks from "./components/pages/Workbench/Networks.svelte"
  import {
    selectedMenuItem,
    authUserStore,
    loginUserStore,
    networksList,
    selectedNetworkIndex,
    fetchedNetworkOnce
  } from "./stores"
  import { getAuth } from "firebase/auth"
  import {
    loginUser,
    getNetworks as getNetworksFromFirestore,
    getProfileImage
  } from "./api/firebase"
  import { ProgressBarData } from "./definitions/progressBarData"
  import { ProgressBar, Button } from "carbon-components-svelte"
  import { onMount } from "svelte"
  import ImportModal from "./components/common/ImportModal.svelte"
  import { ImportModalType }  from "./definitions/importModalType"

  /* ---- PAGE LOAD AND LOGIN ---- */
  let progressBarData: ProgressBarData = new ProgressBarData(true, "Loading...")
  let isLoggedIn: boolean = false

  // For some reason, the getNetworksFromFirestore() function is called multiple times on page load.
  // For now, this variable is used to prevent that. TODO: Find a better solution.


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
    isLoggedIn = $authUserStore !== undefined //&& getAuth().currentUser !== null
    if (isLoggedIn && $networksList.length === 0) {
      progressBarData.text = "Fetching networks..."
      if($fetchedNetworkOnce) return
      $fetchedNetworkOnce = true
      getNetworksFromFirestore()
        .then(() => (progressBarData.isPresent = false))
        .catch(() => (progressBarData.isPresent = false))
      getProfileImage()
    }
  }

  /* ---- My Networks ---- */
  let isHoveringMyNetworks: boolean = false
  let isHoveringNetworksList: boolean = false

  // $: $selectedNetworkIndex, selectNetwork()

  // function selectNetwork() {
  //   if ($selectedNetworkIndex === undefined) return
  //   isHoveringMyNetworks = false
  //   isHoveringNetworksList = false
  //   $selectedMenuItem = MenuItem.PLOT
  // }

  /* ---- Import Modal ---- */
  let isImportModalOpen: boolean = false
  let selectedImportType: ImportModalType = ImportModalType.NONE

  let showModal = false
</script>

{#if progressBarData.isPresent}
  <div class="main_progress_bar">
    <ProgressBar helperText={progressBarData.text} />
  </div>
{:else}
    {#if isLoggedIn === true}
    <ul id="menuLogin" class="mainUI">
      <Tabs />
      {#if $selectedMenuItem === MenuItem.HOME}
        <Home />
      {:else if $selectedMenuItem === MenuItem.NETWORKS}
      <Networks/>
      {:else if $selectedMenuItem === MenuItem.PLOT}
      <Plot />
      {:else if $selectedMenuItem === MenuItem.EXPERIMENTS}
      <Experiments/>
      {:else if $selectedMenuItem === MenuItem.REPORTS}
      <Reports/>
      {:else if $selectedMenuItem === MenuItem.PROFILE}
      <Profile />
      {:else if $selectedMenuItem === MenuItem.FROM_WEB}
      <div class ="OuterContailer">
        <div class="InnerContainer">
      <FromWeb />
          
        </div>
      </div>
      {:else if $selectedMenuItem === MenuItem.FROM_PC}
      <UploadNetwork />
      {/if}
    </ul>
    {:else if isLoggedIn === false}
      <Tabs />
      {#if $selectedMenuItem === MenuItem.HOME}
        <Home />
      {:else if $selectedMenuItem === MenuItem.LOGIN}
        <Login />
      {:else if $selectedMenuItem === MenuItem.REGISTER}
        <Register />
      {/if}
    {/if}
{/if}


<Footer />

      <!---
      <li>
        <a href="/" on:click|preventDefault={performLogout}>Logout</a>
      </li>
      <li>
        <div
          class:menu_my_networks_open={isHoveringMyNetworks}
          class:menu_my_networks={!isHoveringMyNetworks}
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
        <Button
          class="btn_networks_list_import"
          on:click={() => {
            isHoveringMyNetworks = false
            isHoveringNetworksList = false
            isImportModalOpen = true
          }}
          size="small"
          on:click>Import Network</Button
        >
      </div>
      <div class="networks_list_items" style="--height: {$networksList.length * 120}px;">
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
  
  <ImportModal bind:selectedImportType bind:open={isImportModalOpen} />
  {#if selectedImportType === ImportModalType.FROM_WEB}
    <FromWeb/>
  {:else if selectedImportType === ImportModalType.UPLOAD}
    <UploadNetwork/>
  {/if}

{/if}
-->



<style lang="scss">
  .main_progress_bar {
    position: absolute;
    top: 100%;
    left: 100%;
    transform: translate(-50%, -50%);
  }
  .root {
    overflow: auto;
    background-color: whitesmoke;
  }

  
  ul#menu {
    width: 100%;
    display: inline-block;
  }

  .menu_my_networks {
    /*line-height: 40px;*/
    display: inline-block;
    width: 100%;
    color: white;
    height: 100%;
    background-color: #0f62fe;
  }
  .menu_my_networks_open {
    /*line-height: 40px;*/
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
    position: relative;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    height: 2.5rem;
    background-color: grey;
    color: white;
    padding: 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;

  }

  .btn_networks_list_import {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .networks_list_items {
    position: relative;
    top: 2.5rem;
    height: var(--height);
    left: 0;
    right: 0;
    bottom: 0;
    overflow-y: auto;
  }

  .InnerContainer{
    max-height: 1000px; /* set the max-height of the inner div */
  }

  .OuterContailer{
    overflow: auto;
    width: 100%;
  }

  .mainUI{
    height: 100%;
  }
  

</style>
