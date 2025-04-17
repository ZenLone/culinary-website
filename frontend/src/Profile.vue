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
        const userData = ref({}); // Данные пользователя
        //methods
        const validateToken = async () => {
        try {
            if(!token){
                console.log('Login or register!!!');
            }
            else{
        const response = await axios.post('http://127.0.0.1:8000/api/validate-token/',{token});
        isAuthenticated.value = response.data.valid;
        if(isAuthenticated){
            const userResponse = await axios.get('http://127.0.0.1:8000/api/user-data/',{
                        headers: { Authorization: `Bearer ${token}` }
                    });
            userData.value = userResponse.data;
        }
        }
         } catch (error) {
        isAuthenticated.value = false;
        console.error('Token validation failed:', error.message);
        console.log('Login or register!!!');
        }
    };
        const updateAuthStatus = (newStatus) => {
            isAuthenticated.value = newStatus; // Обновляем статус аутентификации
        };

        //Хуки
        validateToken(); // Вызываем при загрузке компонента

        return{isAuthenticated,updateAuthStatus,userData};
    }
}
</script>
<template>
<trueAuth v-if="isAuthenticated" :isAuthenticated="isAuthenticated" 
:userData="userData" @update-auth="updateAuthStatus"></trueAuth>
 <falseAuth v-else></falseAuth>
</template>
<style scoped>

</style>