<script>
    import { createEventDispatcher, onDestroy} from "svelte";

    const dispatch = createEventDispatcher();
    const close = () => dispatch('close');

	let modal;

  </script>


  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <div class="modal-background" on:click={close}></div>
  
  
  
  <div class="modal" role="dialog" aria-modal="true" bind:this={modal}>
    <!-- svelte-ignore a11y-click-events-have-key-events -->

    <slot name="header"></slot>
    <hr>
    <slot name="body"></slot>
    <hr>
    <slot name="footer"></slot>
	<!-- svelte-ignore a11y-click-events-have-key-events -->
	<svg class="svg-icon" on:click={close} viewBox="0 0 20 20">
		<path d="M10.185,1.417c-4.741,0-8.583,3.842-8.583,8.583c0,4.74,3.842,8.582,8.583,8.582S18.768,14.74,18.768,10C18.768,5.259,14.926,1.417,10.185,1.417 M10.185,17.68c-4.235,0-7.679-3.445-7.679-7.68c0-4.235,3.444-7.679,7.679-7.679S17.864,5.765,17.864,10C17.864,14.234,14.42,17.68,10.185,17.68 M10.824,10l2.842-2.844c0.178-0.176,0.178-0.46,0-0.637c-0.177-0.178-0.461-0.178-0.637,0l-2.844,2.841L7.341,6.52c-0.176-0.178-0.46-0.178-0.637,0c-0.178,0.176-0.178,0.461,0,0.637L9.546,10l-2.841,2.844c-0.178,0.176-0.178,0.461,0,0.637c0.178,0.178,0.459,0.178,0.637,0l2.844-2.841l2.844,2.841c0.178,0.178,0.459,0.178,0.637,0c0.178-0.176,0.178-0.461,0-0.637L10.824,10z"></path>
	</svg>
    
  </div>

  
  <style>
    .modal-background {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0,0,0,0.3);
	}

	.modal {
		position: absolute;
		left: 50%;
		top: 50%;
		width: calc(100vw - 4em);
		max-width: 42em;
		max-height: calc(100vh - 4em);
		overflow: auto;
		transform: translate(-50%,-50%);
		padding: 2em;
		border-radius: 0.2em;
		background: white;
		z-index: 1;
    	
	}
	.svg-icon {
		position: absolute;
		top: 0;
		right: 0;
		width: 2.5em;
		height: 2.5em;
		cursor: pointer;
	}

  </style>