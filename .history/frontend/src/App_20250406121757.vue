<script setup>
import { ref, computed } from 'vue';
import AddDish from './Add_Dish.vue';
import Dishes from './Dishes.vue';

// Определение маршрутов
const routes = {
  '/': Dishes,
  '/add_dish': AddDish
};

// Текущий путь (считывается из хэша URL)
const currentPath = ref(window.location.hash);

// Обновление пути при изменении хэша
window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash;
});

// Вычисляем текущий компонент на основе текущего пути
const currentView = computed(() => {
  return routes[currentPath.value.slice(1)]
});
</script>

<template>
  <div class="app-container">
    <!-- Заголовок -->
    <Header />

    <!-- Навигация -->
    <nav>
      <a href="#/">Home</a> |
      <a href="#/dishes">Dishes</a> |
      <a href="#/non-existent-path">Broken Link</a>
    </nav>

    <!-- Динамическая загрузка компонента -->
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
}

nav {
  margin-bottom: 20px;
}
</style>