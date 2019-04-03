<template>
    <div>
        <h3 class="text-center"><router-link to="/">Cryptocurrencies Pricing</router-link></h3>
        <hr/>
        <div class="subhead">
            <notifications group="notif"></notifications>
            <!--<router-view :username="username" @connect="onConnect"></router-view>-->
        </div>

        <router-view ref="login" :username="username" @connect="onConnect"></router-view>
        <!--<router-view name="crypto"></router-view>-->
        <!--<div>-->
            <!--<v-btn color="green" dark @click="favoriteOnly = !favoriteOnly">-->
            <!--<v-icon left dark large color="#FFDE03" v-text="favoriteClass"></v-icon>-->
            <!--{{ favoriteText }}-->
            <!--</v-btn>-->
        <!--</div>-->

        <!--<table class="unstriped">-->
            <!--<thead>-->
                <!--<tr class="headers">-->
                    <!--<th>Coin</th>-->
                    <!--<th>Price</th>-->
                    <!--<th>Market Cap</th>-->
                    <!--<th>24 hours change</th>-->
                    <!--<th>Socials</th>-->
                    <!--<th>Actions</th>-->
                <!--</tr>-->
            <!--</thead>-->
            <!--<tbody>-->
                <!--<Cryptorow v-for="(crypto, symbol) in cryptosSelected" class="row-coin" v-bind="crypto" @delete="deleteCrypto(symbol)" @switchFav="switchFavorite(symbol)">-->
                <!--</Cryptorow>-->
            <!--</tbody>-->
        <!--</table>-->
    </div>
</template>

<script>
    // import _ from 'lodash'
    // import qs from 'qs'
    // import Cryptorow from './components/Cryptorow.vue'
    import CryptoList from './components/CryptoList.vue'
    // import Vue from './main.js'
    // const api_url_default = "https://min-api.cryptocompare.com/data/pricemultifull?tsyms=USD";
    //
    export default {
        name: 'App',
        components: {
    //         Cryptorow,
            CryptoList,
        },
        data: () => {
            return {
                username: "",
    //             cryptos: {},
    //             favoriteOnly: false
            }
        },
        created() {
            this.axios.get('get_user_connected/').then(response => {
                this.username = response['data']['username'];
            });
        },
    //     created() {
    //         this.axios.get('get_user_connected/').then(response => {
    //             this.username = response['data']['username'];
    //             this.initData();
    //         });
    //     },
    //     mounted() {
    //         setInterval(() => this.refreshData(), 20000);
    //     },
    //     computed: {
    //         cryptosEmpty() {
    //             return Object.keys(this.cryptos).length === 0;
    //         },
    //         favoriteClass() {
    //             return this.favoriteOnly ? "star_border" : "star";
    //         },
    //         favoriteText() {
    //             return this.favoriteOnly ? "Show all" : "Show favorites";
    //         },
    //         cryptosSelected() {
    //             if (!this.favoriteOnly)
    //                 return this.cryptos;
    //             return _.filter(this.cryptos, crypto => crypto['favorite'] === true);
    //         }
    //     },
        methods: {
    //         getSymbols() {
    //             return Object.keys(this.cryptos)
    //         },
    //         cryptoInList(symbol) {
    //             if (this.getSymbols().includes(symbol)) {
    //                 this.$notify({
    //                     text: symbol + ' already in your list!',
    //                     type: 'warn',
    //                     group: 'notif'
    //                 });
    //                 return true;
    //             }
    //             return false;
    //         },
    //         loadData() {
    //             let symbol = this.textSearch.toUpperCase();
    //             if (this.cryptoInList(symbol))
    //                 return;
    //             this.loadBackendData(symbol)
    //             .then(() => this.loadApiData(symbol))
    //         },
    //         loadBackendData(symbol) {
    //             return new Promise((resolve, reject) => {
    //                 this.axios.post('user_crypto',
    //                     qs.stringify({symbol: symbol}),
    //                     {
    //                         headers: {
    //                             'X-CSRFToken': window.$cookies.get('csrftoken'),
    //                             'Content-Type': 'application/x-www-form-urlencoded'
    //                         }
    //                     }
    //                 ).then((response) => {
    //                     this.cryptos[symbol] = {
    //                         urls: response['urls'],
    //                         logo: response['logo'],
    //                         symbol: symbol,
    //                     };
    //                     resolve()
    //                 })
    //             });
    //         },
    //         loadApiData(symbol) {
    //             this.axios.get(api_url_default,
    //                 {params: {
    //                     fsyms: symbol
    //                 }
    //             }).then(response => {
    //                 if (response.data["Response"] === "Error")
    //                     this.$notify({
    //                             text: 'This cryptocurrency does not exist.',
    //                             type: 'error',
    //                             group: 'notif'
    //                         });
    //                 else {
    //                     this.$notify({
    //                             text: this.textSearch.toUpperCase() + ' added',
    //                             type: 'success',
    //                             group: 'notif'
    //                         });
    //                     let obj = Object.values(response.data.RAW)[0];
    //                     let symbol = obj['USD']['FROMSYMBOL'];
    //                     this.cryptos[symbol] = obj['USD'];
    //                     this.cryptos[symbol]['symbol'] = symbol;
    //                     this.textSearch = "";
    //                 }
    //             })
    //         },
    //         deleteCrypto(crypto) {
    //             // delete on the frontend
    //             Vue.delete(this.cryptos, crypto);
    //             // delete on the backend
    //             this.axios.post(
    //                 'remove_crypto',
    //                 qs.stringify({symbol: crypto}),
    //                 {headers: {
    //                         'X-CSRFToken': window.$cookies.get('csrftoken'),
    //                         'Content-Type': 'application/x-www-form-urlencoded'}
    //                 }
    //             ).then(() =>
    //                 this.$notify({
    //                     text: crypto + ' deleted',
    //                     type: 'success',
    //                     group: 'notif'
    //                 })
    //             )
    //         },
    //         refreshData() {
    //             this.axios.get(api_url_default, {
    //                 params: {
    //                     fsyms: this.getSymbols().join()
    //                 }
    //             }).then(response => {
    //                 // FIXME add data from Backend in this.cryptos
    //                 for (let obj of Object.values(response.data.RAW)) {
    //                     let res = obj['USD'];
    //                     let toUpdate = this.cryptos[res['FROMSYMBOL']];
    //                     Object.assign(toUpdate, {symbol: res['FROMSYMBOL']}, res);
    //                 }
    //                 this.$forceUpdate();
    //             })
    //         },
    //         initData() {
    //             this.axios.get('user_crypto')
    //             .then(response => {
    //                 this.cryptos = {};
    //                 if(response.data['username']) {
    //                     for (let crypto of response.data['cryptos'])
    //                         this.cryptos[crypto['symbol']] = {
    //                             'urls': crypto['urls'],
    //                             'logo': crypto['logo'],
    //                             'favorite': crypto['favorite'],
    //                         };
    //                 }
    //             })
    //             .finally(() => {
    //                 if (!this.cryptosEmpty)
    //                     this.refreshData();
    //             });
    //         },
            onConnect(username) {
                this.username = username;
                // let cryptolist = this.$refs.login.$refs.cryptolist;
                // cryptolist.initData();
                // this.$router.push('crypto')
                // this.$emit('initdata');
                // this.initData();
            },
    //         switchFavorite(symbol) {
    //             this.cryptosSelected[symbol].favorite = !this.cryptosSelected[symbol].favorite;
    //             this.$forceUpdate();
    //         },
        }
    }
</script>
