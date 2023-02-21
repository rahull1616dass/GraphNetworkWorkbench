<!--
    An accordion that when opened, fetches its content from a URL.
-->
<script lang="ts">
  import { AccordionItem, Button } from "carbon-components-svelte"
  import request from "../../api/request"
  import { createEventDispatcher } from "svelte"
  import { getAuth } from "firebase/auth"  
  import { checkIfNetworkExistTask, getExperimentTasks } from "../../api/firebase"


  export let title: string
  export let endpoint: string
  let content = undefined
  export let isNetworkUploaded: boolean
  const dispatch = createEventDispatcher()

  const onAccordionClick = async (event: MouseEvent) => {
    isNetworkUploaded = await checkIfNetworkExistTask(title)

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
      {#if (isNetworkUploaded == true)}
      <Button
          on:click={() => {console.log('network imported');
          }}
          size="small"
        on:click>Network Imported</Button>
      {:else}
        <Button
          on:click={() => dispatch("fetchNetwork", { networkName: title, content: content })}
          size="small"
        on:click>Import Network</Button>
      {/if}
      
        
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
