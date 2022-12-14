<script lang="ts">
  import ImportModal from "./AddNetwork/ImportModal.svelte"
  import { ImportModalType } from "../../definitions/importModalType"
  import FromWeb from "./AddNetwork/FromWeb.svelte"
  import UploadNetwork from "./AddNetwork/UploadNetwork/UploadNetwork.svelte"
  import { testStoreValue } from "../../stores"
  import { getAuth } from "firebase/auth"
  import { authUserStore, selectedMenuItem } from "../../stores"
  import HomeVisSpec from "../../data/HomeVisSpec"
  import MiserablesData from "../../data/MiserablesVisSpec"
  import { default as vegaEmbed } from "vega-embed"
  import { MenuItem } from "../../definitions/menuItem"

  let isLoggedIn: boolean = false
  $: isLoggedIn = $authUserStore !== undefined && getAuth().currentUser !== null

  let isImportModalOpen: boolean = false
  let selectedImportType: ImportModalType = ImportModalType.NONE

  vegaEmbed("#viz", HomeVisSpec, { actions: false })
</script>

<main>
  <h1>Welcome to Graph Learning Workbench</h1>
  <div class="loggedInText">
    {#if isLoggedIn}
      Logged In as {$authUserStore.email}
      {#if selectedImportType === ImportModalType.NONE}
        <button
          class="buttons"
          on:click={() => (isImportModalOpen = !isImportModalOpen)}
          >Add Network</button
        >
        <ImportModal bind:selectedImportType bind:open={isImportModalOpen} />
      {:else if selectedImportType === ImportModalType.FROM_WEB}
        <FromWeb />
      {:else if selectedImportType === ImportModalType.UPLOAD}
        <UploadNetwork />
      {/if}
    {:else}
      <div class="buttons">
        <button on:click={() => ($selectedMenuItem = MenuItem.LOGIN)}
          >Login</button
        >
        <!-- <button on:click={() => ($selectedMenuItem = MenuItem.REGISTER)}
          >Register</button>-->
      </div>
    {/if}
  </div>
  <div class="viz" id="viz" />
</main>

<style lang="scss">
  .buttons {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 1;
    transform: translate(-50%, -50%);
  }

  .viz {
    width: 100%;
    height: 100%;
    position: relative;
    opacity: 0.5;
  }

  .loggedInText {
    color: red;
    margin: 10px;
  }
</style>
