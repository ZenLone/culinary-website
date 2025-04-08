<script>
import { ref } from 'vue';
import axios from 'axios';
export default{
  name:'App',
  components:{
    
  },
  setup(){

    //data
    const ingredients = ref([]);
    const dish_name = ref('');
    const dish_time = ref('Не указано');
    //methods
    const addIngredientInput = () => {
      ingredients.value.push('');
    };
    const getFormData = async () => {
      const hasIngredients = ingredients.value.some((ingredient) => ingredient.trim() != '');
      if(!hasIngredients){
        console.log('Добавленные ингредиенты, не были заполненны!');
      }
      else if(!dish_name.value){
        console.log('Блюдо не названо!');
      }
      else{
        const filteredIngredients = ingredients.value.filter((ingredient) => ingredient.trim() !== '');
        // console.log('Название блюда:', dish_name.value);
        // console.log("Время приготовления:", dish_time.value);
        // console.log('Ингредиенты:', filteredIngredients);
        const data = {
          name:dish_name.value,
          ingredients:filteredIngredients,
          time:dish_time.value
        }
        console.log(data);
        try{
          const response = await axios.post('http://127.0.0.1:8000/api/data', data);
          console.log('Данные успешно отправлены:', response.data);
        }
        catch(error){
          console.error('Ошибка при отправке данных:', error.message);
        }
      }
    };
    const removeIngredient = (index) => {
      ingredients.value.pop(); // Удаляем элемент из массива по индексу
    };
    //computed

    //watch

    //Хуки

    return {
  dish_name,
  ingredients,
  addIngredientInput,
  getFormData,
  removeIngredient,
  dish_time
  };
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
      <input type="text" @input="dish_time = $event.target.value" placeholder="Введите...">
    </div>

    <h2 class="h2-additions">Ингредиенты:</h2>
    <div  class="additions-input-container">
      <input v-for="(ingredient, index) in ingredients" :key="index" class="addition_input" v-model="ingredients[index] "  type="text" placeholder="Введите..."></input>
    </div>
    <div class="additions-btns-container">
    <button class="addition_button" type="button" @click="removeIngredient(index)">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M432 256c0 17.7-14.3 32-32 32L48 288c-17.7 0-32-14.3-32-32s14.3-32 32-32l352 0c17.7 0 32 14.3 32 32z"/></svg></button>
    <button class="addition_button" @click="addIngredientInput" type="button"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M256 80c0-17.7-14.3-32-32-32s-32 14.3-32 32V224H48c-17.7 0-32 14.3-32 32s14.3 32 32 32H192V432c0 17.7 14.3 32 32 32s32-14.3 32-32V288H400c17.7 0 32-14.3 32-32s-14.3-32-32-32H256V80z"/></svg></button>
  </div>
    <div class="btn-container">
      <button class="add-btn" @click="getFormData">Добавить блюдо</button>
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
  width:115px;
  
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
.additions-input-container{
  padding:0 5px;
  gap:15px;
  display: flex;
  flex-wrap: wrap;
  justify-content: left;
}

.additions-btns-container{
  display: flex;
  column-gap: 10px;
  margin-top: 10px;
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
