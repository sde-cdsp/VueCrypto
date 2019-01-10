<template>
    <div>
        <div v-for="crypto in cryptos" v-bind:key="crypto.name" >
            <div class="card" :id="crypto.name">
                <cryptocurrency :result="crypto.result" :name="crypto.name" @delete="deleteCrypto($event)"></cryptocurrency>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "CryptoList",
};

</script>

<style scoped>

</style>