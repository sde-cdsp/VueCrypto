<template>
    <div>
        <h3 class="text-center"><router-link to="/">Cryptocurrencies Pricing</router-link></h3>
        <hr/>
        <div class="subhead">
            <notifications group="notif"></notifications>
            <div class="search_bar">
                <form id="add_crypto" style="display: flex; align-items: center">
                    <input class="search" type="text" placeholder="Search cryptocurrency..." v-model="textSearch">
                    <input class="button" type="submit" value="Search" @click.prevent="loadData">
                </form>
            </div>
            <!--<router-view :appUsername="username"></router-view>-->
            <router-view :username="username" @connect="onConnect"></router-view>
        </div>

        <div class="headers">
            <span>Coin</span>
            <span>Price</span>
            <span>24 hours change</span>
            <span>Socials</span>
            <span>Action</span>
        </div>
        <div v-for="crypto in cryptosReady" v-bind:key="crypto.symbol">
            <div class="card" :id="crypto.symbol">
                <cryptocurrency :result="crypto.result" :symbol="crypto.symbol"
                                @delete="deleteCrypto(crypto)"></cryptocurrency>
            </div>
        </div>
    </div>
</template>

<script>
    import Cryptocurrency from './components/Cryptocurrency.vue'
    // import CryptoList from './components/CryptoList.vue'
    import Vue from './main.js'
    const api_url_default = "https://min-api.cryptocompare.com/data/pricemultifull?tsyms=USD";

    export default {
        name: 'App',
        components: {
            Cryptocurrency,
            // CryptoList,
        },
        data: () => {
            return {
                username: "",
                textSearch: "",
                // cryptos: [{symbol: 'BTC', result: {}}, {symbol: 'NANO', result: {}}],
                cryptos: [],
            }
        },
        created() {
            this.axios.get('get_user_connected/').then(response => {
                this.username = response['data']['username'];
                this.initData();
            });
        },
        mounted() {
            !this.cryptosEmpty && setInterval(() => this.refreshData(), 20000);
        },
        computed: {
            cryptosEmpty() {
                return this.cryptos.length === 0;
            },
            cryptosReady() { // return array of cryptos that has actual data
                return this.cryptos.filter(crypto => crypto.result.hasOwnProperty("PRICE"))
            },
            userIsConnected() {
                return this.username.length > 0
            }
        },
        methods: {
            getSymbols() {
                let symbols = [];
                for (let obj of this.cryptos)
                    symbols.push(obj['symbol'])
                return symbols
            },
            addCrypto(symbol) {
                this.axios.push('add_crypto/', {
                    symbol: symbol
                })
            },
            loadData() {
                if (this.getSymbols().includes(this.textSearch.toUpperCase())) {
                    this.$notify({
                        text: this.textSearch.toUpperCase() + ' already in your list!',
                        type: 'warn',
                        group: 'notif'
                    });
                    return;
                }
                this.axios.get(api_url_default, {
                    params: {
                        fsyms: this.textSearch.toUpperCase()
                    }
                }).then(response => {
                    if (response.data["Response"] === "Error")
                        this.$notify({
                                text: 'This cryptocurrency does not exist.',
                                type: 'error',
                                group: 'notif'
                            });
                    else {
                        this.$notify({
                                text: this.textSearch + ' added',
                                type: 'success',
                                group: 'notif'
                            });
                        let obj = Object.values(response.data.RAW)[0];
                        obj['symbol'] = obj['USD']['FROMSYMBOL'];
                        obj['result'] = obj['USD'];
                        delete obj['USD'];
                        this.cryptos.push(obj);
                        this.textSearch = "";
                    }
                })
            },
            deleteCrypto(crypto) {
                Vue.delete(this.cryptos, crypto);
                this.cryptos = this.cryptos.filter(ee => ee !== crypto);
                this.$notify({
                    text: crypto['symbol'] + ' deleted',
                    type: 'success',
                    group: 'notif'
                });
            },
            refreshData() {
                this.axios.get(api_url_default, {
                    params: {
                        fsyms: this.getSymbols().join()
                    }
                }).then(response => {
                    this.cryptos = [];
                    for (let obj of Object.values(response.data.RAW)) {
                        obj['symbol'] = obj['USD']['FROMSYMBOL'];
                        obj['result'] = obj['USD'];
                        delete obj['USD'];
                        this.cryptos.push(obj);
                    }
                })
            },
            initData() {
                this.axios.get('user_crypto')
                .then(response => {
                    if(response.data['username']) {
                        this.cryptos = [];
                        for (let symbol of response.data['symbols'])
                            this.cryptos.push({'symbol': symbol, 'result': {}});
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
            }
        }
    }
</script>
