<script>
  export let id;
  export let files;
  let active = false;

  function handleInputClick() {
    active = true;
  }

  function handleInputChange() {
    active = false;
  }
</script>

<div class="file-input-container">
  <input
    class="file-input"
    type="file"
    {id}
    bind:files
    on:click={handleInputClick}
    on:change={handleInputChange}
  />
  <label class={`file-input-label ${active ? "active" : ""}`} for={id}>
    <slot />
  </label>
</div>

<style>
  .file-input-container {
    position: relative;
    width: 100%;
    height: 50px;
    padding: 8px 12px;
    margin-bottom: 10px;
    border-radius: 10px;
    box-shadow: 1px 2px 3px rgba(0, 0, 0, 0.2);
  }

  .file-input {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0.5;
    cursor: pointer;
    
  }

  .file-input-label {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 95%;
    font-weight: bold;
    cursor: pointer;
    color: var(--wueblue);
  }


</style>
