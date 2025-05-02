import { createRouter,createWebHistory } from "vue-router";
import Dishes from './components/Dishes.vue';
import AddDish from './components/Add_Dish.vue';
import Profile from './components/Profile.vue';
import Register from './components/Register.vue';
import AdminPage from './components/Admin.vue';
import Chat from "./components/Chat.vue";
import NotFound from './components/NotFound.vue';

// Определение маршрутов
const routes = [
    { path: '/', component: Dishes },
    { path: '/add_dish', component: AddDish },
    { path: '/profile', component: Profile },
    { path: '/register', component: Register },
    { path: '/admin-panel', component: AdminPage },
    { path: '/chat', component:Chat},
    { path: '/:pathMatch(.*)*', component: NotFound }, // Страница 404
  ];

  // Создание экземпляра маршрутизатора
const router = createRouter({
    history: createWebHistory(), // Используем обычную маршрутизацию (history mode)
    routes,
  });



  export default router;