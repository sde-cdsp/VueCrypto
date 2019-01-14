<template>
    <div class="login_form">
        <h5 class="text-center">Login</h5>
        <div v-if="displayForm">
            <input type="text" id="username" name="username" placeholder="Username">
            <input type="password" id="password" name="password" placeholder="Password">
            <button id="login-button" type="submit" class="button">Log in</button>&nbsp;<a style="float: right;" href="#" @click="displayForm = !displayForm">Forgot your password?</a>
        </div>
        <div v-if="!displayForm" style="">
            <span>A new password will be sent to the email associated with your username</span>
            <input type="text" id="newpassword" name="newpassword" placeholder="Your username">
            <button id="password-button" type="submit" class="button">Submit</button><a style="float: right;" @click="displayForm = !displayForm">back to login</a>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Login",
        data: function () {
            return {
                displayForm: true,
            }
        },
        methods: {
            login() {
                this.axios.get(api_url_default, {
                    params: {
                        fsyms: this.textSearch.toUpperCase()
                    }
                }).then(response => {
        }
    }
</script>

<style scoped>

</style>