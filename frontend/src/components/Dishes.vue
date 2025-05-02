<script>
import {ref, onMounted,onUnmounted} from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
export default{
  name:'Dishes',
  components:{

  },
  setup(){

    //data
    const dishes = ref([]);
    const isAuth = ref(false);
    const apiUrl = import.meta.env.VITE_API_URL;
    //methods
    const fetchDishes = async()=>{
        try{
            const token = Cookies.get('token');
            if(!token){
                console.log('You need to be logged in');
                return;
            }
            else{
            const response = await axios.get(`${apiUrl}/api/data/`, {
                headers:{Authorization:`Bearer ${token}`}
            },);
            dishes.value = response.data.dishes; // Предполагается, что сервер возвращает массив блюд
            console.log('Success dishes collection');
            isAuth.value = true;
        }
        }
        catch(error){
            console.error('Ошибка при получении данных:', error.message);
        }
    }

    const deleteDish = async(id) =>{
        try{
            await axios.delete(`${apiUrl}/api/data/${id}/`);
            // console.log("Успешно удалено блюдо с id: ", id);
            fetchDishes();
            isAuth.value = true;
        }
        catch(error){
            console.log('Ошибка при удалении блюда');
        }
        
        
    }

    //computed

    //watch

    //Хуки
    // Получаем данные при монтировании компонента
    onMounted(() => {
      fetchDishes();
      document.body.style.backgroundImage = "url('/src/assets/images/maket3-dishes.png')";
      document.body.style.backgroundSize = '100%';
    //   document.body.style.backgroundPosition = 'center';
      document.body.style.backgroundRepeat = 'repeat';
    });
    onUnmounted(() => {
      // Возвращаем фон по умолчанию
      document.body.style.backgroundImage = '';
      document.body.style.backgroundSize = '';
      document.body.style.backgroundPosition = '';
    });

    return{dishes, deleteDish,isAuth};
  }
}
</script>

<template>
    <div class="dishes-container">
    <h2 class="dish-title">Список блюд:</h2>
    <h2 v-if="!isAuth" class="errorMessage">Авторизуйтесь, чтобы увидеть или создать свои блюда!</h2>
    <ul class="dish-items-list">
        <li v-for="(dish,index) in dishes ":key="index" class="dish-item">
            <h2 class="dish-h2">{{ dish.name }} - {{ dish.time }}</h2>
            <ul class="dishes-items-list">
          <li class="dish_item" v-for="(ingredient, idx) in dish.ingredients" :key="idx">
            {{ ingredient }}
          </li>
        </ul>
        <button class="dish-delete-btn" @click="deleteDish(dish._id)"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path d="M135.2 17.7C140.6 6.8 151.7 0 163.8 0H284.2c12.1 0 23.2 6.8 28.6 17.7L320 32h96c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64S14.3 32 32 32h96l7.2-14.3zM32 128H416V448c0 35.3-28.7 64-64 64H96c-35.3 0-64-28.7-64-64V128zm96 64c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16zm96 0c-8.8 0-16 7.2-16 16V432c0 8.8 7.2 16 16 16s16-7.2 16-16V208c0-8.8-7.2-16-16-16z"/></svg></button>
        </li>
    </ul>
    
</div>
</template>

<style scoped>
body{
    background-image: url(../assets/images/3-frame.png);
}
.dish-title{
    font-size: 24px;
    padding: 5px 10px 5px 10px;
    margin-bottom: 10px;
    border-bottom:1px solid black;
    border-radius: 1px;

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
    width: auto;
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
    border: 1px solid orange;
    border-radius: 9px;
    width: 115px;
    height: 25px;
    padding: 2px 5px;
    cursor: pointer;
    transition: all .3s ease-out;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: white;
    margin-bottom: 5px;
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
.errorMessage{
    font-size: 18px;
    font-family: 'Helvetica';
}
</style>
