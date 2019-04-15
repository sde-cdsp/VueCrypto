<template>
    <div class="text-center">
        <div class="login_form">
            <router-link style="float: right" to="/register/">Register</router-link>
            <input type="text" id="id_username" name="username" placeholder="Username" v-model="form.username">
            <input type="password" id="id_password" name="password" placeholder="Password" v-model="form.password">
            <span id="error-login" class="form-error is-visible" v-text="this.form.errorstoString()"></span>
            <div class="ld-ext-right button" v-bind:class="{'running': form.isLoading}" :disabled=form.isFormDisabled() @click="login">Log in
                <div id="login-button" type="submit" class="ld ld-ring ld-spin"></div>
            </div>
            &nbsp;<router-link style="float: right;" to="/ask_password_reset/">Forgot your password?</router-link>
        </div>
    </div>
</template>


<script>
    import axios from 'axios';
    import Form from '../../utils/utils.js'

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
            this.isLoading = true;
            return new Promise((resolve, reject) => {  // a Promise is returned to handle Vue related data
                return axios.post('login/', this.userData(), this.headers())
                .then((response) => {
                    resolve(response);
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
                .then((response) => {
                    this.reset(this.defaultData());
                    resolve(response);
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

        props: {
            username: {
                type: String,
                default: ''
            }
        },

        data: () => {
            return {
                form: new LoginForm({
                    username: '',
                    password: ''
                }),
            }
        },
        methods: {
            login() {
                this.form.login()
                    .then((response) => {
                        this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged in',
                            type: 'success'
                        });
                        this.$emit('connect', response['data']['username']);
                        this.$router.push({path: "/", query: {username: response['data']['username']}});
                    })
                    .catch(() => this.form.isLoading = false)
                    .finally(() => this.form.isLoading = false)
            },
            logout() {
                this.form.logout()
                    .then((response) => {
                        this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged out',
                            type: 'success'
                        });
                        this.$emit('connect', response.data['username']);
                        this.$router.push('/login')
                    })
                    .catch(() => this.form.isLoading = false)
                    .finally(() => this.form.isLoading = false)
            }
        }
    }

</script>

<style scoped>

</style>