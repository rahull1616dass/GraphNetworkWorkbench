<script lang="ts">
  import { Form, TextInput } from "carbon-components-svelte"
  import { createEventDispatcher } from "svelte"
  import { Node, Link } from "../../../../definitions/network"
  import CustomModal from "../../../common/CustomModal.svelte"
  import CustomButton from "../../../common/CustomButton.svelte"
  import { unchangeableAttributes } from "../../../../stores"

  export let open: boolean = false
  export let detailedItem: Node | Link = undefined

  const dispatch = createEventDispatcher()
</script>

{#if detailedItem != undefined}
  <CustomModal on:close={() => (open = false)}>
    <h4 slot="header">
      {detailedItem instanceof Node ? "Node Details" : "Edge Details"}
    </h4>
    <div slot="body">
      <Form>
        {#each Object.keys(detailedItem) as key}
            <TextInput
              labelText={key}
              value={detailedItem[key]}
              disabled={$unchangeableAttributes.includes(key)}
              on:input={(e) => {
                console.log("input: ", e)
                detailedItem[key] = isNaN(Number(e.detail))
                  ? e.detail
                  : Number(e.detail)
              }}
              type="text"
              id={key}
            />
        {/each}
      </Form>
    </div>

    <div slot="footer">
      <CustomButton
        type={"secondary"}
        inverse={false}
        on:click={() => {
          dispatch("updateItem", { updatedItem: detailedItem })
          open = false
        }}
      >
        {detailedItem instanceof Node ? "Update Node" : "Update Edge"}
      </CustomButton>
    </div>
  </CustomModal>
{/if}

<style>
</style>
