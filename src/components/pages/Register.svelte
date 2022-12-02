<script lang="ts">
    import { Form, TextInput, PasswordInput, Button, ClickableTile } from "carbon-components-svelte"
    import  { User } from "../../definitions/user"
    import * as EmailValidator from "email-validator"

    let user: User = new User()
    let isPasswordInvalid: boolean = false
    let isPasswordShort: boolean = false
    let doPasswordsMatch: boolean = false
    let isEmailInvalid: boolean = false
    $: doPasswordsMatch = (user.password && user.passwordConfirm && user.password !== user.passwordConfirm)
    $: isPasswordShort = (user.password && user.password.length < 8)
    $: isPasswordInvalid = (isPasswordShort || doPasswordsMatch)
    $: isEmailInvalid = (user.email.length > 4 && !EmailValidator.validate(user.email))

    const onRegisterButtonClicked = () => {

    }
</script>

<div class="register-form">
    Register Form
    <Form>
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
        <Button
            type="submit"        
            kind="primary"
            disabled={user.email.length < 5 || isPasswordInvalid || isEmailInvalid}
            on:click={onRegisterButtonClicked}>Register</Button>
    </Form>
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

</style>