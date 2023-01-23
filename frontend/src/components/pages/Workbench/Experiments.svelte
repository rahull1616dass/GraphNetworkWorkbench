<script lang="ts">
  import { networksList, selectedNetworkIndex } from "../../../stores"
  import { Dropdown, ProgressBar } from "carbon-components-svelte"
  import { ProgressBarData } from "../../../definitions/progressBarData"
  import NetworkListItem from "../../common/NetworkListItem.svelte"
  import { Task } from "../../../definitions/task"
  import { TaskType } from "../../../definitions/taskType"
  import { setExperimentTask, getExperimentTasks } from "../../../api/firebase"
  import CustomButton from "../../common/CustomButton.svelte"

  export let index: number = undefined
  let placeholder: string = "Please select a network from the list"

  // These values should be set by UI Elements later on
  let trainPercentage: number = 0.8
  let epochs: number = 10

  let progressBarData: ProgressBarData = new ProgressBarData(
    false,
    "Training..."
  )

  function selected(event) {
    $selectedNetworkIndex = event.detail.selectedIndex
  }

  async function createTask() {
    const taskToBeCreated = new Task(
      undefined, // This will be set by the backend
      TaskType.NODE_CLASSIFICATION,
      trainPercentage,
      epochs
    )
    const networkId = $networksList[$selectedNetworkIndex].metadata.id
    await getExperimentTasks(networkId)
      .then((tasks) => {
        console.log("Tasks", tasks)
        tasks.forEach((task) => {
          if (task.equals(taskToBeCreated)) {
            console.log("Task already exists")
            return
          }
        })
        setTaskDocument(networkId, taskToBeCreated)
      })
      .catch((error) => {
        console.log("Error getting tasks list", error)
      })
  }

  async function setTaskDocument(
    networkId: string,
    taskToBeCreated: Task
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      setExperimentTask(networkId, taskToBeCreated)
        .then((task) => {
          console.log("Task created", task)
          resolve()
        })
        .catch((error) => {
          console.log("Error creating task", error)
          reject()
        })
    })
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- <div class="dropdown" on:click={() => { $selectedNetworkIndex = index}}>
    <Dropdown
    label={placeholder}
      selectedId="0"
      items={[]}
    />
    </div> -->

<div class="dropdown">
  <!-- Until the firebase issues are solved we will not do anything when the selected item is changed -->
  <select class="selectDropdown" bind:value={index}>
    <!-- <select bind:value={index}> -->

    {#if placeholder}
      <option>{placeholder}</option>
    {/if}
    {#each $networksList as network, index}
      <option
        class="optionDropdown"
        value={index}
        on:click={() => {
          selected
        }}
      >
        {network.metadata.name} --- Nodes: {network.nodes.length} , Edges: {network
          .links.length}
      </option>
    {/each}
  </select>

  <!-- <p>
	Selected {JSON.stringify(index)} -----
    {$selectedNetworkIndex} -----
     {JSON.stringify($networksList)} 
    
</p> -->
</div>

<hr />

<div>hello</div>

{#if progressBarData.isPresent}
  <ProgressBar helperText={progressBarData.text} />
{:else}
  <CustomButton inverse={false} on:click={() => createTask()}>Create Task</CustomButton>
{/if}

<div
  class="networks_list_items"
  style="--height: {$networksList.length * 120}px;"
>
  {#each $networksList as network, index}
    <NetworkListItem
      {network}
      {index}
      selected={$selectedNetworkIndex == index}
      on:selectItem={(event) => {
        $selectedNetworkIndex = event.detail.selectedIndex
      }}
    />
  {/each}
</div>

<style lang="scss">
  .train_box {
    width: 100%;
    height: 100%;
    background-color: #f5f5f5;
    border-radius: 5px;
    padding: 10px;
    margin: 10px;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
    margin: 10px;
    &.selected {
      background-color: #e5e5e5;
    }
  }
  .dropdown {
    position: flex;
    width: 50%;
    background-color: var(--wueblue);
    margin-left: 25%;
    margin-top: 1%;
  }
  .selectDropdown {
    width: 95%;
    height: 100%;
    font-family: var(font-family);
    font-size: 16px;
    font-weight: 800;
    color: var(--lightblack);
    color-scheme: #4a4a56;
    background-color: white;
    padding: 1%;
    margin: 2%;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out;
  }
  .optionDropdown {
    font-family: var(font-family);
    font-size: 14px;
    font-weight: 500;
    color: var(--lightblack);
    color-scheme: #4a4a56;
    background-color: white;
    cursor: pointer;
    cursor:hover {
      background-color: red;
    }
  }
  hr {
    display: block;
    margin: 1em;
    width: 90%;
    content: "";
    margin-left: 5%;
    background-color: whitesmoke;
  }

  option:hover {
    background-color: yellow;
  }
</style>
