<template>
    <div class="login_form">
        <div v-if="connected">
            <span>Welcome {{form.username}}</span>&nbsp;<a style="float: right;" @click="logout">Log out</a>
        </div>
        <div v-else>
            <router-link style="float: right" to="/register/">Register</router-link>
            <input type="text" id="id_username" name="username" placeholder="Username" v-model="form.username">
            <input type="password" id="id_password" name="password" placeholder="Password" v-model="form.password">
            <span id="error-login" class="form-error is-visible" v-text="this.form.errorstoString()"></span>
            <div class="btn btn-lg ld-ext-right button" v-bind:class="{'running': form.isLoading}" :disabled=form.isFormDisabled() @click="login">Log in
                <div id="login-button" type="submit" class="ld ld-ring ld-spin"></div>
            </div>
            &nbsp;<router-link style="float: right;" to="/password_reset/">Forgot your password?</router-link>
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
                    this.errors = error.response.data.error;
                    reject();
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
                    this.errors = error.response.data.error;
                    reject();
                })
            });
        }
    }

    export default {
        name: "Login",
        data: () => {
            return {
                form: new LoginForm({
                    username: '',
                    password: ''
                }),
                connected: false
            }
        },

        methods: {
            login() {
                this.form.login()
                    .then(() => {
                        this.connected = true;
                        this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged in',
                            type: 'success'
                        });
                    })
                    .catch(() => this.form.isLoading = false)
                    .finally(() => this.form.isLoading = false)
            },
            logout() {
                this.form.logout()
                    .then(() => {
                        this.connected = false;
                        this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged out',
                            type: 'success'
                        });
                    })
                    .catch(() => this.form.isLoading = false)
                    .finally(() => this.form.isLoading = false)
            }
        }
    }

</script>

<style scoped>

</style>