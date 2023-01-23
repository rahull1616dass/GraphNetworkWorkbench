<script lang="ts">
  import { Dropdown, ProgressBar } from "carbon-components-svelte"
  import { ProgressBarData } from "../../../definitions/progressBarData"
  import { Task } from "../../../definitions/task"
  import { TaskType } from "../../../definitions/taskType"
  import { setExperimentTask, getExperimentTasks } from "../../../api/firebase"
  import CustomButton from "../../common/CustomButton.svelte"
  import { MLModelType } from "../../../definitions/mlModelType";
  import { networksList, selectedNetworkIndex, selectedModelType } from "../../../stores";

  export let networkIndex: number = undefined
  let placeholderNetwork: string = "Please select a network from the list"
  let placeholderModel: string = "Please select a model from the list"

  // These values should be set by UI Elements later on
  let trainPercentage: number = 0.8
  let epochs: number = 10

  let progressBarData: ProgressBarData = new ProgressBarData(
    false,
    "Training..."
  )

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
  let modelTypes: MLModelType[] = [MLModelType.GCN, MLModelType.DeepWalk, MLModelType.GIN]

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


<div class="dropdown">

<select class="selectNetwork" bind:value={networkIndex}>
    {#if placeholderNetwork}
    <option >{placeholderNetwork}</option>
    {/if}
    {#each $networksList as network, networkIndex}
        <option class="optionDropdown" value={networkIndex} on:click={() => $selectedNetworkIndex=networkIndex}>
            {network.metadata.name} ---
            Nodes: {network.nodes.length} , Edges: {network.links.length} 
        </option>
    {/each}
      
</select>

</div>

<hr/>

<div class="Model">

    <div>
        <select class="selectModel" >
            {#if placeholderModel}
            <option >{placeholderModel}</option>
            {/if}
            {#each modelTypes as model}
                <option class="optionDropdown" value={model} on:click={() => $selectedModelType=model}>
                    {model} 
                </option>
            {/each}
        </select>
    </div>
    

    <div>
        Configurable Parameters:
    </div>

</div>

<hr />

<div>hello</div>

{#if progressBarData.isPresent}
  <ProgressBar helperText={progressBarData.text} />
{:else}
  <CustomButton inverse={false} on:click={() => createTask()}>Create Task</CustomButton>
{/if}


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
    }
    .dropdown {
        position: flex;
        width: 50%;
        background-color: whitesmoke;
        margin-left: 25%;
        margin-top: 1%;
    }
    .Model {
        position: center;
        width: 50%;
        margin-left: 1%;
        margin-top: 1%;
        border-radius: 5px;
        border: #4a4a56 4px solid;
    }
    .selectNetwork {
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
    .selectModel {
        width: 50%;
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
