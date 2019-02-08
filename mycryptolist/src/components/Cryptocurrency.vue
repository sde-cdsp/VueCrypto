<template>
    <div class="coin-container">
        <span style="font-weight: bold"> {{ symbol }} {{ logo }}</span>
        <span>
            <span display="isReady" class="price" :class="coinClass">{{ price }}$</span>
        </span>
        <span display="isReady" :style="{color: dayChangeColor}">{{ change24Hour }}%</span>
        <span>
            <div v-for="social in socials">
                <v-img :src=social></v-img>
            </div>
        </span>
        <v-btn color="blue" dark @click="dialog = true" small>X</v-btn>
        <v-dialog v-model="dialog" max-width="290">
            <v-card>
                <v-card-title class="headline">Delete {{symbol}} from your list?</v-card-title>
                <v-card-actions>
                    <v-btn color="red darken-1" flat="flat" @click="dialog = false">Cancel</v-btn>
                    <v-btn color="green darken-1" flat="flat" @click="deleteCrypto(symbol)">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>
    export default {
        name: "Cryptocurrency",

        props: ['symbol', 'result', 'logo', 'socials'],

        data: function () {
            return {
                coinUp: undefined,
                dialog: false
            };
        },

        computed: {
            dayChangeColor: function () {
                return (this.result.CHANGE24HOUR > 0) ? "green" : "red";
            },
            change24Hour: function () {
                return this.roundPrice(this.result.CHANGEPCT24HOUR, 3);
            },
            price: function () {
                return this.roundPrice(this.result.PRICE, 4);
            },
            coinClass: function () {
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

            deleteCrypto(symbol) {
                this.dialog = false;
                this.$emit('delete', symbol);
            }
        }
    };
</script>

<style scoped>

</style>