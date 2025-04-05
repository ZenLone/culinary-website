<script>
import Header from './components/Header.vue'
import { ref } from 'vue';
export default{
  name:'App',
  components:{
    Header
  },
  setup(){

    //data
    
    //methods

    //computed

    //watch

    //Хуки

    return {
      dish_name: ref('')
    }
  }
}
</script>

<template>
  <div class="app-container">
  <div class="nav">
    <h2>Блюда</h2>
    <h2>Добавить блюдо</h2>
  </div>
  <div class="container">
    <h2>Добавление блюда: {{ dish_name }}</h2>
    <input class="dish_name_input" placeholder="Название блюда" @input="dish_name = $event.target.value" type="text">

    <div class="time-container">
      <h2>Время приготовления:</h2>
      <input type="text" placeholder="Введите...">
    </div>

    <h2 class="h2-additions">Ингридиенты:</h2>
    <div class="additions-btns-container">
      <input class="addition_input" type="text" placeholder="Введите..."></input>
      <button class="addition_button" type="button"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg></button>
    </div>

    <div class="btn-container">
      <button class="add-btn">Добавить блюдо</button>
    </div>

  </div>

</div>
</template>

<style scoped>
.app-container{
  width:450px;
  padding:25px 25px 5px;
  border:1px solid orange;
  border-radius: 21px;
  background-color: white;
  box-shadow: 4px 4px 19px 19px rgba(34, 60, 80, 0.2);
}
.nav{
  display: flex;
  gap:10px;
  justify-content: space-around;
  & h2{
    align-items: center;
    display: flex;
    justify-content: center;
    font-size: 17px;
    font-family: 'Helvetica';
    width: 175px;
    height:25px;
    border-radius: 12px;
    transition: background-color .4s;
    &:hover{
      background-color: rgba(255, 166, 1, 0.732);
      cursor: pointer;
    }
  }
}
.dish_name_input{
  background-color: rgb(185, 185, 185);
  width:100%;
  height:30px;
  font-size: 16px;
  font-family: 'Helvetica';
  border-radius: 15px;
  padding:0 10px;
  &::placeholder{
    color:rgb(92, 90, 90);
  }
}
.container{
  & h2{
    padding:5px;
    font-size: 21px;
  }
}
.time-container{
  display: flex;
  align-items: center;
  margin-top: 5px;
  & h2{
    font-size: 17px;
  }
  & input{
    width:125px;
    border:1px solid orange;
    height:25px;
    padding:7px;
    border-radius: 9px;
    font-size: 14px;
    font-family: 'Helvetica';
  }
}
.h2-additions{
  font-size: 17px;
}
.addition_input{
  font-size: 14px;
  border:1px solid orange;
  border-radius: 9px;
  width:100px;
  
  height:25px;
  padding:0 5px;
  cursor: pointer;
  transition: all .3s ease-out;
  &:hover{
    background-color: orange;
    color:black;
  }
}

.addition_button{
  font-size: 14px;
  border:1px solid orange;
  border-radius: 9px;
  width:65px;
  background-color: transparent;
  height:25px;
  padding:0 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .3s ease-out;
  & svg{
    width:17px;
    height:17px;
  }
  & path{
    fill:orange;
  }
  &:hover{
    background-color: orange;
    & path{
      fill:black;
    }
  }
}
.additions-btns-container{
  padding:0 5px;
  gap:15px;
  display: flex;
}
.add-btn{
  padding:5px 10px;
  background-color: orange;
  font-size: 16px;
  font-family: 'Helvetica';
  border-radius: 3px;
  cursor: pointer;
  height:30px;
  transition: all .2s;
  &:hover{
    opacity: 0.85;
  }
  &:active{
    position: absolute;
    top:2px;
    height:30px;
  }
}
.btn-container{
  justify-content: center;
  display: flex;
  margin-top: 10px;
  height:32px;
  position: relative;
}
</style>
