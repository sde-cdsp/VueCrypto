<template>
    <div>
        <h3><img width="2%" :src="logo"/> {{symbol}}</h3>
        <h4>Current price: {{price}}$</h4>
        <div class="v-container grid-list-md">
            <v-layout row wrap>
                <v-flex class="flex xs4">
                    <v-form>
                        <DatePicker></DatePicker>
                        <input type="text" name="value" placeholder="Value when bought" v-model="form.value">
                    </v-form>
                </v-flex>
                <v-flex class="flex xs7 offset-xs1">
                    TOTO
                    <table>
                    </table>
                </v-flex>
            </v-layout>
        </div>
    </div>
</template>

<script>
    import Form from '../utils/utils.js'
    import DatePicker from './reusable_components/DatePicker'

    class TransactionForm extends Form {
        constructor(data) {
            super(data);
        }
    }

    export default {
        name: "Crypto",
        props: ['username', 'symbol', 'logo', 'price'],
        components: {
            'DatePicker': DatePicker
        },
        data: () => {
            return {
                form: new TransactionForm({
                    username: '',
                    symbol: '',
                    amount: 0,
                    value: 0,
                    date: new Date().toISOString().substr(0, 10),
                    menu: false
                })
            }
        }
    }
</script>

<style scoped>

</style>