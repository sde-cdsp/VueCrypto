<template>
    <div class="login_form">
        <div v-if="connected">
            <span>Welcome {{username}}</span>&nbsp;<a style="float: right;" @click="logout">Log out</a>
        </div>
        <div v-else-if="displayForm">
            <input type="text" id="username" name="username" placeholder="Username" v-model="username">
            <input type="password" id="password" name="password" placeholder="Password" v-model="password">
            <button id="login-button" type="submit" class="button" :disabled=isLoginDisabled @click="login">Log in</button>&nbsp;<a style="float: right;" @click="displayForm = !displayForm">Forgot your password?</a>
        </div>
        <div v-else>
            <span>A new password will be sent to the email associated with your username</span>
            <input type="text" id="newpassword" name="newpassword" placeholder="Your username">
            <button id="password-button" type="submit" class="button">Submit</button><a style="float: right;" @click="displayForm = !displayForm">back to login</a>
        </div>
    </div>
</template>



<script>
    const qs = require('qs');

    export default {
        name: "Login",
        data: function () {
            return {
                csrfToken: "",
                connected: false,
                displayForm: true,
                username: "",
                password: ""
            }
        },
        computed: {
            isLoginDisabled() {
                return this.username.length == 0 || this.password.length == 0
            }
        },
        methods: {
            login() {
                const data = {
                            username: this.username,
                            password: this.password
                };
                this.axios.post(
                    'login/',
                    qs.stringify(data),
                    {
                        headers: {
                            'X-CSRFToken': this.$cookie.get('csrftoken'),
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    }
                    )
                    .catch(error => {
                        console.log(error);
                    })
                    .then(response => {
                        this.connected = true;
                });
            },
            logout() {
                this.connected = false;
                this.displayForm = true;
                this.username = this.password = "";
            }
        }
    }
</script>

<style scoped>

</style>