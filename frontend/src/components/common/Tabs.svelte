<script>
    import {createEventDispatcher} from 'svelte'
    import logo from "../../assets/logo.svg"
    const dispatch = createEventDispatcher();

    export let menuItems;
    export let activeMenuItem;

</script>

<div class="tabs">
    <li class="image"> <img src={logo} class="logo" alt="logo" > </li>
    <ul> 
        
        {#each menuItems as item}
            
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <li class="menuItem" on:click={() => dispatch('tabChange', item)}> 
                <div class:active={item === activeMenuItem}>{ item } | </div> 
            </li>
        {/each}
    </ul>
</div>

<style>
    .tabs{
        background-color: whitesmoke;
        box-shadow: 0 0 0 0 rgba(0,0,0,.5);
    }
    .image{
        display: flex;
        justify-content: left;
        padding: 0%;
        list-style-type: none;
    }
    ul{
        display: flex;
        justify-content: right;
        padding: 0%;
        list-style-type: none;
        
    }
    .menuItem{
        margin: 1% 1%;
        font-size: 120%;
        font-weight: 600;
        /*color: #4a4a56;*/
        color: #063d79;
        cursor: pointer;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    
    }
    
    .active{
        color: #bf0a30;
        padding-bottom: 20%;
        
    }
    img{
        max-width: 30%;
        height: 30%;
        
    }
</style>