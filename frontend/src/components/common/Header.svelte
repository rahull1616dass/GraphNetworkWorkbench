<script lang="ts">
    import wue_banner from "../../assets/wue_banner.svg"
    import { selectedMenuItem } from "../../stores"
    import { MenuItem } from "../../definitions/menuItem"
    import Tabs from "../common/Tabs.svelte"

    let menuItems = ['Home', 'My Networks', 'Visualize', 'Experiments', 'Reports', 'Profile']
    let activeMenuItem = "Home";
    const tabChange = (e) => activeMenuItem = e.detail;
    
</script>


<header>
    <h1>
        <a href="/" on:click|preventDefault={() => ($selectedMenuItem = MenuItem.HOME)}>
            <img  src={wue_banner} class="wue_banner" alt="wue_banner" >
        </a>
        <Tabs {activeMenuItem} {menuItems} on:tabChange={tabChange} />
        
    </h1>

</header>

<style>
    header{
        background-color: #d8dadc;
        padding: 1%;
    }
    h1{
        margin: 0;
        text-align: center;
    }
    img{
        max-width: 100%;
        height: 100%;
    }
</style>