<script lang="ts">
  import { onMount } from "svelte"
  import { createEventDispatcher } from "svelte"

  const dispatch = createEventDispatcher()

  export let subNetworks: string[] = []
  let selectedSubNetworkIndex: number = 0

  const handleSubmit = () => {
    dispatch("submit", {
      selectedNetwork: subNetworks[selectedSubNetworkIndex],
    })
  }

  onMount(() => {})
</script>

<div class="popup-background">
  <div class="popup-panel">
    <button class="close-btn" on:click={() => dispatch("close")}>X</button>
    {#each subNetworks as networkName, index}
      <label>
        <input
          type="radio"
          name="strings"
          value={networkName}
          checked={index === selectedSubNetworkIndex}
          on:change={() => (selectedSubNetworkIndex = index)}
        />
        {networkName}
      </label>
    {/each}
    <button
      class="submit-btn"
      disabled={selectedSubNetworkIndex === undefined}
      on:click={handleSubmit}>Submit</button
    >
  </div>
</div>

<style>
  .popup-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2;
  }

  .popup-panel {
    background-color: white;
    width: 400px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    position: relative;
    max-height: 400px;
    overflow-y: auto;
  }

  .close-btn {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: transparent;
    border: none;
    font-size: 20px;
    cursor: pointer;
  }

  label {
    display: block;
    margin: 10px 0;
  }

  .submit-btn {
    background-color: skyblue;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-size: 16px;
    margin-top: 20px;
    cursor: pointer;
  }
</style>
