<template>
    <div class="text-center">
    <div class="password_form">
        <span>Hi {{this.form.username}}. Change your password.</span>
        <input type="password" id="new_password1" name="new_password1" placeholder="Password" v-model="form.new_password1">
        <input type="password" id="new_password2" name="new_password2" placeholder="Confirm password" v-model="form.new_password2">
        <span id="error-login" class="form-error is-visible" v-text="this.form.errorstoString()"></span>
        <div class="ld-ext-right button" v-bind:class="{'running': form.isLoading}" :disabled=form.isFormDisabled() @click="resetPassword">Reset
            <div id="register-button" type="submit" class="ld ld-ring ld-spin"></div>
        </div>
        <router-link style="float: right;" to="/login">Back to login</router-link>
    </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Form from '../../utils/utils.js'

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
                    key: '',
                    new_password1: '',
                    new_password2: ''
                }),
            }
        },
        created() {
            this.form.username = this.$route.query.username;
            this.form.key = this.$route.query.key;
        },
        methods: {
            resetPassword() {
                this.form.isLoading = true;
                return axios.post('password_reset/', this.form.userData(), this.form.headers())
                    .then(() => {
                        this.$notify({
                            group: 'notif',
                            text: 'Your password has been changed ' + this.form.username,
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