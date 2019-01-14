<template>
    <div>
        <h3 class="text-center"><router-link to="/">Cryptocurrencies Pricing</router-link></h3>
        <hr/>
        <router-link to="/about">About</router-link>
        <router-view></router-view>
        <div class="subhead">
            <div class="search_bar">
                <form id="add_crypto" style="display: flex; align-items: center">
                    <input class="search" type="text" placeholder="Search cryptocurrency..." v-model="textSearch">
                    <input class="button" type="submit" value="Search" @click.prevent="loadData">
                </form>
            </div>
            <login></login>
        </div>

        <div class="headers coin-container">
            <span>Coin</span>
            <span>Price</span>
            <span>24 hours change</span>
            <span>Action</span>
        </div>
        <div v-for="crypto in cryptosReady" v-bind:key="crypto.name">
            <div class="card" :id="crypto.name">
                <cryptocurrency :result="crypto.result" :name="crypto.name"
                                @delete="deleteCrypto(crypto)"></cryptocurrency>
            </div>
        </div>
    </div>
</template>

<script>
    import Login from './components/login/Login.vue'
    import Cryptocurrency from './components/Cryptocurrency.vue'
    // import CryptoList from './components/CryptoList.vue'
    import Vue from './main.js'

    const api_url_default = "https://min-api.cryptocompare.com/data/pricemultifull?tsyms=USD";

    export default {
        name: 'App',
        components: {
            Cryptocurrency,
            Login,
            // CryptoList,
        },
        data: function () {
            return {
                textSearch: "",
                cryptos: [{name: 'BTC', result: {}}, {name: 'NANO', result: {}}],
            }
        },
        created() {
            this.refreshData();
        },
        mounted() {
            setInterval(() => this.refreshData(), 10000);
        },
        computed: {
            cryptosReady() { // return array of cryptos that has actual data
                return this.cryptos.filter(crypto => crypto.result.hasOwnProperty("PRICE"))
            }
        },
        methods: {
            loadData() {
                this.axios.get(api_url_default, {
                    params: {
                        fsyms: this.textSearch.toUpperCase()
                    }
                }).then(response => {
                    if (response.data["Response"] === "Error")
                        alert("This cryptocurrency does not exist.\"");
                    // $('.button').notify("This cryptocurrency does not exist.", {
                    //     className: 'error',
                    //     autoHideDelay: 2000
                    // })
                    else {
                        // $('.button').notify(this.textSearch + " added", {
                        //     className: 'success',
                        //     autoHideDelay: 2000
                        // });
                        var obj = Object.values(response.data.RAW)[0];
                        obj['name'] = obj['USD']['FROMSYMBOL'];
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
                // $.notify(crypto + " deleted", "success");
            },
            refreshData() {
                var names = [];
                for (let obj of this.cryptos)
                    names.push(obj['name'])
                this.axios.get(api_url_default, {
                    params: {
                        fsyms: names.join()
                    }
                }).then(response => {
                    this.cryptos = [];
                    for (let obj of Object.values(response.data.RAW)) {
                        obj['name'] = obj['USD']['FROMSYMBOL'];
                        obj['result'] = obj['USD'];
                        delete obj['USD'];
                        this.cryptos.push(obj);
                    }
                })
            },
        }
    }
</script>
