<script lang="ts">
  import ImportModal from "../common/ImportModal.svelte"
  import CustomButton from "../common/CustomButton.svelte"
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
  
  <div class="loggedInText">
    {#if isLoggedIn}
      <!---Logged In as {$authUserStore.email}--->
      {#if selectedImportType === ImportModalType.NONE}
        <div class="viz" id="viz" />
        <div> <ImportModal bind:selectedImportType bind:open={isImportModalOpen} /> </div>
        
        <div class="addNetworkButton">
        <CustomButton type={"secondary"} inverse={false}
          on:click={() => (isImportModalOpen = !isImportModalOpen)}
          >Add Network</CustomButton>

          

        </div>
      {:else if selectedImportType === ImportModalType.FROM_WEB}
        <FromWeb />
      {:else if selectedImportType === ImportModalType.UPLOAD}
        <UploadNetwork />
      {/if}
    {:else}
    <h1>Welcome to Graph Learning Workbench</h1>
      <div class="viz" id="viz" />
      <div class="loginButton">
        <CustomButton type={"secondary"} on:click={() => ($selectedMenuItem = MenuItem.LOGIN)}
          >Login</CustomButton>
          
        <!-- <button on:click={() => ($selectedMenuItem = MenuItem.REGISTER)}
          >Register</button>-->
      </div>
    {/if}
  </div>
  <!--- <div class="viz" id="viz" /> -->
</main>

<style lang="scss">
  h1{
    width: 100%;
    height: 100%;
    color: #063d79;
    font-weight: 500;
    animation: splash 1s normal forwards ease-in-out;
    border: 10px solid #d8dadc;
    /*animation: mymove 5s bounce;*/
    padding-top: 2%;
    padding-bottom: 2%;
    
  }

  @keyframes splash {
    from {
        opacity: 0;
        transform: scale(0, 0);
    }
    50% {
        opacity: 1;
        transform: scale(1.1, 1.1);
    }
    to {
        transform: scale(1, 1);
    }
  }

  div {
    padding-top: 2%;

  }
  .loginButton {
    font-size: 150%;
    position: flex;
    margin-top: 4%;
    margin-left: 50%;
    z-index: 1;
    transform: translate(-50%, -50%);
  }

  .addNetworkButton {
    /*background-color: #f7f7f8;*/
    /*color: #063d79;*/
    position: flex;
    margin-left: 50%;
    font-size: 150%;
    z-index: 1;
    transform: translate(-50%, -50%);
  }

  .viz {
    width: 100%;
    height: 100%;
    position: relative;
    opacity: 0.7;
  }

  .loggedInText {
    color: #aaa;
    margin: 10px;
  }
</style>
