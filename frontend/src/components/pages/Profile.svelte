<script lang="ts">
 import CustomButton from "../common/CustomButton.svelte"
 import ImageButton from "../common/ImageButton.svelte"
 import { ProgressBarData } from "../../definitions/progressBarData"
 import { getAuth } from "firebase/auth"
 import {
    selectedMenuItem,
    authUserStore,
    loginUserStore,
    networksList,
    selectedNetworkIndex,
    fetchedNetworkOnce
    } from "../../stores"
 import { MenuItem } from "../../definitions/menuItem"
 import Home from "../pages/Home.svelte"
    import { debug } from "svelte/internal";
 let progressBarData: ProgressBarData = new ProgressBarData(true, "Loading Profile...")

 let user = localStorage.getItem("loginUser")
    ? JSON.parse(localStorage.getItem("loginUser"))
    : undefined
 let username = user.email.split("@")[0]
 let profileImage
 let InputE1     
 export const performLogout = () => {
    progressBarData.text = "Logging out..."
    progressBarData.isPresent = true
    console.log(getAuth().currentUser)

    getAuth()
      .signOut()
      .then(() => {
        console.log("User signed out")
        $authUserStore = undefined
        $loginUserStore = undefined
        $networksList = []
        progressBarData.isPresent = false
        $selectedMenuItem = MenuItem.HOME
        $fetchedNetworkOnce = false
      })
      .catch((error) => {
        console.log(`Error while signing out: ${error}`)
        progressBarData.isPresent = false
      })
  }


  const handleProfileEdit = (event) => {
    const file = event.target.files[0];

    profileImage = URL.createObjectURL(file);
  }

  const onClickProfileEdit =() =>{
    console.log("Clicking");
    
    InputE1.click()
  }
</script>


<style lang="scss">
    /* Some basic styles to make the page look presentable */
    h1 {
      font-size: 2em;
      object-fit: cover;
      object-position: center;
    }
  
    p {
      font-size: 1.2em;
    }

    img {
    border-radius: 50%;
    width: 200px;
    height: 200px;
    object-fit: cover;
    object-position: center;
  }

  .ProfileImage{
    position: relative;
    justify-content: center;
    padding-top: 20px;
    padding-bottom: 20px;
  }
  </style>

  <div>
    
    <h1>Hello: {username}</h1>

  </div>
  <div class="ProfileImage">
    {#if profileImage}
        <img src={profileImage}/>
    {:else}
        <img src= "https://eu.ui-avatars.com/api/?name={username}&size=250"/>
    {/if}
    <input type="file" accept="image/*" style="display:none" on:change={handleProfileEdit} bind:this={InputE1} />
    <ImageButton
        defaultImageSource='https://cdn-icons-png.flaticon.com/32/1828/1828270.png'
        position='absolute'
        on:click ={onClickProfileEdit}></ImageButton>
    </div>
    <div>
    <CustomButton
          type={"secondary"}
          on:click={ performLogout }>Logout</CustomButton>
    
  </div>