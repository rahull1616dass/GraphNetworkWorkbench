<script>
  export let margintop = 2;
  export let marginbottom = 4;
</script>

<div
  class="info-text"
  style="margin-top: {margintop}rem; margin-bottom: {marginbottom}rem;"
>
  <slot />
</div>

<style>
  .info-text {
    background-color: var(--wueblue);
    border-radius: 5px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    font-size: 1.1rem;
    color: white;
  }
</style>

  