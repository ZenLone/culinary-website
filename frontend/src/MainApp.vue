<!-- MainApp.vue -->
<script>
import { ref, provide, onMounted } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import AddDish from './components/Add_Dish.vue';
import Dishes from './components/Dishes.vue';
import Header from './components/Header.vue';
import Profile from './components/Profile.vue';
import Register from './components/Register.vue';
import NotFound from './components/NotFound.vue';
import AdminPage from './components/Admin.vue';
import { errorMessages } from 'vue/compiler-sfc';

// // Определение маршрутов
// const routes = {
//   '/': Dishes,
//   '/add_dish': AddDish,
//   '/profile': Profile,
//   '/register': Register,
//   '/admin': AdminPage,
//   '/not_found': NotFound,
// };


export default {
  components: {
    Header, Dishes,
    AddDish, Profile,
    Register, NotFound,
    AdminPage
  },

  setup() {
    // Data
    const token = Cookies.get('token'); // Получаем токен из cookie
    const isAuthenticated = ref(!!token); // Проверяем наличие токена
    const userData = ref({}); // Данные пользователя
    const currentPath = ref(window.location.hash); // Текущий путь (считывается из хэша URL)
    const borderColor = ref('#000000'); // Начальный цвет границы

    // Methods
    const validateToken = async () => {
      try {
        if (!token) {
          console.log('Login or register!!!');
          return;
        } else {
          const response = await axios.post('http://localhost:8000/api/validate-token/', { token });
          isAuthenticated.value = response.data.valid;
          if (isAuthenticated.value) {
            const userResponse = await axios.get('http://localhost:8000/api/user-data/', {
              headers: { Authorization: `Bearer ${token}` },
            });
            userData.value = userResponse.data;
          }
          else{
            Cookies.remove('token');
            isAuthenticated.value = false;
          }
        }
      } catch (error) {
        Cookies.remove('token');
        isAuthenticated.value = false;
        console.error('Token validation failed:', error.message);
        console.log('Login or register!!!');
      }
    };

    // Хуки
    onMounted(() => {
      validateToken();
    });

    // // Следим за изменением хэша URL
    // window.addEventListener('hashchange', () => {
    //   currentPath.value = window.location.hash.slice(1); // Обновляем текущий путь
    // });

    // // Вычисляем, разрешён ли текущий маршрут
    // const isRouteAllowed = computed(() => {
    //   if (currentPath.value === '/admin') {
    //     return isAuthenticated.value && userData.value.role === 'admin'; // Разрешаем только администраторам
    //   }
    //   return true; // Все остальные маршруты разрешены
    // });

     // Генерация случайного цвета
     const randomColor = () => {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    };

    provide('userData', userData);//Передача userData всем компонентам

    return {
      isAuthenticated,
      userData,
      randomColor,
      borderColor,
    };
  },
};
</script>

<template>
  <div class="app-container" :style="{ borderColor }"
    @mouseenter="borderColor = randomColor()"
    @mouseleave="borderColor = '#000000'">
    <Header></Header>
    <router-view></router-view>
  </div>
</template>

<style scoped>
.app-container {
  width: 450px;
  padding: 25px;
  border: 1px solid orange;
  border-radius: 21px;
  background-color: white;
  box-shadow: 4px 4px 19px 19px rgba(34, 60, 80, 0.2);
  position: relative;
  transition: all .4s;
}
</style>