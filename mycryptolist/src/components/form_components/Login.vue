<template>
    <div class="text-center">
        <div class="login_form">
            <router-link style="float: right" to="/register/">Register</router-link>
            <input type="text" id="id_username" name="username" placeholder="Username" v-model="form.username" @keyup.enter="login">
            <input type="password" id="id_password" name="password" placeholder="Password" v-model="form.password" @keyup.enter="login">
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

        login() {
            this.isLoading = true;
            return axios.post('login/', this.userData(), this.headers())
            .then((response) => {
                return Promise.resolve(response);
            })
            .catch(error => {
                this.errors = error.response.data.error;
                return Promise.reject(error);
            })
        }

        logout() {
            this.isLoading = true;
            return axios.post('logout/', {}, this.headers())
            .then((response) => {
                    this.reset(this.defaultData());
                    return Promise.resolve(response);
            })
            .catch(error => {
                    this.errors = error.response.data.error;
                    return Promise.reject(error);
            })
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
                        this.$emit('connect', response.data['username'])
                        this.$router.push("/");
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