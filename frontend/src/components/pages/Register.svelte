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
  import * as EmailValidator from "email-validator"
  import { registerUser } from "../../api/firebase"
  import { ModalData } from "../../definitions/modalData"
  import { ProgressBarData } from "../../definitions/progressBarData"
  import { selectedMenuItem}  from "../../stores"
  import { MenuItem } from "../../definitions/menuItem"
  import CustomButton from "../common/CustomButton.svelte"

  let modalData = new ModalData()
  let progressBarData: ProgressBarData = new ProgressBarData(false, "Registering user...")
  let user: LoginUser = new LoginUser()
  let isPasswordInvalid: boolean = false
  let isPasswordShort: boolean = false
  let doPasswordsMatch: boolean = false
  let isEmailInvalid: boolean = false
  $: doPasswordsMatch =
    user.password &&
    user.passwordConfirm &&
    user.password === user.passwordConfirm
  $: isPasswordShort = user.password && user.password.length < 8
  $: isPasswordInvalid = isPasswordShort || !doPasswordsMatch
  $: isEmailInvalid =
    user.email.length > 4 && !EmailValidator.validate(user.email)

  const onRegisterButtonClicked = () => {
    progressBarData.isPresent = true
    registerUser(user)
      .then(() => {
        onRegisterComplete("Success😎! You can now log in.")
      })
      .catch((error: any) => {
        let errorMessage: string
        switch (error.code) {
          case "auth/email-already-in-use":
            errorMessage = `Email address ${user.email} already in use.`
            break
          case "auth/invalid-email":
            errorMessage = `Email address ${user.email} is invalid.`
            break
          case "auth/operation-not-allowed":
            errorMessage = `Email/password accounts are not enabled.`
            break
          case "auth/weak-password":
            errorMessage = `Password is too weak.`
            break
          default:
            errorMessage = error.message
            break
        }
        onRegisterComplete(errorMessage)
      })
  }

  function onRegisterComplete(message: string) {
    console.log(message)
    modalData.messageBody = message
    modalData.isOpen = true
    progressBarData.isPresent = false
  }
</script>
<div class="register-title"><h>Register Form</h></div>
<div class="register-form">
  
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
      invalidText="Email is invalid"
      invalid={isEmailInvalid}
      bind:value={user.email}
    />
    <PasswordInput
      id="password"
      labelText="Password"
      placeholder="Password"
      type="password"
      required
      invalidText="Password should be at least 8 characters long"
      invalid={isPasswordShort}
      bind:value={user.password}
    />
    <PasswordInput
      id="password"
      labelText="Confirm Password"
      placeholder="Confirm Password"
      type="password"
      required
      invalidText="Passwords do not match"
      invalid={!isPasswordInvalid && !doPasswordsMatch}
      bind:value={user.passwordConfirm}
    />
    {#if !progressBarData.isPresent}
      <div class="register-button">
        <CustomButton
          type="secondary"
          disabled= {user.email.length < 5 ||
            isPasswordInvalid ||
            isEmailInvalid}
          on:click={onRegisterButtonClicked}>Register</CustomButton
        >
      </div>
    {:else}
      <ProgressBar helperText={progressBarData.text} />
    {/if}
    <div class="already_registered">
      <p>Already registered?</p> <a
        href="/"
        on:click|preventDefault={() => ($selectedMenuItem = MenuItem.LOGIN)}
        >Login</a
      >
    </div>
  </Form>
  <Modal
    passiveModal
    bind:open={modalData.isOpen}
    modalHeading={modalData.messageHeader}
    on:close={() => {
      modalData.isOpen = false
      $selectedMenuItem = MenuItem.REGISTER
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

  .register-title {
    padding: 5%;
    color: #063d79;
    font-weight: 500;
  }

  .register-form {
    padding: 1%;
    width: 40%;
    margin-left: auto;
    margin-right: auto;
    display: absolute;
    align-items: center;
    justify-content: center;
  }
  .register-button {
    margin: auto;
    justify-content: center;
    padding-top: 15%;
    padding-bottom: 1%;
    font-size: 120%;
  }
</style>
