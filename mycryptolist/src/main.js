import Vue from 'vue'
import './plugins/vuetify'
import axios from 'axios'
import VueAxios from 'vue-axios'
import './assets/css/foundation.min.css'
import './assets/css/style.css'
import './assets/css/loading-btn.css'
import './assets/css/loading.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import VueRouter from 'vue-router'

import CryptoList from './components/CryptoList.vue'
import Crypto from './components/Crypto.vue'
import Cryptosection from './components/Cryptosection.vue'
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
    {
        path: '/',
        component: Cryptosection,
        meta: {
            requiresAuth: true
        },
        children: [
            {
                path: '',
                component: CryptoList
            },
            {
                path: 'coin',
                component: Crypto
            }
        ]
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/ask_password_reset',
        component: AskPasswordReset
    },
    {
        path: '/password_reset',
        component: PasswordReset
    },
    {
        path: '/register',
        component: Register
    }
];

const router = new VueRouter({
    relative: true,
    routes: routes
});

new Vue({
    router,
    el: '#app',
    render: h => h(App),
});

export default Vue
