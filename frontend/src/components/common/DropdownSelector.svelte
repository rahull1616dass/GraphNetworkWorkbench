<script lang="ts">
  import {
    networksList,
    selectedNetworkIndex,
    selectedModelType,
    selectedTaskType,
  } from "../../stores"
  import { DropdownSelectorType } from "../../definitions/dropdownSelectorType"
  import { MLModelType } from "../../definitions/mlModelType"
  import { TaskType } from "../../definitions/taskType"

  export let placeholder: string = "Select one of the following"
  export let type: DropdownSelectorType = undefined

  let modelTypes: MLModelType[] = [
    MLModelType.GCN,
    MLModelType.DeepWalk,
    MLModelType.GIN,
  ]
  let taskTypes: TaskType[] = [
    TaskType.NODE_CLASSIFICATION,
    TaskType.EDGE_PREDICTION,
  ]

  let nodeColumns: string[] = Object.keys(
    $networksList[$selectedNetworkIndex].nodes[0]
  )

  let networkIndex: number = undefined
  let task: TaskType
  let model: MLModelType
  let y_column: string = undefined
</script>

{#if type === DropdownSelectorType.NETWORK}
  <div>
    <select
      class="select"
      bind:value={networkIndex}
      on:click={() => ($selectedNetworkIndex = networkIndex)}
    >
      <option>{placeholder}</option>
      {#each $networksList as network, networkIndex}
        <option class="optionDropdown" value={networkIndex}>
          {network.metadata.name} --- Nodes: {network.nodes.length} , Edges: {network
            .links.length}
        </option>
      {/each}
    </select>
  </div>
{:else if type === DropdownSelectorType.MLMODEL}
  <div>
    <select
      class="select"
      bind:value={model}
      on:click={() => ($selectedModelType = model)}
    >
      <option>{placeholder}</option>
      {#each modelTypes as model}
        <option class="optionDropdown" value={model}>
          {model}
        </option>
      {/each}
    </select>
  </div>
{:else if type === DropdownSelectorType.TASK}
  <div>
    <select
      class="select"
      bind:value={task}
      on:click={() => ($selectedTaskType = task)}
    >
      <option>{placeholder}</option>
      {#each taskTypes as task, _}
        <option class="optionDropdown" value={task}>
          {task}
        </option>
      {/each}
    </select>
  </div>
{:else if type === DropdownSelectorType.Y_COLUMN}
  <div>
    <select class="select" bind:value={y_column}>
      <option>{placeholder}</option>
      {#each nodeColumns as column}
        <option class="optionDropdown" value={column}>
          {column}
        </option>
      {/each}
    </select>
  </div>
{/if}

<style lang="scss">
  .select {
    width: 60%;
    height: 100%;
    font-family: var(font-family);
    font-size: 16px;
    font-weight: 800;
    color: var(--wueblue);
    background-color: white;
    padding: 1%;
    margin: 2%;
    cursor: pointer;
    border-radius: 10px;
    box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.2);
  }

  .optionDropdown {
    font-family: var(font-family);
    font-size: 14px;
    font-weight: 500;
    color: var(--lightblack);
    background-color: white;
    cursor: pointer;
    cursor:hover {
      background-color: red;
    }
  }
</style>
