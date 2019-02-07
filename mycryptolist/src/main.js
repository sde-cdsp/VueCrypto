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
import Login from './components/form_components/Login.vue'
import Register from './components/form_components/Register.vue'
import AskPasswordReset from './components/form_components/AskPasswordReset.vue'
import PasswordReset from './components/form_components/PasswordReset.vue'
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
    { path: '/ask_password_reset/', component: AskPasswordReset, name: 'AskPasswordReset' },
    { path: '/password_reset/', component: PasswordReset, name: 'PasswordReset' },
];

const router = new VueRouter({
    mode: 'history',
    relative: true,
    routes: routes
});

new Vue({
    router,
    el: '#app',
    render: h => h(App),
});

export default Vue
