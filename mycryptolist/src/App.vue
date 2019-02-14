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
            <router-view :username="username" @connect="onConnect"></router-view>
        </div>

        <!--<v-data-table :headers="headers" :items="desserts" class="elevation-1">-->
        <table class="">
            <thead>
                <tr class="headers">
                    <th>Coin</th>
                    <th>Price</th>
                    <th>24 hours change</th>
                    <th>Socials</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <cryptocurrency v-for="(crypto, symbol) in cryptos" :key="symbol" class="row-coin" :result="crypto.result" :symbol="crypto.symbol" :logo="crypto.logo" :urls="crypto.urls" @delete="deleteCrypto(symbol)">
                </cryptocurrency>
            </tbody>
        </table>
    </div>
</template>

<script>
    import qs from 'qs'
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
                cryptos: {},
            }
        },
        created() {
            this.axios.get('get_user_connected/').then(response => {
                this.username = response['data']['username'];
                this.initData();
            });
        },
        mounted() {
            setInterval(() => this.refreshData(), 20000);
        },
        computed: {
            cryptosEmpty() {
                return Object.keys(this.cryptos).length === 0;
            },
            cryptosReady() { // return array of cryptos that has actual data
                if (!this.cryptosEmpty)
                    return this.cryptos;
                return {};
            },
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
                let symbol = this.textSearch.toUpperCase()
                if (this.cryptoInList(symbol))
                    return;
                this.loadBackendData(symbol)
                .then(() => this.loadApiData(symbol))
            },
            loadBackendData(symbol) {
                return new Promise((resolve, reject) => {
                    this.axios.post('user_crypto',
                        qs.stringify({symbol: symbol}),
                        {
                            headers: {
                                'X-CSRFToken': window.$cookies.get('csrftoken'),
                                'Content-Type': 'application/x-www-form-urlencoded'
                            }
                        }
                    ).then((response) => {
                        console.log(response);
                        this.cryptos[symbol] = {
                            urls: response['urls'],
                            logo: response['logo'],
                            symbol: symbol,
                        };
                        resolve()
                    })
                });
            },
            loadApiData(symbol) {
                this.axios.get(api_url_default,
                    {params: {
                        fsyms: symbol
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
                        let symbol = obj['USD']['FROMSYMBOL'];
                        let result = obj['USD'];
                        this.cryptos[symbol]['result'] = result;
                        this.cryptos[symbol]['symbol'] = symbol;
                        this.textSearch = "";
                    }
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
                    // FIXME add data from Backend in this.cryptos
                    for (let obj of Object.values(response.data.RAW)) {
                        let result = obj['USD'];
                        let toUpdate = this.cryptos[result['FROMSYMBOL']];
                        Object.assign(toUpdate, {symbol: result['FROMSYMBOL'], result: result});
                        this.$set(this.cryptos, 'symbol', toUpdate);
                    }
                })
            },
            initData() {
                this.axios.get('user_crypto')
                .then(response => {
                    this.cryptos = {};
                    if(response.data['username']) {
                        for (let crypto of response.data['cryptos'])
                            this.cryptos[crypto['symbol']] = {'symbol': crypto['symbol'], 'urls': crypto['urls'], 'logo': crypto['logo'], 'result': {}};
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
