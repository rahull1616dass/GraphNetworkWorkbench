<script lang="ts">
  import { MenuItem } from "./definitions/menuItem"
  import Home from "./components/pages/Home.svelte"
  import Plot from "./components/pages/Plot/Plot.svelte"
  import Register from "./components/pages/Register.svelte"
  import Login from "./components/pages/Login.svelte"
  import { ProgressBar } from "carbon-components-svelte"
  import {
    selectedMenuItem,
    authUserStore,
    loginUserStore,
    networksList,
  } from "./stores"
  import { getAuth } from "firebase/auth"
  import {
    loginUser,
    getNetworks as getNetworksFromFirestore,
  } from "./api/firebase"
  import { ProgressBarData } from "./definitions/progressBarData"


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
  }else progressBarData.isPresent = false

  // Should update after the user manually logins or registers
  $: $authUserStore, checkForLoggedIn()

  function checkForLoggedIn() {
    isLoggedIn = $authUserStore !== undefined && getAuth().currentUser !== null
    if (isLoggedIn && $networksList.length === 0) {
      progressBarData.text = "Fetching networks..."
      getNetworksFromFirestore()
        .then(() =>  progressBarData.isPresent = false)
        .catch(() => progressBarData.isPresent = false)
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
</script>

{#if progressBarData.isPresent}
  <div class="main_progress_bar">
    <ProgressBar helperText={progressBarData.text} />
  </div>

{:else}
  <ul id="menu">
    {#if isLoggedIn}
      <li>
        <a href="/" on:click|preventDefault={performLogout}>Logout</a>
      </li>
    {:else}
      <li>
        <a
          href="/"
          on:click|preventDefault={() => ($selectedMenuItem = MenuItem.LOGIN)}
          >Login</a
        >
      </li>
      <li>
        <a
          href="/"
          on:click|preventDefault={() =>
            ($selectedMenuItem = MenuItem.REGISTER)}>Register</a
        >
      </li>
    {/if}

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
      <Home />
    {:else if $selectedMenuItem === MenuItem.LOGIN}
      <Login />
    {:else if $selectedMenuItem === MenuItem.REGISTER}
      <Register />
    {:else if $selectedMenuItem === MenuItem.PLOT}
      <Plot />
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
  ul#menu {
    width: 100%;
    display: inline-block;
  }
</style>
