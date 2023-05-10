<script lang="ts">
  import { networksList, selectedNetworkIndex } from "../../stores"
  import { DropdownSelectorType } from "../../definitions/dropdownSelectorType"
  import { MLModelType } from "../../definitions/mlModelType"
  import { TaskType } from "../../definitions/taskType"
  import { createEventDispatcher } from "svelte"

  const dispatch = createEventDispatcher<{
  modelChange: MLModelType;
  taskChange: TaskType;
  columnChange: string;
  'update:model': MLModelType;
  'update:task': TaskType;
  'update:y_column': string;
}>();


  export let placeholder: string = "Select one of the following"
  export let type: DropdownSelectorType = undefined
  export let selectedModel: MLModelType | undefined = undefined;

  let modelTypes: MLModelType[] = [
    MLModelType.TAGCONV,
    MLModelType.SGCONV,
    MLModelType.GATCONV,
    MLModelType.GCNCONV,
    MLModelType.SAGECONV,
  ]

  let taskTypeDictionary: Record<string, TaskType> = {
    "Node Classification": TaskType.NODE_CLASSIFICATION,
    "Edge Prediction": TaskType.EDGE_PREDICTION,
  }
  // remove the is_train column from the nodeColumns array
  $: nodeColumns = Object.keys(
    $networksList[$selectedNetworkIndex].nodes[0]
  ).filter((nodeColumns) => nodeColumns !== "is_train")

  let networkIndex: number = $selectedNetworkIndex
  let task: TaskType
  let model: MLModelType
  let y_column: string = undefined

  function handleModelChange(event: Event) {
  const target = event.target as HTMLSelectElement;
  selectedModel = target.value as MLModelType;
  dispatch("modelChange", selectedModel);
  dispatch("update:model", selectedModel);
}

function handleTaskChange(event: Event) {
  const target = event.target as HTMLSelectElement;
  task = target.value as TaskType;
  dispatch("taskChange", task);
  dispatch("update:task", task);
}

function handleColumnChange(event: Event) {
  const target = event.target as HTMLSelectElement;
  y_column = target.value;
  dispatch("columnChange", y_column);
  dispatch("update:y_column", y_column);
}
</script>

{#if type === DropdownSelectorType.NETWORK}
  <div>
    <select
      class="select"
      bind:value={networkIndex}
      on:change={() => ($selectedNetworkIndex = networkIndex)}
    >
      <!-- <option disabled selected>{placeholder}</option> -->
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
    <select class="select" bind:value={model} on:change={handleModelChange}>
      <option class="placeholder" value={undefined} disabled selected
        >{placeholder}</option
      >
      {#each modelTypes as model}
        <option class="optionDropdown" value={model}>
          {model}
        </option>
      {/each}
    </select>
  </div>
{:else if type === DropdownSelectorType.TASK}
  <div>
    <select class="select" bind:value={task} on:change={handleTaskChange}>
      <option class="placeholder" disabled selected>{placeholder}</option>
      {#each Object.entries(taskTypeDictionary) as [readableString, taskId]}
        <option class="optionDropdown" value={taskId}>
          {readableString}
        </option>
      {/each}
      <!-- {#each Object.entries(taskTypes) as [task, value]}
        <option class="optionDropdown" value={task}>
          {value}
        </option>
      {/each} -->
    </select>
  </div>
{:else if type === DropdownSelectorType.Y_COLUMN}
  <div>
    <select class="select" bind:value={y_column} on:change={handleColumnChange}>
      <option class="placeholder" value={undefined}>{placeholder}</option>
      {#each nodeColumns as column}
        <option class="optionDropdown" value={column}>
          {column}
        </option>
      {/each}
    </select>
  </div>
{/if}

<style lang="scss">
  .placeholder {
    color: #ddd;
  }
  .select {
    width: 60%;
    height: 100%;
    font-family: var(font-family);
    font-size: 14px;
    font-weight: 400;
    background-color: white;
    padding: 1%;
    margin: 2%;
    cursor: pointer;
    border-radius: 1px;
    border-color: whitesmoke;
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
