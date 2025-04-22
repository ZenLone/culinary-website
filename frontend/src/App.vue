<!-- App.vue -->
<script>
import { ref, onMounted } from 'vue';
import Cookies from 'js-cookie';
import Welcome from './components/Welcome.vue';
import MainApp from './MainApp.vue';

export default {
  components: {
    Welcome,
    MainApp,
  },

  setup() {
    //data
    const showWelcome = ref(true);
    const token = Cookies.get('token');
    //methods
    if (token) {
      showWelcome.value = false; // Если пользователь авторизован, сразу показываем основное приложение
    }
    // Метод для закрытия Welcome
    const closeWelcome = () => {
      showWelcome.value = false;
    };
    return {
      showWelcome,
      closeWelcome
    };
  },
};
</script>

<template>
  <div>
    <Welcome v-if="showWelcome" @close-welcome ="closeWelcome" />
    <MainApp v-else />
  </div>
</template>
<style scoped>
/* Стили для родительского контейнера, добавленного Vue Router */
[data-v-app] > div {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>