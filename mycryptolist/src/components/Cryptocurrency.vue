<template>
    <div class="coin-container">
        <span class="coin large-3 columns" style="font-weight: bold;"> {{ name }}</span>
        <span class="large-3 columns">
            <span display="isReady" class="price" :class="coinClass">{{ price }}$</span>
        </span>
        <span display="isReady" class="large-3 columns" :style="{color: dayChangeColor}">{{change24Hour}}%</span>
        <a class="box-delete large-3 columns" href="#" @click="$emit('delete', name)">x</a>
    </div>
</template>

<script>
    export default {
        name: "Cryptocurrency",

        props: ['name', 'result'],

        data: function () {
        return {
            'coinUp': undefined,
            };
        },

        computed: {
        dayChangeColor: function() {
            return (this.result.CHANGE24HOUR > 0) ? "green" : "red";
        },
        change24Hour: function() {
            return this.roundPrice(this.result.CHANGEPCT24HOUR, 3);
        },
        price: function() {
            return this.roundPrice(this.result.PRICE, 4);
        },
        coinClass:  function() {
            if (this.coinUp === undefined)
                return "coin-even";
            else if (this.coinUp)
                return "coin-up";
            else
                return "coin-down";
        },
        isReady() {
            return this.result.hasOwnProperty("PRICE");
        }
    },
    watch: {
        'result.PRICE': function (val, oldVal) {
            this.coinUp = (val >= oldVal);
        }
    },
    methods: {
        roundPrice: (p, n) => Number(p.toPrecision(n)),
        // deleteCrypto() {}
    }
};
</script>

<style scoped>

</style>