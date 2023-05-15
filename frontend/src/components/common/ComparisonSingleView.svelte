<script>
  import { createEventDispatcher } from "svelte";
  import ExperimentResults from "./ExperimentResults.svelte";
  import CustomButton from "./CustomButton.svelte";
  import CustomDataTable from "./CustomDataTable.svelte";
  import PlotLoss from "./PlotLoss.svelte";
  import Embedding from "./Embedding.svelte";
  import PlotPrediction from "./PlotPrediction.svelte";

  const dispatch = createEventDispatcher();

  export let task;
  export let currentNetwork;

  let experimentPlots = {
    plotLoss: undefined,
    plotNodeEmbeddding: undefined,
    plotPrediction: undefined,
  };
  let nodeDataResult;
  let edgeDataResult;
</script>

<CustomDataTable {currentNetwork} {task} />

<div class="container">
  <table>
    <thead>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>{"Accuracy"}</td>
        <td>{task.accuracy}</td>
      </tr>

      <tr>
        <td>{"Precision"}</td>
        <td>{task.precision}</td>
      </tr>

      <tr>
        <td>{"Recall"}</td>
        <td>{task.recall}</td>
      </tr>
      <tr>
        <td>{"F1 Score"}</td>
        <td>{task.f1} </td>
      </tr>
      <tr>
        <td>{"AUC"}</td>
        <td>{task.auc} </td>
      </tr>
    </tbody>
  </table>
</div>

<div class="plots-container">
  <div class="plot-wrapper">
    <h4>Loss Function</h4>
    <div>
      <PlotLoss
        losses={task.losses}
        on:plotLoaded={(e) => {
          experimentPlots["plotLoss"] = e.detail;
        }}
      />
    </div>
  </div>

  <div class="plot-wrapper">
    <h4>Node Embedding</h4>
    <div>
      <Embedding
        {task}
        on:plotLoaded={(e) => {
          experimentPlots["plotNodeEmbedding"] = e.detail;
        }}
      />
    </div>
  </div>
</div>



<style>
  .plot-wrapper {
    position: flex;
    width: 100%; /* Adjust this value to change the size of the plots */
    margin-right: -20px;
  }

  .container {
    position: flex;
    /* top: 50%;
    left: 50%;
    transform: translate(-50%, -50%); */
    margin: auto;
    width: 80%;
    padding: 20px;
    box-sizing: border-box;
    background-color: #f0f0f0; /* Light gray background for contrast */
    border-radius: 10px; /* Rounded corners */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Slight shadow for a lifted effect */
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
</style>
