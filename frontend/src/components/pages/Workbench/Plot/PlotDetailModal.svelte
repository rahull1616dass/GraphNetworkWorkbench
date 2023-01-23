<script lang="ts">
  import { Form, TextInput, Dropdown } from "carbon-components-svelte"
  import { createEventDispatcher } from "svelte"
  import { Node, Link } from "../../../../definitions/network"
  import CustomModal from "../../../common/CustomModal.svelte"
  import CustomButton from "../../../common/CustomButton.svelte"
  import type { DropdownItem } from "carbon-components-svelte/types/Dropdown/Dropdown.svelte"
  export let open: boolean = false
  export let detailedItem: Node | Link = undefined

  /*
   It is necessary to keep track of this if the user is updating the edges. This way,
   a dropdown can be used to select the source and target nodes.
  */
  export let existingNodes: Node[] = []
  let dropdownItems: DropdownItem[] = []
  if (existingNodes.length > 0) {
    dropdownItems = existingNodes.map((node) => {
      return { id: node.index, text: node.name }
    })
  }

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
          {#if detailedItem instanceof Node}
            <TextInput
              labelText={key}
              value={detailedItem[key]}
              on:input={(e) => {
                console.log("input: ", e)
                detailedItem[key] = isNaN(Number(e.detail))
                  ? e.detail
                  : Number(e.detail)
              }}
              type="text"
              id={key}
            />
          {:else if key === "source" || key === "target"}
            <Dropdown
              titleText={key}
              selectedId={dropdownItems.find(
                (item) => item.text === detailedItem[key]
              ).id}
              items={dropdownItems}
              on:select={(e) => {
                console.log(
                  `For ${key}, selected item: ${e.detail.selectedItem.text}`
                )
                detailedItem[key] = e.detail.selectedItem.text
              }}
            />
          {:else}
            <TextInput
              labelText={key}
              value={detailedItem[key]}
              on:input={(e) => {
                console.log("input: ", e)
                detailedItem[key] = isNaN(Number(e.detail))
                  ? e.detail
                  : Number(e.detail)
              }}
              type="text"
              id={key}
            />
          {/if}
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
