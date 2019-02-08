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

        <div class="headers">
            <span>Coin</span>
            <span>Price</span>
            <span>24 hours change</span>
            <span>Socials</span>
            <span>Action</span>
        </div>
        <div v-for="crypto in cryptosReady" v-bind:key="crypto.symbol">
            <div class="card" :id="crypto.symbol">
                <cryptocurrency :result="crypto.result" :symbol="crypto.symbol" :logo="crypto.logo" :socials="crypto.socials"
                                @delete="deleteCrypto(crypto)">
                </cryptocurrency>
            </div>
        </div>
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
            setInterval(() => this.refreshData(), 20000);
        },
        computed: {
            cryptosEmpty() {
                return this.cryptos.length === 0;
            },
            cryptosReady() { // return array of cryptos that has actual data
                return this.cryptos.filter(crypto => crypto.result.hasOwnProperty("PRICE"))
            },
            cryptoInList() {
                if (this.getSymbols().includes(this.textSearch.toUpperCase())) {
                    this.$notify({
                        text: this.textSearch.toUpperCase() + ' already in your list!',
                        type: 'warn',
                        group: 'notif'
                    });
                    return true;
                }
                return false;
            }
        },
        methods: {
            getSymbols() {
                let symbols = [];
                for (let obj of this.cryptos)
                    symbols.push(obj['symbol'])
                return symbols
            },
            addCryptoBackend(crypto) {
                this.axios.post('user_crypto',
                    qs.stringify({symbol: crypto['symbol']}),
                    {headers: {
                            'X-CSRFToken': window.$cookies.get('csrftoken'),
                            'Content-Type': 'application/x-www-form-urlencoded'}
                    }
                )
            },
            loadData() {
                this.loadApiData();
                this.loadBackendData();
            },
            loadBackendData() {

            },
            loadApiData() {
                if (this.cryptoInList)
                    return;
                this.axios.get(api_url_default,
                    {params: {
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
                        this.addCryptoBackend(obj);
                        this.textSearch = "";
                    }
                })
            },
            deleteCrypto(crypto) {
                // delete on the frontend
                this.cryptos = this.cryptos.filter(ee => ee !== crypto);
                // delete on the backend
                this.axios.post(
                    'remove_crypto',
                    qs.stringify({symbol: crypto['symbol']}),
                    {headers: {
                            'X-CSRFToken': window.$cookies.get('csrftoken'),
                            'Content-Type': 'application/x-www-form-urlencoded'}
                    }
                ).then(() =>
                    this.$notify({
                        text: crypto['symbol'] + ' deleted',
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
                this.cryptos = [];
                this.axios.get('user_crypto')
                .then(response => {
                    if(response.data['username']) {
                        console.log(response.data)
                        for (let crypto of response.data['cryptos'])
                            this.cryptos.push({'symbol': crypto['symbol'], 'socials': crypto['socials'], 'logo': crypto['logo'], 'result': {}});
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
