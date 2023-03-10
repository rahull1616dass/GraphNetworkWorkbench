<script lang="ts">
  import CardView from "./CardView.svelte"
  import Embedding from "./Embedding.svelte"
  import PlotLoss from "./PlotLoss.svelte"
  import PlotPrediction from "./PlotPrediction.svelte"
  import type { Task } from "../../definitions/task"

  export let task: Task = undefined
</script>

<div class="container">
  <CardView>
    <h4 slot="header">Details</h4>
    <div slot="body">
      <p>Accuracy:{task.accuracy}</p>
      <p>F1 score:</p>
      <p>Precision:</p>
      <p>Recall:</p>
    </div>

    <div slot="footer" />
  </CardView>

  <CardView>
    <h4 slot="header">Loss Function</h4>
    <div slot="body" />
      <PlotLoss losses={task.losses} />
    <div slot="footer" />
  </CardView>

  <CardView>
    <h4 slot="header">Node Embedding</h4>
    <div slot="body">
      <Embedding />
    </div>

    <div slot="footer" />
  </CardView>

  <CardView>
    <h4 slot="header">Network Results</h4>
    <div slot="body">
      <p>
        Green nodes/edges for correct predictions, red nodes/edges for false
        predictions
      </p>
      <PlotPrediction predictions={task.predictions} />
    </div>

    <div slot="footer" />
  </CardView>

  <CardView>
    <h4 slot="header">Expert Opinion</h4>
    <div slot="body">
      <p>{task.expertOpinion}</p>
    </div>
    <div slot="footer" />
  </CardView>
</div>

<style>
  .container {
    display: grid;
    grid-template-rows: repeat(3, 1fr);
    grid-template-columns: repeat(2, 1fr);
    gap: 2%;
    margin: 2%;
  }
  p {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI",
      Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue",
      sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
  }
</style>
