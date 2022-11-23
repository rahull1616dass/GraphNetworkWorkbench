<script lang="ts">
  import { Modal, Form, TextInput } from "carbon-components-svelte"
    import { text } from "svelte/internal"
  import { Node } from "../../definitions/network"
  export let modalProps: any = undefined
  export let open: boolean = false
  export let node: Node = undefined
  let textInputValues: Node = new Node()

  $: modalProps, () => {
    textInputValues = new Node(
      modalProps.name,
      modalProps.id,
      modalProps.group,
      modalProps.index,
      modalProps.pos
    )
  }
</script>

<main>
 
    <Modal
      passiveModal
      bind:open
      modalHeading="Vega Node #{modalProps['Symbol(vega_id)']}"
      on:close={() => (open = false)}
      primaryButtonText="Update Node Details"
      on:click:button--primary={() => {
        open = false
        node = textInputValues
    }}
    >
      <Form>
        {#each Object.keys(textInputValues) as key}
          <TextInput
            labelText={key}
            bind:value={textInputValues[key]}
            type="text"
            id={key}
          />
        {/each}
      </Form>
    </Modal>

</main>

<style>
</style>
