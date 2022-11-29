<script lang="ts">
  import { Modal, Form, TextInput } from "carbon-components-svelte"
  import { createEventDispatcher } from "svelte"
  import { Node } from "../../../definitions/network"
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

<main>
  {#if node != undefined}
    <p>{node.name}</p>
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
      <button on:click={() => {
        console.log("textInputs", textInputs)
        node.name = textInputs.name
        dispatch("updateNode", { newNode: node })}
        }>Update Node</button>
  {/if}
</main>

<style>
</style>
