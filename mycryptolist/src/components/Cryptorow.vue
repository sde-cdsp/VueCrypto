<template>
    <tr>
        <td style="font-weight: bold"><router-link to="/coin">{{ symbol }}&nbsp;</router-link><img width="10%" :src="logo"/></td>
        <td>
            <span display="isReady" class="price" :class="coinClass">{{ price }}$</span>
        </td>
        <td>${{ marketCap }}</td>
        <td display="isReady" :style="{color: dayChangeColor}">{{ change24Hour }}%</td>
        <td>
            <a v-for="(url, url_type) in this.urls" :href="url" style="margin-right: 2px;" :title="url_type"><img style="max-height: 1.5em; object-fit: fill;" :src=getImage(url_type)></a>
        </td>
        <td><v-btn color="blue" dark @click="dialog = true" small title="Delete">X</v-btn>&nbsp;
            <v-icon dark color="#FFDE03" v-text="favoriteClass" @click="switchFavorite" :title="favoriteTitle"></v-icon>
        </td>
        <v-dialog v-model="dialog" max-width="290">
            <v-card>
                <v-card-title class="headline">Delete {{ symbol }} from your list?</v-card-title>
                <v-card-actions>
                    <v-btn color="red darken-1" flat="flat" @click="dialog = false">Cancel</v-btn>
                    <v-btn color="green darken-1" flat="flat" @click="deleteCrypto">Confirm</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </tr>
</template>

<script>
    import publicPath from '../../vue.config'
    import Form from '../utils/utils.js'
    import qs from 'qs'
    import axios from 'axios';
    import numeral from 'numeral'

    export default {
        name: "Cryptocurrency",
        props: ["symbol", "favorite", "urls", "logo", "CHANGEPCT24HOUR", "CHANGE24HOUR", "PRICE", "MKTCAP"],

        data: function () {
            return {
                coinUp: undefined,
                dialog: false,
            };
        },

        computed: {
            marketCap() {
                return numeral(this.MKTCAP).format('0,0').replace(/,/g, ' ');
            },
            dayChangeColor() {
                return (this.CHANGE24HOUR > 0) ? "green" : "orangered";
            },
            change24Hour() {
                return this.CHANGEPCT24HOUR === undefined ? 0 : this.roundPrice(this.CHANGEPCT24HOUR, 3);
            },
            price() {
                return this.PRICE === undefined ? 0 : this.roundPrice(this.PRICE, 4);
            },
            coinClass() {
                if (this.coinUp === undefined)
                    return "coin-even";
                else if (this.coinUp)
                    return "coin-up";
                else
                    return "coin-down";
            },
            favoriteClass() {
                return this.favorite ? "star" : "star_border";
            },
            favoriteTitle() {
                return this.favorite ? "Add to starred coins" : "Remove from starred coins";
            },
            isReady() {
                return this.hasOwnProperty("PRICE");
            }
        },
        watch: {
            'PRICE': function (val, oldVal) {
                this.coinUp = (oldVal === undefined) ? undefined : (val >= oldVal);
            }
        },
        methods: {
            roundPrice: (p, n) => Number(p.toPrecision(n)),

            deleteCrypto() {
                this.dialog = false;
                this.$emit('delete', this.symbol);
            },

            getImage(url_type) {
                return `${publicPath.publicPath}img/${url_type}.png`;
            },

            switchFavorite() {
                let form = new Form();
                axios.post('favorite_crypto', qs.stringify({symbol: this.symbol}), form.headers())
                .then(() => {
                    this.$emit('switchFav', this.symbol);
                    let text = this.favorite ? `${this.symbol} removed from your favorite list` : `${this.symbol} added to your favorite list`;
                    this.$notify({
                        text: text,
                        type: 'success',
                        group: 'notif'
                    });
                })
            }
        }
    };
</script>

<style scoped>

</style>