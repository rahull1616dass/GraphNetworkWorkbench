<script lang="ts">
 import CustomButton from "../common/CustomButton.svelte"
 import { ProgressBarData } from "../../definitions/progressBarData"
 import { getAuth } from "firebase/auth"
 import {
    selectedMenuItem,
    authUserStore,
    loginUserStore,
    networksList,
    selectedNetworkIndex,
    } from "../../stores"
 import { MenuItem } from "../../definitions/menuItem"
 import Home from "../pages/Home.svelte"
 let progressBarData: ProgressBarData = new ProgressBarData(true, "Loading Profile...")

 let user = localStorage.getItem("loginUser")
    ? JSON.parse(localStorage.getItem("loginUser"))
    : undefined

    
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
      })
      .catch((error) => {
        console.log(`Error while signing out: ${error}`)
        progressBarData.isPresent = false
      })
  }
</script>


<style lang="scss">
    /* Some basic styles to make the page look presentable */
    h1 {
      font-size: 2em;
    }
  
    p {
      font-size: 1.2em;
    }
  </style>




  <div>
    
    <h1>{user.email}</h1>

    <CustomButton
          type={"secondary"}
          on:click={ performLogout }>Logout</CustomButton>
  </div>