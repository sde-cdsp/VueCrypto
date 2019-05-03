<template>
    <div>
        <router-view :username="username"></router-view>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Cryptosection",
        props: ['username'],

        beforeRouteEnter (to, from, next) {
            axios.get('get_user_connected/').then(response => {
                response['data']['username'].length === 0 ? next('/login') : next()
            });
        },
    }
</script>

<style scoped>

</style>