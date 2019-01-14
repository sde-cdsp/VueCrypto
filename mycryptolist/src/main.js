import Vue from 'vue'
import './plugins/vuetify'
import axios from 'axios'
import VueAxios from 'vue-axios'
import '../public/css/foundation.min.css'
import '../public/css/style.css'
import VueRouter from 'vue-router'

import App from './App.vue'
import About from './components/About.vue'
import Login from './components/login/Login.vue'

Vue.use(VueRouter);
Vue.use(VueAxios, axios);
Vue.config.productionTip = false;

const routes = [
    { path: '/index', component: App, name: 'Index' },
    { path: '/about', component: About, name: 'About' },
    { path: '/login/', component: Login, name: 'Login' },
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
