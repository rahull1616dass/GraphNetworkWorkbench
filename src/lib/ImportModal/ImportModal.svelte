<script lang="ts">
    import { Modal } from "carbon-components-svelte"
    import { ImportModalType } from "./ImportModalType"
    export let open: boolean = false
    export let clickedImport: ImportModalType
</script>

{#if open}
<Modal
  bind:open
  modalHeading="Uploading graph data. Which way would you like to continue?"
  primaryButtonText="From the web"
  secondaryButtonText="Upload"
  on:click:button--primary={() => {
      open = false
     clickedImport = ImportModalType.FROM_WEB
  }}
  on:click:button--secondary={() => {
    open = false
   clickedImport = ImportModalType.UPLOAD
}}
  on:open
  on:close
  on:submit>
  <p>Select how you would like to import your data</p>
</Modal>
{/if}
