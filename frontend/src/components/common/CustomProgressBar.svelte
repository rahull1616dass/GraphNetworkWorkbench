<script>
    let progress = 0;
  </script>
  
  <div class="bx--progress">
    <div class="bx--progress-bar" role="progressbar" style="width: {progress}%" bind:this={progressBar}></div>
  </div>
  
  <style>
    .bx--progress {
      width: 100%;
      height: 8px;
      background: #e0e0e0;
      position: relative;
    }
  
    .bx--progress-bar {
      height: 100%;
      background: #0f62fe;
      animation: progress 2s infinite;
    }
  
    @keyframes progress {
      0% {
        width: 0;
      }
      50% {
        width: 100%;
      }
      100% {
        width: 0;
      }
    }
  </style>



  