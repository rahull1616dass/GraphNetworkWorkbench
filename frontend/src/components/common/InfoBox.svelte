<script>
  import CustomModal from "./CustomModal.svelte";
  import CustomButton from "./CustomButton.svelte";
  import ImageButton from "./ImageButton.svelte";
  import infoIcon from "../../assets/info.svg";

  export let isInfoModalOpen = false;
  export let headerText = undefined;
  export let bodyText = undefined;

</script>

<div class="infobox">
  <ImageButton styleClass="deleteButtonClass"
    on:click={() => {
      isInfoModalOpen = !isInfoModalOpen;
    }}
    defaultImageSource={infoIcon}
  />

  {#if isInfoModalOpen}
    <CustomModal
      on:close={() => {
        isInfoModalOpen = false;
      }}
    >
      <h4 slot="header">{headerText}</h4>
      <div slot="body">{bodyText}</div>
      <div slot="footer">
        <CustomButton type={"secondary"} inverse={false}
          on:click={() => {
            isInfoModalOpen = !isInfoModalOpen;
          }}
        >
          Got it!
        </CustomButton>
      </div>
    </CustomModal>
  {/if}
</div>

<style>
  .infobox {
    position: flex;
    margin: auto;
  }
</style>