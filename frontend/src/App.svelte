<script lang="ts">
  import { MenuItem } from "./definitions/menuItem";
  import NetworkListItem from "./components/common/NetworkListItem.svelte";
  import Home from "./components/pages/Home.svelte";
  import Plot from "./components/pages/Workbench/Plot/Plot.svelte";
  import Register from "./components/pages/Register.svelte";
  import Login from "./components/pages/Login.svelte";
  import Profile from "./components/pages/Profile.svelte";
  import Experiments from "./components/pages/Workbench/Experiments.svelte";
  import Reports from "./components/pages/Workbench/Reports.svelte";
  import FromWeb from "./components/pages/AddNetwork/FromWeb.svelte";
  import UploadNetwork from "./components/pages/AddNetwork/UploadNetwork/UploadNetwork.svelte";
  import Footer from "./components/common/Footer.svelte";
  import Tabs from "./components/common/Tabs.svelte";
  import Test from "./components/pages/Test.svelte";
  import Networks from "./components/pages/Workbench/Networks.svelte";
  import {
    selectedMenuItem,
    authUserStore,
    loginUserStore,
    networksList,
    selectedNetworkIndex,
    fetchedNetworkOnce,
    defaultSeed,
  } from "./stores";
  import { getAuth } from "firebase/auth";
  import {
    loginUser,
    getNetworks as getNetworksFromFirestore,
    setDefaultSeed,
    getAppConfig
  } from "./api/firebase";
  import { ProgressBarData } from "./definitions/progressBarData";
  import { ProgressBar, Button } from "carbon-components-svelte";
  import { onMount } from "svelte";
  import ImportModal from "./components/common/ImportModal.svelte";
  import { ImportModalType } from "./definitions/importModalType";
  import { fly, fade } from "svelte/transition";

  /* ---- PAGE LOAD AND LOGIN ---- */
  let progressBarData: ProgressBarData = new ProgressBarData(
    true,
    "Loading..."
  );
  let isLoggedIn: boolean = false;

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
          console.log(error);
          progressBarData.isPresent = false;
        });
    } else progressBarData.isPresent = false;
  });

  // Should update after the user manually logins or registers
  $: $authUserStore, checkForLoggedIn();

  function checkForLoggedIn() {
    isLoggedIn = $authUserStore !== undefined; //&& getAuth().currentUser !== null
    if (isLoggedIn && $networksList.length === 0) {
      progressBarData.text = "Fetching networks...";
      if ($fetchedNetworkOnce) return;
      $fetchedNetworkOnce = true;
      getNetworksFromFirestore().finally(() => {
        $networksList = $networksList.sort((a, b) => {
          if (a.name < b.name) return -1
          else if (a.name > b.name) return 1
          else return 0
        });
        progressBarData.isPresent = false;
      })
      setDefaultSeed()
      getAppConfig()
    }
  }
</script>

<div class="main">
  {#if progressBarData.isPresent}
    <div class="main_progress_bar">
      <ProgressBar helperText={progressBarData.text} />
    </div>
  {:else if isLoggedIn === true}
    <ul id="menuLogin" class="menuLogin">
      <Tabs />
      <div class="content">
        {#if $selectedMenuItem === MenuItem.HOME}
          <Home />
        {:else if $selectedMenuItem === MenuItem.NETWORKS}
          <Networks />
        {:else if $selectedMenuItem === MenuItem.PLOT}
          <Plot />
        {:else if $selectedMenuItem === MenuItem.EXPERIMENTS}
          <Experiments />
        {:else if $selectedMenuItem === MenuItem.REPORTS}
          <Reports />
        {:else if $selectedMenuItem === MenuItem.PROFILE}
          <Profile />
        {:else if $selectedMenuItem === MenuItem.FROM_WEB}
          <FromWeb />
        {:else if $selectedMenuItem === MenuItem.FROM_PC}
          <UploadNetwork />
        {:else if $selectedMenuItem === MenuItem.TEST}
          <Test />
        {/if}
      </div>
    </ul>
  {:else if isLoggedIn === false}
    <ul>
      <Tabs />
      <div class="content">
        {#if $selectedMenuItem === MenuItem.HOME}
          <Home />
        {:else if $selectedMenuItem === MenuItem.LOGIN}
          <Login />
        {:else if $selectedMenuItem === MenuItem.REGISTER}
          <Register />
        {/if}
      </div>
    </ul>
  {/if}
  <div class="footer-container">
    <Footer />
  </div>
</div>

<style lang="scss">
  .footer-container {
    width: 100%;
    margin-top: auto;
  }
  .main {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  .content {
    padding-top: 70px;
    padding-bottom: 70px;
    flex: 1;
  }
  .menuLogin {
    height: 100%;
  }
  .main_progress_bar {
    position: relative;
    display: flex;
    height: 100%;
    width: 100%;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: center;
    align-items: center;
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

  .mainUI {
    height: 100%;
  }
</style>
