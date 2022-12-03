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
    import { loginUser }  from "../../api/firebase"
    import { ModalData } from "../../definitions/modalData"
    import { selectedMenuItem}  from "../../stores"
    import { MenuItem } from "../../definitions/menuItem"
  
    let modalData = new ModalData()
    let user: LoginUser = new LoginUser()
    let showProgress: boolean = false
    let isSuccess: boolean = false
  
    const onLoginButtotnClicked = () => {
      showProgress = true
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
      showProgress = false
    }
  </script>
  
  <div class="login-form">
    Login Form
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
      {#if !showProgress}
        <div class="login-button">
          <Button
            type="submit"
            kind="primary"
            disabled={user.email.length === 0 || user.password.length === 0}
            on:click={onLoginButtotnClicked}>Login</Button
          >
        </div>
      {:else}
        <ProgressBar helperText="Logging in..." />
      {/if}
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
    .login-form {
      padding: 10%;
      width: 100%;
      display: absolute;
      flex-direction: column;
      align-items: center;
      justify-content: center;
    }
    .login-button {
      margin: 10px;
      justify-content: center;
    }
  </style>
  