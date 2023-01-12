<script lang="ts">
    // import { Modal } from "carbon-components-svelte"
    import { ImportModalType } from "../../definitions/importModalType"
    import CustomModal from "./CustomModal.svelte";
    import CustomButton from "./CustomButton.svelte";
    export let open: boolean = false
    export let selectedImportType: ImportModalType
</script>

{#if open}
  <CustomModal on:close="{() => open = false}">
    <h4 slot="header">
      Uploading graph data. Which way would you like to continue?
    </h4>
    <div slot="body">
      <p>Select how you would like to import your data</p>
    </div>

    <div slot="footer">
      <CustomButton type={"primary"} inverse={true} on:click={() => {
        open = false
        selectedImportType = ImportModalType.FROM_WEB
      }}>
        From Web
      </CustomButton>

      <CustomButton type={"secondary"} inverse={false} on:click={() => {
        open = false
        selectedImportType = ImportModalType.UPLOAD
      }}>
        From PC
      </CustomButton>

      <!-- <CustomButton type={"delete"} on:click={close}>close modal</CustomButton> -->


    </div>

    
    

  </CustomModal>

{/if}

  <style lang="scss">
    p {
      color: var(--lightblack);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;;
      font-weight: 400;
    }
    h4 {
      color: var(--lightblack);
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;;
      font-weight: 600;
    }
  </style>

