<script lang="ts">
  import { Modal, Form, TextInput } from "carbon-components-svelte"
  import { createEventDispatcher } from "svelte"
  import { Node } from "../../../../definitions/network"
  import CustomModal from "../../../common/CustomModal.svelte";
  import CustomButton from "../../../common/CustomButton.svelte";

  export let modalProps: any = undefined
  export let open: boolean = false
  let node: Node = undefined
  let textInputs = new Node()
  const dispatch = createEventDispatcher()

  // Log the result when modalProps is updated
  $: {
    if (modalProps != undefined) {
      console.log("modalProps", modalProps)
      node = new Node(
        modalProps.name,
        modalProps.id,
        modalProps.group,
        modalProps.index,
        modalProps.pos
      )
      console.log("node", node)
    }
  }
</script>

<!-- <main>
  {#if node != undefined}
    <Modal
      modalHeading="Node Details"
      bind:open
      size="sm"
      preventCloseOnClickOutside
      primaryButtonText="Update Node"
      secondaryButtonText="Cancel"
      on:click:button--primary={() => {
        console.log("textInputs", textInputs)
        node.name = textInputs.name
        dispatch("updateNode", { newNode: node })
        open = false
      }}
      on:click:button--secondary={() => {
        open = false
      }}
    >
      <Form>
        {#each Object.keys(node) as key}
          <TextInput
            labelText={key}
            value={node[key]}
            on:input={(e) => {
              console.log("input: ", e)
              textInputs[key] = e.detail
            }}
            type="text"
            id={key}
          />
        {/each}
      </Form>
    </Modal>
  {/if}
</main> -->

{#if node != undefined}
  <CustomModal on:close="{() => open = false}">
    <h4 slot="header">
      Node Details
    </h4>
    <div slot="body">
      <Form>
        {#each Object.keys(node) as key}
          <TextInput
            labelText={key}
            value={node[key]}
            on:input={(e) => {
              console.log("input: ", e)
              textInputs[key] = e.detail
            }}
            type="text"
            id={key}
          />
        {/each}
      </Form>
    </div>

    <div slot="footer">
      <CustomButton type={"secondary"} inverse={false} on:click={() => {
        open = false
      }}>
        Update Node
      </CustomButton>

    </div>

  </CustomModal>

{/if}

<style>
</style>
