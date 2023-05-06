<script lang="ts">
  import { ExperimentState } from "../../../definitions/experimentState";
  import { DataTable, ProgressBar } from "carbon-components-svelte";
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
  import Countup from "svelte-countup";
  import { COLUMN_IS_TRAIN } from "../../../definitions/constants";
  import InfoBox from "../../common/InfoBox.svelte";
  import LeftArrow from "../../common/LeftArrow.svelte";
  import RightArrow from "../../common/RightArrow.svelte";
  import InfoText from "../../common/InfoText.svelte";
  import { onMount } from "svelte";
  import DropdownMultiSelector from "../../common/DropdownMultiSelector.svelte";
  import { MLModelType } from "../../../definitions/mlModelType";
  let infoBoxContent =
    "<p>Select a network, model, and task. Choose which columns to predict and use as features. Customize the hyperparameters, such as epochs, training percentage, and learning rate.</p><p>You can also customize the network layers by adding or changing the number of neurons in each layer. Once everything is specified, create the task. Note that you must select all the necessary fields before creating the task.</p>";

  $: isInfoModalOpen = false;

  let hiddenLayers = [
    { permanent: true, checked: false, size: 10 },
    { permanent: true, checked: false, size: 10 },
  ];
  let customizedSplitDefined: boolean = false;

  // These values should be set by UI Elements later on
  let task = new Task(
    "cJuui4MU0OYn5YyeLu6Z", // taskID
    MLModelType.GCNCONV, // mlModelType,
    TaskType.NODE_CLASSIFICATION, // taskType,
    100, // epochs,
    0.8, // trainPercentage,
    false, //useCustomSplit
    0.01, // learningRate
    [10, 7, 17], // hiddenLayerSizes
    99, // seed
    undefined, // createdAt,
    ExperimentState.RESULT, // experimentState,
    ["index"], // xColumns,
    "group", // yColumn,
    "Based on the provided data, it seems like the model is already performing very well with a validation accuracy score of 1.0, and good values for loss, precision, recall, f1 score, and ROC AUC score. Therefore, it might not be necessary to optimize the model further, unless there are specific requirements or constraints that need to be met.However, if the user still wants to optimize the model, there are a few things that they could try. Firstly, they could experiment with different activation functions (other than Relu and Softmax) to see if they can improve performance. Secondly, they could try adjusting the number of layers and their sizes, and observe the effect on the models metrics. Thirdly, they could try adjusting the learning rate to see if they can achieve faster convergence. Finally, they could try adding more features to the model to see if it improves performance",
    0.1,
    1,
    1,
    1,
    1,
    [2.3574, 1.0597, 0.67, 0.91, 1.0585, 0.9929, 0.8292, 0.7172, 0.6718],
    {
      "5": "0",
      "6": "0",
      "16": "0",
      "18": "1",
      "27": "1",
      "32": "1",
      "33": "1",
    },
    {
      "0": [3.4665, 1.8362],
      "1": [0.1957, 0.818],
      "2": [4.0159, 0.627],
      "3": [-3.8721, 0.5197],
      "4": [-7.2122, 0.358],
      "5": [-6.1562, 0.6418],
    }
  );

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

  let progressDataTable = {
    rows: [],
    headers: [
      { key: "parameter", value: "Parameter" },
      { key: "value", value: "Value" },
    ],
  };

  // remove the is_train column from the selectableColumns array
  $: selectableColumns = Object.keys(currentNetwork.nodes[0]).filter(
    (nodeColumns) => nodeColumns !== COLUMN_IS_TRAIN
  );
  $: task.hiddenLayerSizes = hiddenLayers.map((layer) => layer.size);
  $: currentNetwork = $networksList[$selectedNetworkIndex];
  $: customizedSplitDefined = checkCustomizedSplit();

  // Create a reactive variable to store checked state of each column
  let checkedStates = {};
  $: {
    selectableColumns.forEach((column) => {
      checkedStates[column] = task.xColumns.includes(column);
    });
  }

  let currentIndex = 0;
  const totalContent = 5;
  let previousTasks: Task[] = [];

  $: {
    if (task.state === ExperimentState.RESULT) {
      resetPage();
    } else if (task.state === ExperimentState.ERROR) {
      resetPage();
    }
  }

  onMount(() => {
    getPreviousTasks();
  });

  async function getPreviousTasks() {
    await getExperimentTasks(currentNetwork.metadata.id)
      .then((tasks) => {
        previousTasks = tasks;
        for (let previousTask of previousTasks) {
          // @ts-ignore
          if (
            ExperimentState[previousTask.state] === ExperimentState.PROGRESS
          ) {
            listenExpResult(previousTask.id);
            task = previousTask;
            task.state = ExperimentState.PROGRESS;
            createExperimentDataTable();
            break;
          }
        }
      })
      .catch((error) => {
        task.state = ExperimentState.ERROR;
        console.log(
          `Error retrieving tasks for network ${currentNetwork}: ${error}`
        );
      });
  }

  function listenExpResult(taskDocId: string) {
    listenForExperimentResult(currentNetwork.metadata.id, taskDocId)
      .then((resultTask: Task) => {
        task = resultTask;
        progressBarData.isPresent = false;
        console.log("Result", resultTask);
        // @ts-ignore
        task.state = ExperimentState[resultTask.state];
      })
      .catch((error) => {
        task.state = ExperimentState.ERROR;
        console.log(`Error listening for experiment result: ${error}`);
      });
  }

  function goLeft() {
    currentIndex = (currentIndex - 1 + totalContent) % totalContent;
  }

  function goRight() {
    currentIndex = (currentIndex + 1) % totalContent;
  }

  function resetPage() {
    currentIndex = 0;
  }

  function checkCustomizedSplit(): boolean {
    return (
      currentNetwork !== undefined &&
      currentNetwork.nodes.every(
        (node) =>
          node[COLUMN_IS_TRAIN] !== undefined && node[COLUMN_IS_TRAIN] !== null
      )
    );
  }

  function resetCustomizedSplit() {
    currentNetwork.nodes.forEach((node) => delete node[COLUMN_IS_TRAIN]);
    customizedSplitDefined = false;
  }

  function handleModelChange(event) {
    task.mlModelType = event.detail;
  }

  function handleTaskChange(event) {
    task.taskType = event.detail;
  }

  function handleColumnChange(event) {
    task.yColumn = event.detail;
  }

  function updateSelectedNodeColumns(event) {
    const column = event.target.value;
    if (event.target.checked) {
      task.xColumns = [...task.xColumns, column];
    } else {
      task.xColumns = task.xColumns.filter((f) => f !== column);
    }
  }

  function randomize() {
    task.seed = Math.floor(Math.random() * 1000);
  }

  function startNewExperiment() {
    task.state = ExperimentState.CREATE;
    task.taskType = undefined;
    task.mlModelType = undefined;
    task.xColumns = [];
  }

  function addHiddenLayer() {
    hiddenLayers = hiddenLayers.concat({
      permanent: false,
      checked: false,
      size: 10,
    });
  }

  function clearHiddenLayer() {
    hiddenLayers = hiddenLayers.filter((t) => !t.checked || t.permanent);
  }

  function saveSplitClicked(event: CustomEvent) {
    currentNetwork = event.detail.network;
    isCustomizeModalOpen = false;
    customizedSplitDefined = true;
    console.log("Current Network", currentNetwork);
  }

  function closePlotPopup(event: CustomEvent) {
    console.log("Close");
    isCustomizeModalOpen = false;
  }

  function createExperimentDataTable() {
    let parameters = Object.keys(task).filter(
      (key) => task[key] !== undefined && task[key] !== null
    );
    progressDataTable.rows = parameters.map((parameter) => {
      // If task[parameter] is an array, convert it to a string
      let taskValue = task[parameter];
      if (Array.isArray(task[parameter])) {
        taskValue = task[parameter].join(", ");
      }
      return { parameter: parameter, value: taskValue };
    });
    // For each row in rows, create an id field with id as the index of the row
    progressDataTable.rows.forEach((row, index) => {
      row.id = index;
    });
  }

  async function createTask() {
    task.state = ExperimentState.PROGRESS;
    task.useCustomSplit = customizedSplitDefined;
    if (task.taskType === TaskType.EDGE_PREDICTION) {
      task.yColumn = "";
    }
    createExperimentDataTable();
    // await delay(2000) // To simulate task being run. TODO: Remove this later on.
    previousTasks.forEach((firestoreTask) => {
      if (firestoreTask.equals(task)) {
        console.log("Task already exists");
        return;
      }
    });
    task.createdAt = getCurrentTimestamp();
    setExperimentTask(currentNetwork, task)
      .then((taskDocId) => {
        console.log(`Task created with id: ${taskDocId}`);
        progressBarData.text = "Experiment created. Running...";
        listenExpResult(taskDocId);
      })
      .catch((error) => {
        task.state = ExperimentState.ERROR;
        console.log(`Error creating task ${task}`, error);
      });
  }

  $: {
    if (isCustomizeModalOpen) {
      window.scrollTo(0, 0);
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  }
</script>

<div class="info">
  <InfoBox
    bind:isInfoModalOpen
    headerText="Experiments Guide"
    bodyText={infoBoxContent}
  />
</div>

<div
  in:fly={{ y: -50, duration: 250, delay: 300 }}
  out:fly={{ y: -50, duration: 250 }}
>
  {#if task.state === ExperimentState.CREATE}
    <div class="container">
      {#if currentIndex !== 0}
        <LeftArrow on:click={goLeft} />
      {/if}

      {#if currentIndex === 0}
        <div class="content">
          <InfoText>
            Select the network you want to run an experiment on <br />
            Then select the model and task you want to run on the network
          </InfoText>

          <DropdownSelector
            placeholder={"Select a Network"}
            type={DropdownSelectorType.NETWORK}
          />

          <DropdownSelector
            placeholder={"Select a Model"}
            type={DropdownSelectorType.MLMODEL}
            on:modelChange={handleModelChange}
            bind:model={task.mlModelType}
          />

          <DropdownSelector
            placeholder={"Select a Task"}
            type={DropdownSelectorType.TASK}
            on:taskChange={handleTaskChange}
            bind:task={task.taskType}
          />
        </div>
      {:else if currentIndex === 1}
        <div class="content">
          <InfoText>
            Here is where you can select the columns to use as features and the
            column to predict.
          </InfoText>

          {#if task.taskType === TaskType.NODE_CLASSIFICATION}
            <DropdownSelector
              placeholder={"Select a column to predict"}
              type={DropdownSelectorType.Y_COLUMN}
              on:columnChange={handleColumnChange}
              bind:y_column={task.yColumn}
            />
          {/if}

          <hr />
          Select the columns to use as features.
          <hr />
          <div>
            {#each selectableColumns as column}
              <label>
                <input
                  type="checkbox"
                  value={column}
                  on:change={updateSelectedNodeColumns}
                  bind:checked={checkedStates[column]}
                />
                {column}
              </label>
            {/each}
          </div>
        </div>
      {:else if currentIndex === 2}
        <div class="content">
          <InfoText>
            This is where you can customize the hyperparameters of the
            experiment
          </InfoText>

          <div>
            <li>Epochs</li>
            <li class="range">
              <input
                type="range"
                bind:value={task.epochs}
                min="0"
                max="1000"
                step="10"
                class="slider"
              />
              <input
                type="number"
                bind:value={task.epochs}
                class="inputNumber"
              />
            </li>
          </div>
          <div>
            <li>Learning Rate</li>
            <li class="range">
              <input
                type="range"
                bind:value={task.learningRate}
                min="0"
                max="0.4"
                step="0.001"
                class="slider"
              />
              <input
                type="number"
                bind:value={task.learningRate}
                min="0"
                max="0.4"
                step="0.001"
                class="inputNumber"
              />
            </li>
          </div>

          <div>
            <li>
              {#if task.taskType === TaskType.NODE_CLASSIFICATION && customizedSplitDefined === true}
                Train/Test Split
              {:else}
                Training Percentage
              {/if}
              {#if task.taskType === TaskType.NODE_CLASSIFICATION}
                <CustomButton
                  type={"secondary"}
                  inverse={false}
                  fontsize={60}
                  on:click={() =>
                    (isCustomizeModalOpen = !isCustomizeModalOpen)}
                  >Customize</CustomButton
                >
                {#if customizedSplitDefined === true}
                  <p>Customized training percentage used</p>
                  <CustomButton
                    type={"secondary"}
                    inverse={false}
                    fontsize={60}
                    on:click={() => resetCustomizedSplit()}>Reset</CustomButton
                  >
                {/if}
                {#if isCustomizeModalOpen}
                  <PlotDatasetSplitter
                    on:saveSplitClicked={saveSplitClicked}
                    on:closePopup={closePlotPopup}
                    seed={task.seed}
                    {currentNetwork}
                    groupColumn={task.yColumn}
                    trainPercentage={task.trainPercentage}
                  />
                {/if}
              {/if}
            </li>
            {#if task.taskType !== TaskType.NODE_CLASSIFICATION || (task.taskType === TaskType.NODE_CLASSIFICATION && customizedSplitDefined === false)}
              <li class="range">
                <input
                  type="range"
                  bind:value={task.trainPercentage}
                  min="0"
                  max="1"
                  step="0.05"
                  class="slider"
                />
                <input
                  type="number"
                  bind:value={task.trainPercentage}
                  min="0"
                  max="1"
                  step="0.05"
                  class="inputNumber"
                />
              </li>
            {/if}
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
                bind:value={task.seed}
                min="0"
                max="1000"
                step="10"
                class="slider"
              />
              <input type="number" bind:value={task.seed} class="inputNumber" />
            </li>
          </div>
        </div>
      {:else if currentIndex === 3}
        <div class="content">
          <InfoText>
            You can customize the neural network by adding and removing layers
          </InfoText>
          <li class="hiddenLayers">
            {#each hiddenLayers as hiddenLayer, index}
              <div class:checked={hiddenLayer.checked}>
                <label for="hiddenLayer">Hidden Layer {index + 1}</label>
                <input type="checkbox" bind:checked={hiddenLayer.checked} />
                <input
                  type="range"
                  min="2"
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
      {:else if currentIndex === 4}
        <div class="content">
          <InfoText>
            You can start the experiment by clicking the button below <br />
            If the button is inactive, you have to fill in all the required fields
            in the previous steps
          </InfoText>
          <table>
            <thead>
              <tr>
                <th>Required Fields</th>
                <th>Selected Value</th>
              </tr>
            </thead>
            <tbody>
              <tr class:highlight={!currentNetwork.metadata.name}>
                <td>{"Network"}</td>
                <td>{currentNetwork.metadata.name}</td>
              </tr>

              <tr class:highlight={task.mlModelType === undefined}>
                <td>{"Model"}</td>
                <td>{task.mlModelType}</td>
              </tr>

              <tr class:highlight={task.taskType === undefined}>
                <td>{"Task"}</td>
                <td>{task.taskType}</td>
              </tr>

              <tr class:highlight={task.xColumns.length === 0}>
                <td>{"Columns to Train"}</td>
                <td>{task.xColumns} </td>
              </tr>

              <tr class:highlight={!task.epochs}>
                <td>{"Epochs"}</td>
                <td>{task.epochs}</td>
              </tr>

              <tr class:highlight={task.learningRate === 0.0}>
                <td>{"Learning Rate"}</td>
                <td>{task.learningRate}</td>
              </tr>

              <tr
                class:highlight={task.trainPercentage === 1 ||
                  task.trainPercentage === 0}
              >
                <td>{"Training Percentage"}</td>
                <td>{task.trainPercentage}</td>
              </tr>

              <tr class:highlight={!task.seed}>
                <td>{"Seed"}</td>
                <td>{task.seed}</td>
              </tr>

              <tr class:highlight={!task.hiddenLayerSizes}>
                <td>{"Hidden Layers"}</td>
                <td>{task.hiddenLayerSizes}</td>
              </tr>
            </tbody>
          </table>
          <div class="createTask">
            <CustomButton
              type={"secondary"}
              inverse={false}
              disabled={task.mlModelType === undefined ||
                task.epochs === 0 ||
                task.learningRate === 0.0 ||
                (!customizedSplitDefined && task.trainPercentage === 0) ||
                (task.trainPercentage === 0 &&
                  task.taskType === TaskType.NODE_CLASSIFICATION &&
                  checkCustomizedSplit() === true) ||
                (task.taskType === TaskType.NODE_CLASSIFICATION &&
                  task.yColumn === undefined) ||
                task.xColumns.length === 0 ||
                task.trainPercentage === 1}
              on:click={() => {
                createTask();
              }}>Create Task</CustomButton
            >
          </div>
        </div>
      {/if}

      {#if currentIndex !== totalContent - 1}
        <RightArrow on:click={goRight} />
      {/if}
    </div>
  {:else if task.state === ExperimentState.PROGRESS}
    <div class="progress_bar">
      <ProgressBar helperText={progressBarData.text} />
      It has been running for
      <Countup
        initial={0}
        value={100}
        duration={100000}
        step={1}
        roundto={1}
        format={true}
      />
      seconds
      <DataTable
        headers={progressDataTable.headers}
        rows={progressDataTable.rows}
      />
    </div>
  {:else if task.state === ExperimentState.RESULT}
    <ExperimentResults {task} {currentNetwork} {startNewExperiment} />
  {:else if task.state === ExperimentState.ERROR}
    <InfoText>Error: {task.errorMessage}</InfoText>
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
  {/if}
</div>

<style lang="scss">
  .highlight {
    background-color: #ffcccc !important; /* Change the color to your desired highlight color */
  }

  .fixed-left-arrow {
    position: fixed;
    left: 10px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1000;
  }

  .fixed-right-arrow {
    position: fixed;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    z-index: 1000;
  }

  table {
    border-collapse: collapse;
    width: 100%;
  }

  th,
  td {
    text-align: left;
    padding: 8px;
  }

  th {
    background-color: #f2f2f2;
    font-weight: bold;
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  .container {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .content {
    margin: 0 2rem;
  }
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
