<script>
  import CardView from "./CardView.svelte";
</script>

<div class="container">
  <CardView />

  <CardView />

  <CardView />

  <CardView />
</div>

<style>
  .container {
    display: grid;
    grid-template-rows: repeat(2, 1fr);
    grid-template-columns: repeat(2, 1fr);
    gap: 2%;
    margin: 2%;
  }
</style>
