<script>
    import {createEventDispatcher} from 'svelte'
    const dispatch = createEventDispatcher();

    export let menuItems;
    export let activeMenuItem;

</script>

<div class="tabs">
    <ul>
        {#each menuItems as item}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <li on:click={() => dispatch('tabChange', item)}>
                <div class:active={item === activeMenuItem}>{ item }</div>
            </li>
        {/each}
    </ul>
</div>

<style>
    .tabs{
        margin-bottom: 40px;
    }
    ul{
        display: flex;
        justify-content: center;
        padding: 0%;
        list-style-type: none;
        
    }
    li{
        margin: 1% 5%;
        font-size: 120%;
        font-weight: 600;
        color: #aaa;
        cursor: pointer;
    }
    .active{
        color: #063d79;
        border-bottom: 5px solid #063d79;
        padding-bottom: 10%;
        
    }
</style>