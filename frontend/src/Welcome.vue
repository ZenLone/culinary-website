<!-- Welcome.vue -->
<template>
    <div class="welcome-container">
      <h1>Добро пожаловать!</h1>
      <p>Это ваше веб-приложение для создания и хранения рецептов.</p>
      <button @click="close">Начать</button>
    </div>
  </template>
  
  <script>
  export default {
    name:'Welcome',
    emits:['close-welcome'],
    setup(_,{emit}){
    //data
    //methods
    const close = () => {
        emit('close-welcome'); // Уведомляем родителя о необходимости закрыть Welcome
      };
  
    return{close}
  }
  }
  
  </script>
  
  <style scoped>
  .welcome-container {
    text-align: center;
    padding: 50px;
    font-family: Arial, sans-serif;
  }
  </style>