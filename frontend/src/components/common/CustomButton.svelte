<script>
    export let type = 'primary';
    export let flat = false;
    export let inverse = false;
    export let disabled = false;
  </script>
  
  <button class:flat={flat} 
          class:inverse={inverse} 
          class={type} 
          class:disabled={disabled} on:click>
    <slot></slot>
  </button>
  
  <style>
    button{
      border: 0;
      cursor: pointer;
      border-radius: 6px;
      padding: 8px 12px;
      font-weight: bold;
      box-shadow: 1px 2px 3px rgba(0,0,0,0.2);
    }
    .flat{
      box-shadow: none;
    }
    .primary{
      background: #d8dadc;
      color: #063d79;
    }
    .secondary{
      background: #063d79;
      color: white;
    }
    .delete{
        background: red;
        color: white;
    }
    .primary.inverse{
      color: #063d79;
      background: #d8dadc;
      border: 2px solid #063d79;
    }
    .secondary.inverse{
      color: #063d79;
      background: white;
      border: 2px solid #063d79;
    }
    .delete.inverse{
        color: red;
        background: white;
        border: 2px solid red;
    }
    .primary.disabled {
        pointer-events: none;
        background-color: whitesmoke;
        color: lightgrey
    }
    .secondary.disabled {
        pointer-events: none;
        background-color: whitesmoke;
        color: lightgrey
    }
  </style>