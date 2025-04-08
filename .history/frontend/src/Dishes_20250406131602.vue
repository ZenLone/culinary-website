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
    <h2>Список блюд:</h2>
    <ul class="dish-items-list">
        <li v-for="(dish,index) in dishes ":key="index" class="dish-item">
            <h2 class="dish-h2">{{ dish.name }} - {{ dish.time }}</h2>
            <ul>
          <li class="dish_item" v-for="(ingredient, idx) in dish.ingredients" :key="idx">
            {{ ingredient }}
          </li>
        </ul>
        </li>
    </ul>
</div>
</template>

<style scoped>
.dish-h2{
    border:1px solid orange;
    padding:3px 5px;
    border-radius: 9px;
    display: flex;
    align-items: center;
    font-size:22px;
}
</style>
