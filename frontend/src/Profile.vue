<script>
import Cookies from 'js-cookie';
import trueAuth from './components/trueAuth.vue';
import falseAuth from './components/falseAuth.vue';
import axios from 'axios';
import {ref} from 'vue';
export default{
    name:'Profile',
    components:{
    trueAuth,
    falseAuth
    },
    setup(){
        //data
        const token = Cookies.get('token'); // Получаем токен из cookie
        const isAuthenticated = ref(!!token); // Проверяем наличие токена
        //methods
        const validateToken = async () => {
        try {
        const response = await axios.post('http://localhost:8000/api/validate-token/');
        isAuthenticated.value = response.data.valid;
         } catch (error) {
        isAuthenticated.value = false;
        console.error('Token validation failed:', error.message);
        console.log('Login or register!!!');
        }
    };


        //Хуки
        validateToken(); // Вызываем при загрузке компонента
    }
}
</script>
<template>
<trueAuth v-if="isAuthenticated"></trueAuth>
 <falseAuth v-else></falseAuth>
</template>
<style scoped>

</style>