<!--
    An accordion that when opened, fetches its content from a URL.
-->
<script lang="ts">
  import { AccordionItem, Button } from "carbon-components-svelte"
  import request from "../../api/request"
  import { createEventDispatcher } from "svelte"

  export let title: string
  export let endpoint: string
  let content = undefined

  const dispatch = createEventDispatcher()

  const onAccordionClick = async (event: MouseEvent) => {
    if (content == undefined) {
      content = await request(endpoint)
    }
    console.log(content.description)
  }
</script>

<AccordionItem
  on:click={(e) => {
    onAccordionClick(e)
  }}
  bind:title
>
  {#if content}
    <div class="root">
      <div class="content">
        <b>Title:</b>
        {content.title} <br />
        <b>Description:</b>
        {content.description}
      </div>
      <div class="import_button">
        <Button
          on:click={() => dispatch("fetchNetwork", { networkName: title })}
          size="small"
          on:click>Import Network</Button
        >
      </div>
    </div>
  {:else}
    <p>Fetching content...</p>
  {/if}
</AccordionItem>

<style lang="scss">
  .content {
    text-align: left;
    padding: 1rem;
  }

  .import_button {
    right: 0;
    margin: 1rem;
  }
</style>
