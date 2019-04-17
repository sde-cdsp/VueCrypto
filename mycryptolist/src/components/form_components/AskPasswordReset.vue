<template>
    <div class="text-center">
    <div class="password_form">
        <span>An email will be sent to the email associated with your username.</span>
        <input type="text" id="newpassword" name="newpassword" placeholder="Your username" v-model="form.username">
        <span id="error-login" class="form-error is-visible" v-text="this.form.errorstoString()"></span>
        <div class="ld-ext-right button" v-bind:class="{'running': form.isLoading}" :disabled=form.isFormDisabled() @click="askReset">Submit
            <div id="register-button" type="submit" class="ld ld-ring ld-spin"></div>
        </div>
        <router-link style="float: right;" to="/login">Back to login</router-link>
    </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Form from '../../utils/utils.js'

    class AskPasswordResetForm extends Form {
        constructor(data) {
            super(data);
        }
    }

    export default {
        name: "AskPasswordReset",
        data: () => {
            return {
                form: new AskPasswordResetForm({
                    username: '',
                }),
            }
        },
        methods: {
            askReset() {
                this.form.isLoading = true;
                return axios.post('ask_password_reset/', this.form.userData(), this.form.headers())
                    .then(() => {
                        this.$notify({
                            group: 'notif',
                            text: 'An email has been sent to the email associated with the username ' + this.form.username,
                            type: 'success'
                        });
                        this.$router.push('/login');
                    })
                    .catch((error) => this.form.errors = error.response.data.error)
                    .finally(() => this.form.isLoading = false)
            }
        }
    }
</script>

<style scoped>

</style>