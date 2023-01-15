<script>

export let defaultImageSource;
export let position = 'relative'

</script>

<button on:click>
    <img src= {defaultImageSource}>
    <slot></slot>
</button>

<style lang="scss">
    button {
      position: absolute; 
      top: 30px;
      right: 530px;
      border: none;
      color: transparent;
      padding: 0px;
      background-color: transparent;
    }
  
    img {
      position: relative;
    }
  </style>
  
  
  
  