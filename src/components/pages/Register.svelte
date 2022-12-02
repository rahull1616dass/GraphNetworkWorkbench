<script lang="ts">
  import {
    Form,
    TextInput,
    PasswordInput,
    Button,
    Modal,
    ProgressBar,
  } from "carbon-components-svelte"
  import { User, type UserLogin } from "../../definitions/user"
  import * as EmailValidator from "email-validator"
  import { registerUser } from "../../api/firebase"
  import { ModalData } from "../../definitions/modalData"
  import { selectedMenuItem}  from "../../stores"
  import { MenuItem } from "../../definitions/menuItem"

  let modalData = new ModalData()
  let user: User = new User()
  let isPasswordInvalid: boolean = false
  let isPasswordShort: boolean = false
  let doPasswordsMatch: boolean = false
  let isEmailInvalid: boolean = false
  let showProgress: boolean = false
  $: doPasswordsMatch =
    user.password &&
    user.passwordConfirm &&
    user.password !== user.passwordConfirm
  $: isPasswordShort = user.password && user.password.length < 8
  $: isPasswordInvalid = isPasswordShort || doPasswordsMatch
  $: isEmailInvalid =
    user.email.length > 4 && !EmailValidator.validate(user.email)

  const onRegisterButtonClicked = () => {
    showProgress = true
    registerUser(user)
      .then((user: User) => {
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
    showProgress = false
  }
</script>

<div class="register-form">
  Register Form
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
      invalid={doPasswordsMatch}
      bind:value={user.passwordConfirm}
    />
    {#if !showProgress}
      <div class="register-button">
        <Button
          type="submit"
          kind="primary"
          disabled={user.email.length < 5 ||
            isPasswordInvalid ||
            isEmailInvalid}
          on:click={onRegisterButtonClicked}>Register</Button
        >
      </div>
    {:else}
      <ProgressBar helperText="Registering user..." />
    {/if}
  </Form>
  <Modal
    passiveModal
    bind:open={modalData.isOpen}
    modalHeading={modalData.messageHeader}
    on:close={() => {
      modalData.isOpen = false
      $selectedMenuItem = MenuItem.HOME
    }}>{modalData.messageBody}</Modal
  >
</div>

<style lang="scss">
  .register-form {
    padding: 10%;
    width: 100%;
    display: absolute;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  .register-button {
    margin: 10px;
    justify-content: center;
  }
</style>
