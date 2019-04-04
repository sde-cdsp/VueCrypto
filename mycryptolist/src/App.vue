<template>
    <div>
        <h3 class="text-center"><router-link to="/">Cryptocurrencies Pricing</router-link></h3>
        <hr/>
        <div class="subhead">
            <notifications group="notif"></notifications>
        </div>

        <router-view :username="username" @connect="onConnect"></router-view>
    </div>
</template>

<script>

    import CryptoList from './components/CryptoList.vue'
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
        created() {
            this.axios.get('get_user_connected/').then(response => {
                this.username = response['data']['username'];
            });
        },
        methods: {
            onConnect(username) {
                this.username = username;
            },
        }
    }
</script>
