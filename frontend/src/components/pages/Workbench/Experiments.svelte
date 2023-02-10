<script lang="ts">
  import { Dropdown, ProgressBar } from "carbon-components-svelte";
  import { ProgressBarData } from "../../../definitions/progressBarData";
  import { Task } from "../../../definitions/task";
  import { TaskType } from "../../../definitions/taskType";
  import { setExperimentTask, getExperimentTasks } from "../../../api/firebase";
  import CustomButton from "../../common/CustomButton.svelte";
  import { MLModelType } from "../../../definitions/mlModelType";
  import { MenuItem } from "../../../definitions/menuItem";
  import {
    networksList,
    selectedNetworkIndex,
    selectedModelType,
    selectedTaskType,
    selectedMenuItem,
  } from "../../../stores";
  import { fade, slide, scale } from "svelte/transition";
  import Plot from "./Plot/Plot.svelte";
  import CustomModal from "../../common/CustomModal.svelte";

  let networkIndex: number = undefined;
  let task: TaskType;
  let model: MLModelType;
  let placeholderNetwork: string = "Select a network";
  let placeholderModel: string = "Select a model";
  let placeholderTask: string = "Select a task";
  let unique = {}; // every {} is unique, {} === {} evaluates to false

  // These values should be set by UI Elements later on
  let trainPercentage: number = 0.8;
  let epochs: number = 100;
  let learningRate: number = 0.01;
  let seed: number = 42;
  let hiddenLayers = [{ first: true, checked: false, size: 10 }];
  $: hiddenLayerSizes = hiddenLayers.map((layer) => layer.size);

  function randomize() {
    seed = Math.floor(Math.random() * 10000);
  }

  function openModal() {
    return;
  }

  function startNewExperiment() {
    $selectedMenuItem = MenuItem.PLOT;
    //$selectedMenuItem = MenuItem.EXPERIMENTS;
  }

  let progressBarData: ProgressBarData = new ProgressBarData(
    false,
    "Training..."
  );

  function add() {
    hiddenLayers = hiddenLayers.concat({
      first: false,
      checked: false,
      size: 10,
    });
  }

  function clear() {
    hiddenLayers = hiddenLayers.filter((t) => !t.checked || t.first);
  }

  async function createTask() {
    const taskToBeCreated = new Task(
      undefined, // This will be set by the backend
      $selectedModelType,
      $selectedTaskType,
      trainPercentage,
      epochs,
      learningRate,
      hiddenLayerSizes,
      seed
    );
    const networkId = $networksList[$selectedNetworkIndex].metadata.id;
    await getExperimentTasks(networkId)
      .then((tasks) => {
        console.log("Tasks", tasks);
        tasks.forEach((task) => {
          if (task.equals(taskToBeCreated)) {
            console.log("Task already exists");
            return;
          }
        });
        setTaskDocument(networkId, taskToBeCreated);
      })
      .catch((error) => {
        console.log("Error getting tasks list", error);
      });
  }
  let modelTypes: MLModelType[] = [
    MLModelType.GCN,
    MLModelType.DeepWalk,
    MLModelType.GIN,
  ];
  let taskTypes: TaskType[] = [
    TaskType.NODE_CLASSIFICATION,
    TaskType.EDGE_CLASSIFICATION,
  ];

  async function setTaskDocument(
    networkId: string,
    taskToBeCreated: Task
  ): Promise<void> {
    return new Promise((resolve, reject) => {
      setExperimentTask(networkId, taskToBeCreated)
        .then((task) => {
          console.log("Task created", task);
          resolve();
        })
        .catch((error) => {
          console.log("Error creating task", error);
          reject();
        });
    });
  }
</script>

