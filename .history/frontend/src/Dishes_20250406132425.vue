<script>
import {ref, onMounted} from 'vue';
import axios from 'axios';
export default{
  name:'Dishes',
  components:{

  },
  setup(){

    //data
    const dishes = ref([]);
    //methods
    const fetchDishes = async()=>{
        try{
            const response = await axios.get('http://localhost:3000/dishes');
            dishes.value = response.data; // Предполагается, что сервер возвращает массив блюд
        }
        catch(error){
            console.error('Ошибка при получении данных:', error.message);
        }
    }
    //computed

    //watch

    //Хуки
    // Получаем данные при монтировании компонента
    onMounted(() => {
      fetchDishes();
    });

    return{dishes};
  }
}
</script>

<template>
    <div class="dishes-container">
    <h2 class="dish-title">Список блюд:</h2>
    <ul class="dish-items-list">
        <li v-for="(dish,index) in dishes ":key="index" class="dish-item">
            <h2 class="dish-h2">{{ dish.name }} - {{ dish.time }}</h2>
            <ul class="dishes-items-list">
          <li class="dish_item" v-for="(ingredient, idx) in dish.ingredients" :key="idx">
            {{ ingredient }}
          </li>
        </ul>
        </li>
    </ul>
    <button class="dish-delete-btn"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"/></svg></button>
</div>
</template>

<style scoped>
.dish-title{
    font-size: 21px;
    
    margin:5px 0;
}
.dish-h2{
    border:1px solid orange;
    padding:3px 5px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    font-size:20px;
}
.dish_item{
    font-size: 18px;
    font-family: 'Helvetica';
    border: 1px solid orange;
    border-radius: 9px;
    width: 115px;
    height: 25px;
    padding: 2px 5px;
    cursor: pointer;
    transition: all .3s ease-out;
    display: flex;
    align-items: center;
    &:hover{
        background-color: orange;
    }
}
.dish-delete-btn{
    font-size: 18px;
    font-family: 'Helvetica';
    border: 1px solid orange;
    border-radius: 9px;
    width: 115px;
    height: 25px;
    padding: 2px 5px;
    cursor: pointer;
    transition: all .3s ease-out;
    display: flex;
    align-items: center;
    &:hover{
        background-color: orange;
    }
    & svg{
        width:15px;
        height:15px;
    }
    & path{
        fill:black;
    }
}
.dishes-items-list{
    padding: 5px 1px;
    gap: 10px;
    display: flex;
    flex-wrap: wrap;
    justify-content: left;
}
</style>
