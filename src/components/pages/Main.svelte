<script lang="ts">
  import ImportModal from "./ImportModal.svelte"
  import { ImportModalType } from "../../definitions/importModalType"
  import FromWeb from "./FromWeb.svelte"
  import UploadNetwork from "./UploadNetwork/UploadNetwork.svelte"
  import { testStoreValue } from "../../stores"
  import { getAuth } from "firebase/auth"
  import { userStore } from "../../stores"

  let isLoggedIn: boolean = false
  $: isLoggedIn = $userStore !== undefined && getAuth().currentUser !== null

  let isImportModalOpen: boolean = false
  let selectedImportType: ImportModalType = ImportModalType.NONE
</script>

<main>
  <!--
    <div>
      <a href="https://vitejs.dev" target="_blank"> 
        <img src="/vite.svg" class="logo" alt="Vite Logo" />
      </a>
      <a href="https://svelte.dev" target="_blank"> 
        <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
      </a>
    </div>
    <h1>Vite + Svelte</h1>
  
    <div class="card">
      <Counter />
    </div>
  
    <p>
      Check out <a href="https://github.com/sveltejs/kit#readme" target="_blank">SvelteKit</a>, the official Svelte app framework powered by Vite! Test
    </p>
    <p>
      Hello World!
    </p>
  
    <p class="read-the-docs">
      Click on the Vite and Svelte logos to learn more
    </p>
    -->
  <div class="loggedInText">
    {#if isLoggedIn}
      Logged In as {$userStore.email}
    {/if}
  </div>
  {#if selectedImportType === ImportModalType.NONE}
    <button on:click={() => (isImportModalOpen = !isImportModalOpen)}
      >Add Data</button
    >
    <ImportModal bind:selectedImportType bind:open={isImportModalOpen} />
    <p>Selected import method is {selectedImportType}</p>
    <p>Imported store value is = {$testStoreValue}</p>
    <button on:click|preventDefault={() => ($testStoreValue += "!")}
      >Change store value</button
    >
  {:else if selectedImportType === ImportModalType.FROM_WEB}
    <FromWeb />
  {:else if selectedImportType === ImportModalType.UPLOAD}
    <UploadNetwork />
  {/if}
</main>

<style>
  .loggedInText {
    color: red;
    margin: 10px;
  }
</style>
