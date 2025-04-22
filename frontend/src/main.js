// main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './routes'; // Импортируем маршрутизатор
import './assets/main.css'
const app = createApp(App);

// Подключаем маршрутизатор
app.use(router);

// Монтируем приложение
app.mount('#app');