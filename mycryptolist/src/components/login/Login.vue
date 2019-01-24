<template>
    <div class="login_form">
        <div v-if="connected">
            <span>Welcome {{loginForm.username}}</span>&nbsp;<a style="float: right;" @click="logout">Log out</a>
        </div>
        <div v-else-if="loginForm.displayForm">
            <input type="text" id="username" name="username" placeholder="Username" v-model="loginForm.username">
            <input type="password" id="password" name="password" placeholder="Password" v-model="loginForm.password">
            <span id="error-login" class="form-error" v-bind:class="{'is-visible': loginForm.error}" v-text="loginForm.error"></span>
            <button id="login-button" type="submit" class="button" :disabled=loginForm.isLoginDisabled() @click="login">Log in</button>&nbsp;<a style="float: right;" @click="loginForm.switchDisplay()">Forgot your password?</a>
        </div>
        <div v-else>
            <span>A new password will be sent to the email associated with your username</span>
            <input type="text" id="newpassword" name="newpassword" placeholder="Your username">
            <button id="password-button" type="submit" class="button">Submit</button><a style="float: right;" @click="loginForm.switchDisplay()">back to login</a>
        </div>
    </div>
</template>



<script>
    import qs from 'qs';
    import axios from 'axios';

    class LoginForm {
        constructor(data) {
            for (let field in data) {
                this[field] = data[field];
            }
            this.displayForm = true;
            this.error = "";
            this.isLoading = false;
        }

        userData() {
            const data = {
                username: this.username,
                password: this.password
            };
            return qs.stringify(data);
        }

        headers() {
            return {
                headers: {
                            'X-CSRFToken': window.$cookies.get('csrftoken'),
                            'Content-Type': 'application/x-www-form-urlencoded'
                }
            }
        }

        reset() {
            this.displayForm = true;
            this.username = this.password = this.error = "";
        }

        switchDisplay () {
            this.displayForm = !this.displayForm;
        }

        isLoginDisabled() {
            return this.username.length === 0 || this.password.length === 0
        }

        login() {
            this.isLoading = true;
            return new Promise((resolve, reject) => {  // a Promise is returned to handle Vue related data
                axios.post('login/', this.userData(), this.headers())
                .then(() => {
                    resolve();
                })
                .catch(error => {
                    this.error = error.response.data.error;
                    reject(error.response.data);
                })
            });
        }
        logout() {
            this.isLoading = true;
            return new Promise((resolve, reject) => {
                axios.post('logout/', {}, this.headers())
                .then(() => {
                    this.reset();
                    resolve();
                })
                .catch(error => {
                    this.error = error.response.data.error;
                    reject(error.response.data);
                })
            });
        }

    }

    export default {
        name: "Login",
        data: function () {
            return {
                loginForm: new LoginForm({
                    username: '',
                    password: ''
                }),
                connected: false
            }
        },

        methods: {
            login() {
                const self = this;
                this.loginForm.login()
                    .then(() => this.connected = true)
                    .catch((error) => console.log(error))
                    .finally(() => self.loginForm.isLoading = false) // FIXME: not working!
            },
            logout() {
                this.loginForm.logout()
                    .then(() => this.connected = false)
                    .catch((error) => console.log(error))
                    .finally(() => self.loginForm.isLoading = false) // FIXME: not working!
            }
        }
    }
</script>

<style scoped>

</style>