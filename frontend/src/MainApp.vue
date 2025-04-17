<!-- MainApp.vue -->
<script>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import AddDish from './Add_Dish.vue';
import Dishes from './Dishes.vue';
import Header from './components/Header.vue';
import Profile from './Profile.vue';
import Register from './Register.vue';
import NotFound from './NotFound.vue';
import AdminPage from './Admin.vue';

// Определение маршрутов
const routes = {
  '/': Dishes,
  '/add_dish': AddDish,
  '/profile': Profile,
  '/register': Register,
  '/admin': AdminPage,
  '/not_found': NotFound,
};


export default {
  components: {
    Header,
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
        } else {
          const response = await axios.post('http://127.0.0.1:8000/api/validate-token/', { token });
          isAuthenticated.value = response.data.valid;

          if (isAuthenticated.value) {
            const userResponse = await axios.get('http://127.0.0.1:8000/api/user-data/', {
              headers: { Authorization: `Bearer ${token}` },
            });
            userData.value = userResponse.data;
          }
        }
      } catch (error) {
        isAuthenticated.value = false;
        console.error('Token validation failed:', error.message);
        console.log('Login or register!!!');
      }
    };

    // Хуки
    onMounted(() => {
      validateToken();
    });

    window.addEventListener('hashchange', () => {
      // Обновление пути при изменении хэша
      currentPath.value = window.location.hash;
    });

    // Вычисляем текущий компонент на основе текущего пути
    const currentView = computed(() => {
      if (currentPath.value === '#/admin' && (userData.value.role !== 'admin' || userData.value.role == undefined)) {
        return routes['/not_found'];
      } else {
        return routes[currentPath.value.slice(1)] || routes['/not_found'];
      }
    });

     // Генерация случайного цвета
     const randomColor = () => {
      const letters = '0123456789ABCDEF';
      let color = '#';
      for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
      }
      return color;
    };

    return {
      isAuthenticated,
      userData,
      currentView,
      randomColor,
      borderColor
    };
  },
};
</script>

<template>
  <div class="app-container" :style="{ borderColor }"
    @mouseenter="borderColor = randomColor()"
    @mouseleave="borderColor = '#000000'">
    <Header></Header>
    <component :is="currentView" />
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