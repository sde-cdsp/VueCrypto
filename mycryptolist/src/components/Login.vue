<template>
    <div class="login_form">
        <div v-if="connected">
            <span>Welcome {{loginForm.username}}</span>&nbsp;<a style="float: right;" @click="logout">Log out</a>
        </div>
        <div v-else-if="loginForm.displayForm">
            <router-link style="float: right" to="/register/">Register</router-link>
            <input type="text" id="id_username" name="username" placeholder="Username" v-model="loginForm.username">
            <input type="password" id="id_password" name="password" placeholder="Password" v-model="loginForm.password">
            <span id="error-login" class="form-error" v-bind:class="{'is-visible': loginForm.error}" v-text="loginForm.error"></span>
            <div class="btn btn-lg ld-ext-right button" v-bind:class="{'running': loginForm.isLoading}" :disabled=loginForm.isFormDisabled() @click="login">Log in
                <div id="login-button" type="submit" class="ld ld-ring ld-spin"></div>
            </div>
            &nbsp;<a style="float: right;" @click="loginForm.switchDisplay()">Forgot your password?</a>
        </div>
        <div v-else>
            <span>A new password will be sent to the email associated with your username</span>
            <input type="text" id="newpassword" name="newpassword" placeholder="Your username">
            <button id="password-button" type="submit" class="button">Submit</button><a style="float: right;" @click="loginForm.switchDisplay()">back to login</a>
        </div>
    </div>
</template>


<script>

    import axios from 'axios';
    import Form from '../utils/utils.js'

    class LoginForm extends Form {
        constructor(data) {
            super(data);
        }

        defaultData() {
            return {
                username: '',
                password: ''
            }
        }

        login() {
            return new Promise((resolve, reject) => {  // a Promise is returned to handle Vue related data
                this.isLoading = true;
                return axios.post('login/', this.userData(), this.headers())
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
                    this.reset(this.defaultData());
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
                this.loginForm.login()
                    .then(() => {
                        this.connected = true;
                        this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged in',
                            type: 'success'
                        });
                    })
                    .catch(error => console.log(error))
                    .finally(() => this.loginForm.isLoading = false)
            },
            logout() {
                this.loginForm.logout()
                    .then(() => {
                        this.connected = false;
                        this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged out',
                            type: 'success'
                        });
                    })
                    .catch(error => console.log(error))
                    .finally(() => this.loginForm.isLoading = false)
            }
        }
    }

</script>

<style scoped>

</style>