<script>

export let defaultImageSource
export let styleClass = "defaultStyle"
export let width = "30px"
export let height = "30px"
</script>

<button on:click class={styleClass} >
    <!-- svelte-ignore a11y-missing-attribute -->
    <img src= {defaultImageSource} width={width} height={height}>
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
  
  
  
  