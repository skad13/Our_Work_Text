import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

// 创建Vue应用
const app = createApp(App)

// 使用路由
app.use(router)

// 挂载Vue应用
app.mount('#app')