<div transition:fade>
  <div class="newExperiment">
    <CustomButton
      type={"secondary"}
      inverse={false}
      on:click={() => startNewExperiment()}
      >Start New Experiment
    </CustomButton>
  </div>

  <hr />

  <div>
    <li class="Model">
      <div>
        <select
          class="selectModel"
          bind:value={networkIndex}
          on:click={() => ($selectedNetworkIndex = networkIndex)}
        >
          {#if placeholderNetwork}
            <option>{placeholderNetwork}</option>
          {/if}
          {#each $networksList as network, networkIndex}
            <option
              class="optionDropdown"
              value={networkIndex}
              on:click={() => ($selectedNetworkIndex = networkIndex)}
            >
              {network.metadata.name} --- Nodes: {network.nodes.length} , Edges:
              {network.links.length}
            </option>
          {/each}
        </select>
      </div>

      <div>
        <select
          class="selectModel"
          bind:value={task}
          on:click={() => ($selectedTaskType = task)}
        >
          {#if placeholderModel}
            <option>{placeholderTask}</option>
          {/if}
          {#each taskTypes as task, _}
            <option
              class="optionDropdown"
              value={task}
              on:click={() => ($selectedTaskType = task)}
            >
              {task}
            </option>
          {/each}
        </select>
      </div>

      <div>
        <select
          class="selectModel"
          bind:value={model}
          on:click={() => ($selectedModelType = model)}
        >
          {#if placeholderModel}
            <option>{placeholderModel}</option>
          {/if}
          {#each modelTypes as model, _}
            <option
              class="optionDropdown"
              value={model}
              on:click={() => ($selectedModelType = model)}
            >
              {model}
            </option>
          {/each}
        </select>
      </div>

      <hr />

      <div>Configurable Parameters:</div>

      <div>
        <li>Epochs</li>
        <li class="range">
          <input
            type="range"
            bind:value={epochs}
            min="0"
            max="1000"
            step="10"
            class="slider"
          />
          <input type="number" bind:value={epochs} class="inputNumber" />
        </li>
      </div>
      <div>
        <li>Learning Rate</li>
        <li class="range">
          <input
            type="range"
            bind:value={learningRate}
            min="0"
            max="0.4"
            step="0.001"
            class="slider"
          />
          <input
            type="number"
            bind:value={learningRate}
            min="0"
            max="0.4"
            step="0.001"
            class="inputNumber"
          />
        </li>
      </div>
      <div>
        <li>
          Training Percentage

          {#if $selectedTaskType === TaskType.NODE_CLASSIFICATION}
            <CustomButton
              type={"secondary"}
              inverse={false}
              fontsize={8}
              on:click={() => openModal()}>Customize</CustomButton
            >
          {/if}
        </li>
        <li class="range">
          <input
            type="range"
            bind:value={trainPercentage}
            min="0"
            max="1"
            step="0.05"
            class="slider"
          />
          <input
            type="number"
            bind:value={trainPercentage}
            min="0"
            max="1"
            step="0.05"
            class="inputNumber"
          />
        </li>
      </div>

      <div>
        <li>
          Seed
          <CustomButton
            type={"secondary"}
            inverse={false}
            on:click={() => randomize()}
            fontsize={8}>Randomize</CustomButton
          >
        </li>
        <li class="range">
          <input
            type="range"
            bind:value={seed}
            min="0"
            max="1000"
            step="10"
            class="slider"
          />
          <input type="number" bind:value={seed} class="inputNumber" />
        </li>
      </div>

      <div>
        <li>Add/Delete Hidden Layers</li>
        <li class="hiddenLayers">
          {#each hiddenLayers as hiddenLayer, index}
            <div class:checked={hiddenLayer.checked}>
              <label for="hiddenLayer">Hidden Layer {index + 1}</label>
              <input type="checkbox" bind:checked={hiddenLayer.checked} />
              <input
                type="range"
                min="1"
                max="20"
                step="1"
                class="slider"
                bind:value={hiddenLayer.size}
              />
              {hiddenLayer.size}
            </div>
          {/each}

          <div class="hiddenLayerButtons">
            <CustomButton
              type={"secondary"}
              inverse={false}
              fontsize={8}
              on:click={() => add()}>Add New Layer</CustomButton
            >

            -
            <CustomButton
              type={"delete"}
              inverse={false}
              fontsize={8}
              on:click={() => clear()}>Delete Selected Layer</CustomButton
            >
          </div>
        </li>
      </div>

      <hr />

      <div class="createTask">
        <CustomButton
          type={"secondary"}
          inverse={false}
          disabled={$selectedModelType === undefined ||
            $selectedTaskType === undefined ||
            epochs === 0 ||
            learningRate === 0.0 ||
            trainPercentage === 0 ||
            trainPercentage === 1}
          on:click={() => createTask()}>Create Task</CustomButton
        >
      </div>
    </li>

    <li class="Modal" />
  </div>

  <hr />
</div>

<style lang="scss">
  .inputNumber {
    width: 15%;
    padding: 1%;
    //background-color: whitesmoke;
    border-radius: 15px;
    box-shadow: 1px 2px 3px rgba(0, 0, 0, 0.1);
  }
  .customizeButton {
    display: flex;
    justify-content: center;
    margin-top: 2%;
    font-size: small;
  }
  .hiddenLayerButtons {
    display: flex;
    justify-content: center;
    //flex-direction: row;
    margin-top: 5%;
    margin-bottom: 5%;
    font-size: small;
  }
  .hiddenLayers {
    flex-direction: row;
    align-items: center;
    margin-left: 25%;
    margin-right: 20%;
    margin-top: 1%;
  }
  .newExperiment {
    display: flex;
    justify-content: center;
    margin-top: 1%;
  }
  .tooltip {
    z-index: 1;
  }
  .background {
    color: var(--wueblue);
    font-weight: 600;
  }
  .range {
    width: 80%;
    margin-left: 10%;
    align-items: left;
  }
  .dropdown {
    position: flex;
    width: 50%;
    margin-left: 25%;
    margin-top: 1%;
    background-color: whitesmoke;
    border-radius: 15px;
    box-shadow: 1px 2px 3px rgba(0, 0, 0, 0.1);
  }
  .Model {
    position: center;
    width: 55%;
    margin-left: 22%;
    margin-top: 1%;
    margin-bottom: 3%;
    border-radius: 15px;
    // border: whitesmoke 4px inset;
    box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.2);
    background-color: whitesmoke;
    //color: white;
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
    box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.2);
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
  .slider {
    -webkit-appearance: none; /* Override default CSS styles */
    appearance: none;
    width: 75%; /* Full-width */
    background: white; /* Grey background */
    opacity: 1;
    -webkit-transition: 0.2s;
    transition: opacity 0.2s;
    border-radius: 15px;
    border: 1px solid var(--wueblue);
    box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.2);
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
  p {
    margin-top: 1%;
    margin-bottom: 1%;
    margin-right: 25%;
  }
  li {
    margin-left: 15%;
    margin-top: 2%;
    margin-bottom: 2%;
    margin-right: 25%;
  }
  .createTask {
    display: block;
    margin-bottom: 8%;
    padding-top: 5%;
  }
</style>
