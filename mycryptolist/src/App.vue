<template>
    <div>
        <h3 class="text-center"><router-link to="/">Cryptocurrencies Pricing</router-link></h3>
        <hr/>
        <div class="subhead">
            <notifications group="notif"></notifications>
            <div v-if="isConnected">
                <div class="float-right">Welcome {{username}}</div>&nbsp;
                <div><a class="float-right" @click="logout">Log out</a></div>
            </div>
        </div>
        <router-view :username="username" @connect="onConnect"></router-view>
    </div>

</template>

<script>

    import CryptoList from './components/CryptoList.vue'
    import axios from 'axios';
    import LoginForm from './utils/utils.js'

    export default {
        name: 'App',
        components: {
            CryptoList,
        },
        data: () => {
            return {
                username: "",
            }
        },
        computed: {
            isConnected() {
                return this.username.length > 0;
            }
        },
        mounted() {
            this.axios.get('get_user_connected/').then(response => this.username = response['data']['username']);
        },
        methods: {
            onConnect(username) {
                this.username = username;
            },
            logout() {
                let form = new LoginForm();
                return axios.post('logout/', {}, form.headers())
                .then(() => {
                    this.username = "";
                    this.$notify({
                            group: 'notif',
                            text: 'You are successfully logged out',
                            type: 'success'
                        });
                    this.$router.push('/login')
                })
                .catch(error => {
                    this.errors = error.response.data.error;
                    reject();
                })
            }
        }
    }
</script>
