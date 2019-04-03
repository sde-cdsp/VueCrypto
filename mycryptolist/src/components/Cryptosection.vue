<template>
    <div>
        <h2>Crypto Section</h2>
        <router-view :username="username"></router-view>
    </div>
</template>

<script>
    export default {
        name: "Cryptosection",
        props: ['username']
    }
</script>

<style scoped>

</style>