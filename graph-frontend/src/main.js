import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { createPinia } from 'pinia'
const app = createApp(App)
app.use(router)
app.use(Antd)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.mount('#app')
