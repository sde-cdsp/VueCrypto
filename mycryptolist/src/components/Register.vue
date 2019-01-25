<template>
    <div class="register_form">
        <router-link style="float: right" to="/login/">Back to login</router-link>
        <input type="text" id="email" name="email" placeholder="Email">
        <input type="text" id="username" name="username" placeholder="Username">
        <input type="password" id="password" name="password" placeholder="Password">
        <div class="btn btn-lg ld-ext-right button">Register
            <div id="register-button" type="submit" class="ld ld-ring ld-spin"></div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Register"
    }
</script>

<style scoped>

</style>