<!-- Welcome.vue -->
<template>
  <div class="welcome-container">
    <!-- <h1>Добро пожаловать!</h1> -->
    <h2 class="h2-title" ref="h2title">Добро пожаловать!<br>С этим веб-приложением вы можете создавать ваши блюда и записывать их сюда.</h2>
    <div class="dish-menu-container" ref="dishContainer">
      <div class="dish-name" ref="dishName">Ваше блюдо - 7 минут</div>
      <ul class="ingredients-list">
        <li class="i-1" ref="dishI">Ингредиент 1</li>
        <li class="i-2" ref="dishI">Ингредиент 2</li>
        <li class="i-3" ref="dishI">Ингредиент 3</li>
        <li class="i-4" ref="dishI">Ингредиент 4</li>
        <li class="i-5" ref="dishI">Ингредиент 5</li>

      </ul>
    </div>
    <h2 class="h2-2-title">Узнавайте новые факты о блюдах, переписываясь с другими пользователями.</h2>
    <div class="chat-container">
      <div class="avatar-name-container">
        <img class="avatarPicture-welcome" src="../assets/images/avatar-welcome.jpg"></img>
        <h2 class="avatar-name">Аня Строцкая</h2>
      </div>
      <div class="chat-container-welcome">
        <div class="chat-welcome">Написать сообщение...</div>
      </div>
    </div>
    

    <button class="welcomeBtn" @click="close">Начать</button>
  </div>
</template>

<script>
import {ref, reactive, onMounted} from 'vue';
export default {
  name:'Welcome',
  emits:['close-welcome'],
  setup(_,{emit}){
  //data
  const h2title = ref(null); 
  const dishContainer = ref(null);
  const dishName = ref(null);
  const dishI = ref(null);      
  //methods
  const close = () => {
      emit('close-welcome'); // Уведомляем родителя о необходимости закрыть Welcome
    };
  const startAnimation= ()=>{
    anime({//Текст
      targets:h2title.value,
      translateX:10,
      duration:1000,
      opacity:1,
      easing:'easeOutQuad',
      delay:150
    });
    anime({
      targets:dishContainer.value,
      opacity:1,
      duration:1000,
      delay:250,
      easing:'easeOutQuad',
      translateX:10
    });
    anime({
      targets:dishName.value,
      opacity:1,
      duration:1000,
      delay:500,
      easing:'easeOutQuad'
    });
    anime({
      targets:'.ingredients-list li',
      opacity:1,
      duration:1000,
      delay:600,
      easing:'easeOutQuad'
    });
    anime({
      targets:'.h2-2-title',
      opacity:1,
      translateX:10,
      duration:1000,
      delay:250,
      easing:'easeOutQuad'
    });
    anime({
      targets:'.chat-container',
      opacity:1,
      translateX:10,
      duration:1000,
      delay:250,
      easing:'easeOutQuad'
    });
    anime({
      targets:'.avatarPicture-welcome',
      opacity:1,
      delay:350,
      easing:'easeOutQuad',
      duration:1000,
    });
    anime({
      targets:'.avatar-name',
      opacity:1,
      delay:350,
      easing:'easeOutQuad',
      duration:1000,
    });
    anime({
      targets:'.chat-welcome',
      opacity:1,
      delay:450,
      easing:'easeOutQuad',
      duration:1000,
    });
  }
    onMounted(()=>{
      startAnimation();
    })

  return{close,startAnimation,h2title,dishContainer,
    dishName,dishI
  }
}
}

</script>

<style scoped>
.welcome-container {
  text-align: center;
  padding: 50px;
  font-family: Arial, sans-serif;
  background-color: white;
  border-radius: 9px;
  width:568px;
  height:626px;
  position: relative;
}
.box {
  width: 100px;
  height: 100px;
  background-color: #4caf50;
}
.animatedText span {
  display: inline-block;
  font-size: 2rem;
  transform: translateY(0);
}
.h2-title{
  font-family: 'Roboto Serif';
  font-size: 24px;
  font-weight: 500;
  text-align: left;
  width:465px;
  opacity: 0;
  position: absolute;
  top:35px;
  left:40px;
}
.h2-2-title{
  font-family: 'Roboto Serif';
  font-size: 24px;
  font-weight: 500;
  text-align: left;
  width:465px;
  opacity: 0;
  position: absolute;
  top:360px;
  left:40px;
}
.chat-container{
  height:95px;
  background-color: #ff8c0083;
  position: absolute;
  top:450px;
  width:480px;
  border-radius: 6px;
  left:35px;
  opacity: 0;
}
.avatar-name-container{
  display: flex;
  padding:8px 18px;
  column-gap: 10px;
  align-items: center;
}
.chat-container-welcome{
  padding:0 18px;
  height:30px;
}
.chat-welcome{
  background-color: white;
  width:410px;
  height:30px;
  padding:10px;
  font-size: 16px;
  font-weight: 500;
  font-family: 'Roboto Serif';
  color:rgba(116, 116, 116, 0.608);
  border-radius: 1px 6px 6px 1px;
  display: flex;
  align-items: center;
  opacity: 0;
}
.avatarPicture-welcome{
  width:40px;
  height:40px;
  opacity: 0;
}
.avatar-name{
  font-size: 18px;
  font-family: 'Roboto Serif';
  font-weight: 500;
  opacity: 0;
}
.welcomeBtn{
  width:193px;
  height:42px;
  font-family: 'Roboto Serif';
  font-size: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background-color: #ff8c0083;
  cursor: pointer;
  position: absolute;
  bottom:15px;
  left:50%;
  transform: translateX(-50%);
  transition: all .4s;
  &:hover{
    background-color: #ff8c00bb;
  }
}
.dish-menu-container{
  padding:12px 16px;
  background-color: #f98d0a7a;
  /* opacity: 0.15; */
  width:480px;
  height:188px;
  border-radius: 9px;
  position: absolute;
  top:160px;
  left:34px;
  right:44px;
  opacity: 0;
}
.ingredients-list{
  width:450px;
  flex-wrap: wrap;
  display: flex;
  column-gap: 22px;
  row-gap: 18px;
}
.i-1,.i-2,.i-3,.i-4,.i-5{
  border:1px solid black;
  border-radius: 3px;
  font-family: 'Roboto Serif';
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: white;
  opacity: 0;
  cursor: default;
  transition: background-color .4s;
  &:hover{
    background-color: #ffa73a;
  }
}
.i-1{
  width:135px;
  height:37px;
}
.i-2{
  width:190px;
  height:37px;
}
.i-3{
  width:135px;
  height:37px;
}
.i-4{
  width:135px;
  height:37px;
}
.i-5{
  width:135px;
  height:37px;
}
.dish-name{
  font-size: 24px;
  font-family: 'Roboto Serif';
  text-align: left;
  width:450px;
  background-color: white;
  border-radius: 3px;
  height:53px;
  border: 1px solid black;
  border-radius: 3px;
  display: flex;
  justify-content: left;
  align-items: center;
  padding: 12px;
  margin-bottom: 15px;
  opacity: 0;
  margin-top: 2.5px;
  cursor: default;
  transition: background-color .4s;
  &:hover{
    background-color: #ffa73a;
  }
}
</style>