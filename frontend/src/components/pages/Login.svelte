<script lang="ts">
  import {
    Form,
    TextInput,
    PasswordInput,
    Button,
    Modal,
    ProgressBar,
  } from "carbon-components-svelte"
  import { LoginUser } from "../../definitions/user"
  import { loginUser } from "../../api/firebase"
  import { ModalData } from "../../definitions/modalData"
  import { ProgressBarData } from "../../definitions/progressBarData"
  import { selectedMenuItem } from "../../stores"
  import { MenuItem } from "../../definitions/menuItem"
  import CustomButton from "../common/CustomButton.svelte"

  let modalData = new ModalData()
  let progressBarData: ProgressBarData = new ProgressBarData(
    false,
    "Logging in..."
  )
  let user: LoginUser = new LoginUser()
  let isSuccess: boolean = false

  const onLoginButtotnClicked = () => {
    progressBarData.isPresent = true
    loginUser(user)
      .then((user: LoginUser) => {
        isSuccess = true
        onLoginComplete("Success😎! You are logged in.")
      })
      .catch((error: any) => {
        let errorMessage: string
        switch (error.code) {
          case "auth/wrong-password":
            errorMessage = `Password or email address is not correct.`
            break
          case "auth/user-not-found":
            errorMessage = `User with email address ${user.email} not found. Try registering first.`
            break
          default:
            errorMessage = error.message
            break
        }
        onLoginComplete(errorMessage)
      })
  }

  function onLoginComplete(message: string) {
    console.log(message)
    modalData.messageBody = message
    modalData.isOpen = true
    progressBarData.isPresent = false
  }
</script>


<div class="login-title"><h>Login Form</h></div>
<div class="login-form">
  <Form
    on:submit={(e) => {
      e.preventDefault()
    }}
  >
    <TextInput
      id="email"
      labelText="Email"
      placeholder="Email"
      type="text"
      required
      bind:value={user.email}
    />
    <PasswordInput
      id="password"
      labelText="Password"
      placeholder="Password"
      type="password"
      required
      bind:value={user.password}
    />
    {#if !progressBarData.isPresent}
      <div class="login-button">
        <CustomButton
          type={"secondary"}
          disabled={user.email.length === 0 || user.password.length === 0}
          on:click={onLoginButtotnClicked}>Login</CustomButton
        >
      </div>
    {:else}
      <ProgressBar helperText={progressBarData.text} />
    {/if}
    <div class="not_registered_yet">
      <p>Not registered yet?</p> <a
        href="/"
        on:click|preventDefault={() => ($selectedMenuItem = MenuItem.REGISTER)}
        >Register</a
      >
    </div>
  </Form>
  <Modal
    passiveModal
    bind:open={modalData.isOpen}
    modalHeading={modalData.messageHeader}
    on:close={() => {
      modalData.isOpen = false
      if (isSuccess) {
        $selectedMenuItem = MenuItem.HOME
      }
    }}>{modalData.messageBody}</Modal
  >
</div>

<style lang="scss">

  a{
    font-size: 100%;
    padding-top: 5%;
    padding-bottom: 5%;
  }

  p{
    font-size: 100%;
    padding-top: 5%;
    padding-bottom: 1%;
  }

  h{
    font-size: 200%;
    
  }

  .login-title {
    padding: 5%;
    color: #063d79;
    font-weight: 500;
  }

  .login-form {
    padding: 1%;
    width: 40%;
    margin-left: auto;
    margin-right: auto;
    display: absolute;
    align-items: center;
    justify-content: center;
    
  }
  .login-button {
    margin: auto;
    justify-content: center;
    padding-top: 15%;
    padding-bottom: 1%;
    font-size: 120%;
  }
</style>
