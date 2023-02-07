<script lang="ts">
  import { Dropdown, ProgressBar } from "carbon-components-svelte"
  import { ProgressBarData } from "../../../definitions/progressBarData"
  import { Task } from "../../../definitions/task"
  import { TaskType } from "../../../definitions/taskType"
  import { setExperimentTask, getExperimentTasks } from "../../../api/firebase"
  import CustomButton from "../../common/CustomButton.svelte"
  import { MLModelType } from "../../../definitions/mlModelType";
  import { networksList, selectedNetworkIndex, selectedModelType } from "../../../stores";
  import Plot from "./Plot/Plot.svelte"

  export let networkIndex: number = undefined
  let placeholderNetwork: string = "Select a network"
  let placeholderModel: string = "Select a model"

  // These values should be set by UI Elements later on
  let trainPercentage: number = 0.8
  let epochs: number = 100
  let learningRate: number = 0.01

  function handleEpoch(event) {
    epochs = event.target.value;
  }
  function handleLearningRate(event) {
    learningRate = event.target.value;
  }
  function handleTrainingPercentage(event) {
    trainPercentage = event.target.value;
  }
  

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

<div class="background">


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

<div>
<li class="Model">

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
    
    <hr/>

    <div>
        Configurable Parameters:
    </div>

    <div>
        <li>
            Epochs
        </li>
        <li class="range">
            <input type="range" min="0" max="1000" value="100" step="10" class="slider" on:input={handleEpoch}>
            {epochs}
        </li>
    </div>
    <div>
        <li>
            Learning Rate	
        </li>
        <li class="range">
            <input type="range" min="0.00" max="0.4" value="0.01" step="0.001" class="slider" on:input={handleLearningRate}>
            {learningRate}
        </li>
    </div>
    <div>
        <li>
            Training Percentage	
        </li>
        <li class="range">
            <input type="range" min="0" max="1" value="0.8" step="0.05" class="slider" on:input={handleTrainingPercentage}>
            {trainPercentage}
        </li>
    </div>

    <div class="createTask">
        {#if progressBarData.isPresent}
        <ProgressBar helperText={progressBarData.text} />
      {:else}
        <CustomButton 
        type={"secondary"} 
        inverse={false} 
        disabled={epochs === 0 || epochs === 1000 || learningRate === 0.00 || learningRate === 0.4 || trainPercentage === 0 || trainPercentage === 1} 
        on:click={() => createTask()}>Create Task</CustomButton>
      {/if}
    </div>

</li>

<li class="Modal">
   
</li>

</div>

<hr/>




</div>

<style lang="scss">
    .tooltip {
        // position: flex;
        // top: 55%;
        // left: 30%;
        // transform: translateX(-10%);
        // padding: 1px;
        // background-color: white;
        // border: 1px solid gray;
        // border-radius: 5px;
        z-index: 1;
    }
    .background {
        color: var(--wueblue);
        font-weight: 600;
    }	
    .range{
        width: 80%;
        margin-left: 2%;
        align-items: left;
    }
    .dropdown {
        position: flex;
        width: 50%;
        margin-left: 25%;
        margin-top: 1%;
        background-color: whitesmoke;
        border-radius: 15px;
        box-shadow: 1px 2px 3px rgba(0,0,0,0.1);
    }
    .Model {
        position: center;
        width: 35%;
        margin-left: 5%;
        margin-top: 1%;
        margin-bottom: 3%;
        border-radius: 15px;
        // border: whitesmoke 4px inset;
        box-shadow: 2px 3px 4px rgba(0,0,0,0.2);
        background-color: whitesmoke;
    }
    .selectNetwork {
        width: 95%;
        height: 100%;
        font-family: var(font-family);
        font-size: 16px;
        font-weight: 800;
        color: var(--lightblack);
        background-color: white;
        padding: 1%;
        margin: 2%;
        cursor: pointer;
        border-radius: 10px;
        box-shadow: 2px 3px 4px rgba(0,0,0,0.2);
    }
    .selectModel {
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
        box-shadow: 2px 3px 4px rgba(0,0,0,0.2);
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
    .slider {
        -webkit-appearance: none;  /* Override default CSS styles */
        appearance: none;
        width: 75%; /* Full-width */
        background: white; /* Grey background */
        opacity: 1; 
        -webkit-transition: .2s; 
        transition: opacity .2s;
        border-radius: 15px;
        border: 1px solid var(--wueblue);
        box-shadow: 2px 3px 4px rgba(0,0,0,0.2);

    }
    .slider:hover {
        opacity: 0.9;
    }

    .slider::-webkit-slider-thumb {
        -webkit-appearance: none;
        appearance: none;
        width: 15px;
        height: 15px;
        background: var(--wueblue);
        cursor: pointer;
        border-radius: 15px;
    }

    .slider::-moz-range-thumb {
        width: 15px;
        height: 15px;
        background: var(--wueblue);
        cursor: pointer;
    }
    hr {
        display: block;
        margin: 1em;
        width: 90%;
        height: 1px;
        content: "";
        margin-left: 5%;
        background-color: whitesmoke;
    }

  option:hover {
    background-color: var(--wueblue);
    color: black;
  }
  p{
    margin-top: 1%;
    margin-bottom: 1%;
    margin-right: 25%;
  }
    li{
        margin-left: 5%;
        margin-top: 2%;
        margin-bottom: 2%;
        margin-right: 25%;
    }
    .createTask {
        display: block;
        margin-bottom: 8%;
        padding-top: 55%;
    }

</style>
