<script lang="ts">
  import { ExperimentState } from "../../../definitions/experimentState";
  import { ProgressBar } from "carbon-components-svelte";
  import { ProgressBarData } from "../../../definitions/progressBarData";
  import { Task } from "../../../definitions/task";
  import { TaskType } from "../../../definitions/taskType";
  import CustomButton from "../../common/CustomButton.svelte";
  import PlotDatasetSplitter from "../../common/PlotDatasetSplitter.svelte";
  import DropdownSelector from "../../common/DropdownSelector.svelte";
  import {
    setExperimentTask,
    getExperimentTasks,
    getCurrentTimestamp,
    listenForExperimentResult,
  } from "../../../api/firebase";
  import { DropdownSelectorType } from "../../../definitions/dropdownSelectorType";
  import type { Network } from "../../../definitions/network";
  import {
    networksList,
    selectedNetworkIndex,
    defaultSeed,
  } from "../../../stores";
  import { fly } from "svelte/transition";
  import { ModalData } from "../../../definitions/modalData";
  import ExperimentResults from "../../common/ExperimentResults.svelte";
  import { delay } from "../../../util/generalUtil";

  let experimentState: ExperimentState = ExperimentState.CREATE;

  // These values should be set by UI Elements later on
  let xColumns: string[] = [];
  let trainPercentage: number = 0.8;
  let epochs: number = 100;
  let learningRate: number = 0.01;
  let seed: number = $defaultSeed;
  let hiddenLayers = [{ first: true, checked: false, size: 10 }];
  $: hiddenLayerSizes = hiddenLayers.map((layer) => layer.size);

  let selectedTask = undefined;
  let selectedModel = undefined;
  let selectedYColumn = undefined;

  let isCustomizeModalOpen: boolean = false;
  let currentNetwork: Network = undefined;
  let uploadingNetworkErrorModalData: ModalData = new ModalData(
    undefined,
    "Error Uploading Network",
    `There was an error uploading the network to storage. Please try again. If the problem persists, please contact the developers.`,
    false
  );

  /*
  progressBarData.isPresent = true by default since the page is being controlled by ExperimentState enum anyway
  */
  let progressBarData: ProgressBarData = new ProgressBarData(
    true,
    "Creating experiment..."
  );

  // remove the is_train column from the nodeColumns array
  $: nodeColumns = Object.keys(
    $networksList[$selectedNetworkIndex].nodes[0]
  ).filter((nodeColumns) => nodeColumns !== "is_train");

  let selectedNodeColumns = [];

  function handleModelChange(event) {
    selectedModel = event.detail;
  }

  function handleTaskChange(event) {
    selectedTask = event.detail;
  }

  function handleColumnChange(event) {
    selectedYColumn = event.detail;
  }

  function updateSelectedNodeColumns(event) {
    const column = event.target.value;
    if (event.target.checked) {
      selectedNodeColumns = [...selectedNodeColumns, column];
    } else {
      selectedNodeColumns = selectedNodeColumns.filter((f) => f !== column);
    }
  }

  function randomize() {
    seed = Math.floor(Math.random() * 1000);
  }

  function startNewExperiment() {
    experimentState = ExperimentState.CREATE;
    selectedTask = undefined;
    selectedModel = undefined;
  }

  function addHiddenLayer() {
    hiddenLayers = hiddenLayers.concat({
      first: false,
      checked: false,
      size: 10,
    });
  }

  function clearHiddenLayer() {
    hiddenLayers = hiddenLayers.filter((t) => !t.checked || t.first);
  }

  function saveSplitClicked(event: CustomEvent) {
    currentNetwork = event.detail.network;
    isCustomizeModalOpen = false;
    console.log("Current Network", currentNetwork);
  }

  async function createTask() {
    experimentState = ExperimentState.PROGRESS;
    await delay(2000); // To simulate task being run. TODO: Remove this later on.
    const taskToBeCreated = new Task(
      undefined, // This will be set by the backend
      selectedModel,
      selectedTask,
      epochs,
      trainPercentage,
      learningRate,
      hiddenLayerSizes,
      seed,
      getCurrentTimestamp(),
      ExperimentState.PROGRESS,
      selectedNodeColumns,
      selectedYColumn
    );

    await getExperimentTasks($networksList[$selectedNetworkIndex].metadata.id)
      .then((tasks) => {
        console.log("Tasks", tasks);
        tasks.forEach((task) => {
          if (task.equals(taskToBeCreated)) {
            console.log("Task already exists");
            return;
          }
        });
        setExperimentTask($networksList[$selectedNetworkIndex], taskToBeCreated)
          .then((taskDocId) => {
            console.log(`Task created with id: ${taskDocId}`);
            progressBarData.text = "Experiment created. Running...";
            listenForExperimentResult(
              $networksList[$selectedNetworkIndex].metadata.id,
              taskDocId
            )
              .then((resultTask: Task) => {
                progressBarData.isPresent = false;
                console.log("Result", resultTask);
                // @ts-ignore
                experimentState = ExperimentState[resultTask.state];
              })
              .catch((error) => {
                experimentState = ExperimentState.ERROR;
                console.log(`Error listening for experiment result: ${error}`);
              });
          })
          .catch((error) => {
            experimentState = ExperimentState.ERROR;
            console.log(`Error creating task ${taskToBeCreated}`, error);
          });
      })
      .catch((error) => {
        experimentState = ExperimentState.ERROR;
        console.log(
          `Error retrieving tasks for network ${$networksList[$selectedNetworkIndex]}: ${error}`
        );
      });
  }
