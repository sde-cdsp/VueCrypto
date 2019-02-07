<template>
    <div class="register_form">
        <router-link style="float: right" to="/">Back to login</router-link>
        <input type="text" id="email" name="email" placeholder="Email" v-model="form.email">
        <input type="text" id="username" name="username" placeholder="Username" v-model="form.username">
        <input type="password" id="password1" name="password1" placeholder="Password" v-model="form.password1">
        <input type="password" id="password2" name="password2" placeholder="Confirm password" v-model="form.password2">
        <span id="error-login" class="form-error is-visible" v-text="this.form.errorstoString()"></span>
        <div class="btn btn-lg ld-ext-right button" v-bind:class="{'running': form.isLoading}" :disabled=form.isFormDisabled() @click="register">Register
            <div id="register-button" type="submit" class="ld ld-ring ld-spin"></div>
        </div>
    </div>
</template>

<script>

    import Form from '../../utils/utils.js'
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
                form: new RegisterForm({
                    username: '',
                    password1: '',
                    password2: '',
                    email: ''
                }),
            }
        },

        methods: {
            register() {
                this.form.isLoading = true;
                return axios.post('', this.form.userData(), this.form.headers())
                .then(() => {
                    this.$notify({
                            group: 'notif',
                            text: 'You successfully registered as ' + this.form.username,
                            type: 'success'
                        });
                    this.$router.push('/');
                })
                .catch(error => {
                    this.form.errors = error.response.data.error;
                })
            },
        }
    }

</script>

<style scoped>

</style>