<script>
  import { TaskType } from "../../definitions/taskType";
  export let currentNetwork;
  export let task;
  export let width = "75%";
</script>

<div class="container" style="width: {width};">
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
      {#if task.taskType === TaskType.NODE_CLASSIFICATION}
        <tr class:highlight={task.yColumn === undefined}>
          <td>{"Column to Predict"}</td>
          <td>{task.yColumn} </td>
        </tr>
      {/if}

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
</div>

<style>
  .container {
    display: flex;
    align-self: center;
    margin: auto;
    width: 75%;
    padding: 20px;
    box-sizing: border-box;
    background-color: #f0f0f0; /* Light gray background for contrast */
    border-radius: 10px; /* Rounded corners */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Slight shadow for a lifted effect */
    overflow: auto;
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

  .highlight {
    background-color: #ffcccc !important; /* Change the color to your desired highlight color */
  }
</style>
