<template>
    <div class="password_form">
        <span>An email will be sent to the email associated with your username.</span>
        <input type="text" id="newpassword" name="newpassword" placeholder="Your username" v-model="form.username">
        <span id="error-login" class="form-error is-visible" v-text="this.form.errorstoString()"></span>
        <button id="password-button" type="submit" class="button" v-bind:class="{'running': form.isLoading}" :disabled=form.isFormDisabled() @click="askReset">Submit</button>
        <router-link style="float: right;" to="/">back to login</router-link>
    </div>
</template>

<script>
    import axios from 'axios';
    import Form from '../utils/utils.js'

    class PasswordResetForm extends Form {
        constructor(data) {
            super(data);
        }
    }

    export default {
        name: "PasswordReset",
        data: () => {
            return {
                form: new PasswordResetForm({
                    username: '',
                }),
            }
        },
        methods: {
            askReset() {
                return axios.post('ask_reset_password/', this.form.userData(), this.form.headers())
                    .then(() => {
                        this.$notify({
                            group: 'notif',
                            text: 'An email has been sent to the email associated with the username ' + this.form.username,
                            type: 'success'
                        });
                        this.$router.push('/');
                    })
                    .catch((error) => this.form.errors = error.response.data.error)
            }
        }
    }
</script>

<style scoped>

</style>