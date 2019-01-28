<template>
    <div class="register_form">
        <router-link style="float: right" to="/">Back to login</router-link>
        <input type="text" id="email" name="email" placeholder="Email" v-model="registerForm.email">
        <input type="text" id="username" name="username" placeholder="Username" v-model="registerForm.username">
        <input type="password" id="password1" name="password1" placeholder="Password" v-model="registerForm.password1">
        <input type="password" id="password2" name="password2" placeholder="Confirm password" v-model="registerForm.password2">
        <span id="error-login" class="form-error is-visible" v-text="this.errorstoString"></span>
        <div class="btn btn-lg ld-ext-right button" v-bind:class="{'running': registerForm.isLoading}" :disabled=registerForm.isFormDisabled() @click="register">Register
            <div id="register-button" type="submit" class="ld ld-ring ld-spin"></div>
        </div>
    </div>
</template>

<script>

    import Form from '../utils/utils.js'
    import axios from 'axios'

    class RegisterForm extends Form {
        constructor(data) {
            super(data)
        }
    }

    export default {
        name: "Register",

        data: () => {
            return {
                registerForm: new RegisterForm({
                    username: '',
                    password1: '',
                    password2: '',
                    email: ''
                }),
                errors: {}
            }
        },

        computed: {
            errorstoString() {
                let str = "";
                for (let field in this.errors) {
                    str += this.errors[field].join('\n');
                    str += '\n';
                }
                return str;
            }
        },

        methods: {
            register() {
                this.isLoading = true;
                return axios.post('register/', this.registerForm.userData(), this.registerForm.headers())
                .then(() => {
                    this.$notify({
                            group: 'notif',
                            text: 'You are successfully registered as ' + this.registerForm.username,
                            type: 'success'
                        });
                    this.$router.push('/');
                })
                .catch(error => {
                    this.errors = error.response.data.error;
                })
            },
        }
    }

</script>

<style scoped>

</style>