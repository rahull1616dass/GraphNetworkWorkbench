<script>

export let defaultImageSource
export let styleClass = "defaultStyle"
</script>

<button on:click class={styleClass} >
    <img src= {defaultImageSource}>
    <slot></slot>
</button>


<style lang="scss">
    .defaultStyle {
      position: relative;
      top: -160px;
      right: 60px;
      border: none;
      color: transparent;
      padding: 0px;
      background-color: transparent;
    }
    .deleteButtonClass{
      position: relative;
      border: none;
      color: transparent;
      padding: 0px;
      background-color: transparent;
    }
  </style>
  
  
  
  