<script lang="ts">
</script>

<div class="CardView">
  <slot class="header" />
  <hr />
  <slot class="body" />
  <hr />
  <slot class="footer" />
</div>

<style lang="scss">
  .CardView {
    position: center;
    width: 90%;
    margin-left: 5%;
    margin-top: 1%;
    margin-bottom: 3%;
    border-radius: 5px;
    box-shadow: 2px 3px 4px rgba(0, 0, 0, 0.2);
    background-color: whitesmoke;
  }

  hr {
    display: block;
    margin: 1em;
    width: 80%;
    height: 1%;
    margin-left: 10%;
    background-color: whitesmoke;
  }
</style>
