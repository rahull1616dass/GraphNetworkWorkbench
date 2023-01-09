<script>

export let defaultImageSource;

</script>

<button on:click>
    <img src= {defaultImageSource}>
    <slot></slot>
</button>

<style lang="scss">
    button {
      border: none;
      color: transparent;
      padding: 0px;
      background-color: transparent;
    }
  
    img {
      position: relative;
    }
  </style>
  
  
  
  