<template>
    <div class="login_form">fe
        <router-view @connect="onConnect"></router-view>
    </div>
</template>

<script>
    export default {
        name: "TemplateLogin",

        methods: {
            onConnect(username) {
                this.$emit('connect', username)
            }
        }
    }

</script>

<style scoped>

</style>