</script>

<div
  in:fly={{ y: -50, duration: 250, delay: 300 }}
  out:fly={{ y: -50, duration: 250 }}
>
  {#if experimentState === ExperimentState.CREATE}
    <div class="background">
      <div>
        <li class="Model">
          <DropdownSelector
            placeholder={"Select a Network"}
            type={DropdownSelectorType.NETWORK}
          />

          <DropdownSelector
            placeholder={"Select a Model"}
            type={DropdownSelectorType.MLMODEL}
            on:modelChange={handleModelChange}
          />

          <DropdownSelector
            placeholder={"Select a Task"}
            type={DropdownSelectorType.TASK}
            on:taskChange={handleTaskChange}
          />

          <hr />

          <div>Configure Columns:</div>

          <DropdownSelector
            placeholder={"Select a column to predict"}
            type={DropdownSelectorType.Y_COLUMN}
            on:columnChange={handleColumnChange}
          />

          <div>
            {#each nodeColumns as column}
              <label>
                <input
                  type="checkbox"
                  value={column}
                  on:change={updateSelectedNodeColumns}
                />
                {column}
              </label>
            {/each}
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
              {#if selectedTask === TaskType.NODE_CLASSIFICATION}
                <CustomButton
                  type={"secondary"}
                  inverse={false}
                  fontsize={60}
                  on:click={() =>
                    (isCustomizeModalOpen = !isCustomizeModalOpen)}
                  >Customize</CustomButton
                >
              {/if}
              {#if isCustomizeModalOpen}
                <PlotDatasetSplitter
                  on:saveSplitClicked={saveSplitClicked}
                  {seed}
                  {trainPercentage}
                />
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
                fontsize={60}>Randomize</CustomButton
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
                  fontsize={100}
                  on:click={() => addHiddenLayer()}>Add New Layer</CustomButton
                >

                -
                <CustomButton
                  type={"delete"}
                  inverse={false}
                  fontsize={100}
                  on:click={() => clearHiddenLayer()}
                  >Delete Selected Layer</CustomButton
                >
              </div>
            </li>
          </div>

          <hr />

          <div class="createTask">
            <CustomButton
              type={"secondary"}
              inverse={false}
              disabled={selectedModel === undefined ||
                selectedTask === undefined ||
                epochs === 0 ||
                learningRate === 0.0 ||
                trainPercentage === 0 ||
                trainPercentage === 1}
              on:click={() => {
                createTask();
              }}>Create Task</CustomButton
            >
          </div>
        </li>

        <li class="Modal" />
      </div>
      <hr />
    </div>
  {:else if experimentState === ExperimentState.PROGRESS}
    <div class="progress_bar">
      <ProgressBar helperText={progressBarData.text} />
    </div>
  {:else if experimentState === ExperimentState.RESULT}
    <div class="newExperiment">
      <CustomButton
        type={"secondary"}
        inverse={false}
        on:click={() => {
          startNewExperiment();
        }}
        >Start New Experiment
      </CustomButton>
    </div>
    <hr />
    <ExperimentResults />
  {:else if experimentState === ExperimentState.ERROR}
    <p>Error</p>
  {/if}
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
    width: 55%;
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
