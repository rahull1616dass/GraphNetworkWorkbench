<script>
  import CardView from "./CardView.svelte";
  import Embedding from "./Embedding.svelte";
</script>

<div class="container">
  <CardView>
    <h4 slot="header">Details</h4>
    <div slot="body">
      <p>Accuracy:</p>
      <p>F1 score:</p>
      <p>Precision:</p>
      <p>Recall:</p>
    </div>

    <div slot="footer" />
  </CardView>

  <CardView>
    <h4 slot="header">Loss Function</h4>
    <div slot="body" />

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
    </div>

    <div slot="footer" />
  </CardView>
</div>

<style>
  .container {
    display: grid;
    grid-template-rows: repeat(2, 1fr);
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
