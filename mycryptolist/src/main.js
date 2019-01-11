import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import '../public/css/foundation.min.css'
import '../public/css/style.css'

Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

new Vue({
    el: '#app',
    render: h => h(App),
})

export default Vue
