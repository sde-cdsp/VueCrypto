import Vue from 'vue'
import './plugins/vuetify'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './assets/css/foundation.min.css'
import './assets/css/style.css'
import './assets/css/loading-btn.css'
import './assets/css/loading.css'
import VueRouter from 'vue-router'

import App from './App.vue'
import About from './components/About.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import VueCookies from 'vue-cookies'
import Notifications from 'vue-notification'

Vue.use(Notifications);
Vue.use(VueCookies);
Vue.use(VueRouter);
Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

const routes = [
    { path: '/index', component: App, name: 'Index' },
    { path: '/', component: Login, name: 'Login' },
    { path: '/register/', component: Register, name: 'Register' },
];

const router = new VueRouter({
  routes // short for `routes: routes`
});

new Vue({
    router,
    el: '#app',
    render: h => h(App),
});

export default Vue
