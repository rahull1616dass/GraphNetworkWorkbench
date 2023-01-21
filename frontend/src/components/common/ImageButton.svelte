<script>

export let defaultImageSource;

</script>

<button on:click>
    <img src= {defaultImageSource}>
    <slot></slot>
</button>


<style lang="scss">
    button {
      position: relative;
      top: -160px;
      right: 60px;
      border: none;
      color: transparent;
      padding: 0px;
      background-color: transparent;
    }
  </style>
  
  
  
  