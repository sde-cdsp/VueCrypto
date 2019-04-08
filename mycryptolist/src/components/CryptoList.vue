<template>
    <div>
        <div class="search_bar">
            <div id="add_crypto" style="display: flex; align-items: center">
                <input class="search" type="text" placeholder="Search cryptocurrency..." v-model="textSearch" @keyup.enter="loadData">
                <div class="ld-ext-right button" v-bind:class="{'running': loading}" @click="loadData">Search
                    <div class="ld ld-ring ld-spin" type="submit"></div>
                </div>
            </div>
        </div>
        <div>
            <v-btn color="green" dark @click="favoriteOnly = !favoriteOnly">
            <v-icon left dark large color="#FFDE03" v-text="favoriteClass"></v-icon>
            {{ favoriteText }}
            </v-btn>
        </div>

        <table class="unstriped">
            <thead>
                <tr class="headers">
                    <th>Coin</th>
                    <th>Price</th>
                    <th>Market Cap</th>
                    <th>24 hours change</th>
                    <th>Socials</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <Cryptorow v-for="(crypto, symbol) in cryptosSelected" class="row-coin" :key="symbol" v-bind="crypto" @delete="deleteCrypto(symbol)" @switchFav="switchFavorite(symbol)">
                </Cryptorow>
            </tbody>
        </table>
    </div>
</template>

<script>
import _ from 'lodash'
    import qs from 'qs'
    import Cryptorow from './Cryptorow.vue'
    import Vue from '../main.js'
    const api_url_default = "https://min-api.cryptocompare.com/data/pricemultifull?tsyms=USD";

    export default {
        name: 'CryptoList',
        components: {
            Cryptorow,
        },
        props: ['username'],
        data: () => {
            return {
                textSearch: "",
                loading: false,
                cryptos: {},
                favoriteOnly: false
            }
        },
        watch: {
            username: function () {
                this.initData();
                setInterval(() => this.refreshData(), 20000);
            },
        },
        mounted() {
            this.initData();
        },
        computed: {
            cryptosEmpty() {
                return Object.keys(this.cryptos).length === 0;
            },
            favoriteClass() {
                return this.favoriteOnly ? "star_border" : "star";
            },
            favoriteText() {
                return this.favoriteOnly ? "Show all" : "Show favorites";
            },
            cryptosSelected() {
                if (!this.favoriteOnly)
                    return this.cryptos;
                return _.filter(this.cryptos, crypto => crypto['favorite'] === true);
            }
        },
        methods: {
            getSymbols() {
                return Object.keys(this.cryptos)
            },
            cryptoInList(symbol) {
                if (this.getSymbols().includes(symbol)) {
                    this.$notify({
                        text: symbol + ' already in your list!',
                        type: 'warn',
                        group: 'notif'
                    });
                    return true;
                }
                return false;
            },
            loadData() {
                let symbol = this.textSearch.toUpperCase();
                if (this.cryptoInList(symbol))
                    return;
                this.loading = true;
                this.loadBackendData(symbol)
                .then(() => this.loadApiData(symbol))
                .catch(() => {})
                .finally(() => this.loading = false)
            },
            loadBackendData(symbol) {
                return this.axios.post('user_crypto',
                    qs.stringify({symbol: symbol}),
                    {
                        headers: {
                            'X-CSRFToken': window.$cookies.get('csrftoken'),
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                    }
                ).then((response) => {
                    this.cryptos[symbol] = {
                        urls: response['data']['urls'],
                        logo: response['data']['logo'],
                        symbol: symbol,
                    };
                }).catch(() => {
                    this.$notify({
                            text: 'This cryptocurrency does not exist.',
                            type: 'error',
                            group: 'notif'
                        });
                    return Promise.reject();
                    }
                )
            },
            loadApiData(symbol) {
                return this.axios.get(api_url_default,
                    {params:
                        {fsyms: symbol}
                    }).then(response => {
                        this.$notify({
                            text: this.textSearch.toUpperCase() + ' added',
                            type: 'success',
                            group: 'notif'
                        });
                        let obj = Object.values(response.data.RAW)[0];
                        let symbol = obj['USD']['FROMSYMBOL'];
                        let newCrypto = this.cryptos[symbol];
                        Object.assign(newCrypto, obj['USD']);
                        this.textSearch = "";
                })
            },
            deleteCrypto(crypto) {
                // delete on the frontend
                Vue.delete(this.cryptos, crypto);
                // delete on the backend
                this.axios.post(
                    'remove_crypto',
                    qs.stringify({symbol: crypto}),
                    {headers: {
                            'X-CSRFToken': window.$cookies.get('csrftoken'),
                            'Content-Type': 'application/x-www-form-urlencoded'}
                    }
                ).then(() =>
                    this.$notify({
                        text: crypto + ' deleted',
                        type: 'success',
                        group: 'notif'
                    })
                )
            },
            refreshData() {
                this.axios.get(api_url_default, {
                    params: {
                        fsyms: this.getSymbols().join()
                    }
                }).then(response => {
                    for (let obj of Object.values(response.data.RAW)) {
                        let res = obj['USD'];
                        let toUpdate = this.cryptos[res['FROMSYMBOL']];
                        Object.assign(toUpdate, {symbol: res['FROMSYMBOL']}, res);
                    }
                    this.$forceUpdate();
                })
            },
            initData() {
                this.axios.get('user_crypto')
                .then(response => {
                    this.cryptos = {};
                    if(response.data['username']) {
                        for (let crypto of response.data['cryptos'])
                            this.cryptos[crypto['symbol']] = {
                                'urls': crypto['urls'],
                                'logo': crypto['logo'],
                                'favorite': crypto['favorite'],
                            };
                    }
                })
                .finally(() => {
                    if (!this.cryptosEmpty)
                        this.refreshData();
                });
            },
            onConnect(username) {
                this.username = username;
                this.initData();
            },
            switchFavorite(symbol) {
                this.cryptosSelected[symbol].favorite = !this.cryptosSelected[symbol].favorite;
                this.$forceUpdate();
            },
        }
    }
</script>

<style scoped>

</style>