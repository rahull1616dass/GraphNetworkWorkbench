<script>
    import { onMount } from 'svelte';
    import { createEventDispatcher } from 'svelte';
  
    const dispatch = createEventDispatcher();
    let strings = [];
    let selectedString = '';
    let selectedStringIndex = -1;
  
    export let multipleNetworks = [];
    export let existMultipleNetworks = [];
  
    const handleSelection = (event) => {
      selectedString = event.target.value;
      selectedStringIndex = strings.indexOf(selectedString);
    };
  
    const handleSubmit = () => {
      if (selectedStringIndex >= 0) {
        existMultipleNetworks[selectedStringIndex] = true;
        dispatch('submit', selectedString);
      }
    };
  
    onMount(() => {
      strings = [...multipleNetworks];
    });
  </script>
  
  <div class="popup-background">
    <div class="popup-panel">
      <button class="close-btn" on:click={() => dispatch('close')}>X</button>
      {#each multipleNetworks as string, index}
        <label>
          <input
            type="radio"
            name="strings"
            value={string}
            on:change={handleSelection}
            disabled={existMultipleNetworks[index]}
          />
          {string}
        </label>
      {/each}
      <button class="submit-btn" disabled={!selectedString} on:click={handleSubmit}>Submit</button>
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
      z-index: 1;
    }
  
    .popup-panel {
      background-color: white;
      width: 400px;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
      position: relative;
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