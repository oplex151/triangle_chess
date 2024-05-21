import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(ElementPlus)

app.mount('#app')

// var backend_url = "http://127.0.0.1:8888" //后端地址
// if (navigator.platform.indexOf('Linux') != -1){
//     backend_url = "http://124.70.208.148" //后端地址
// }

export default{ //后端地址
    url: "http://127.0.0.1:8888"
}
