<script>
import {ref} from 'vue';
import axios from 'axios';
export default{
    name:'Register',
    components:{

    },
    setup(){
        //data
        const user = {
            username:'',
            mail:'',
            password:''
        };
        const errorMessage = ref('');
        //methods
        const registerUser = async()=>{
            errorMessage.value = '';
            if(!user.username || !user.mail || !user.password){
                errorMessage.value = 'All fields are required';
            }
            else{
                try{
                    const response = await axios.post('http://127.0.0.1:8000/api/register/', user);
                    // Check server response
                    if (response.data.token) {
                    console.log('Token:', response.data.token); // Save token for future use
                    console.log('New user registered!');
                } else {
                    errorMessage.value = response.data.message || 'Error: maybe a user with this username is exists';
                    console.log('Register is failed');
                }
                }
                catch(error){
                    errorMessage.value = 'Register failed. Please try again.';
                    console.log(error.message);
                }
            }
        }
        //Хуки

        return {
            user,
            errorMessage,
            registerUser
        };
    }
}
</script>
<template>
<form @submit.prevent="registerUser">
    <h2 class="form-title">Register</h2>
    <div class="form-input">
        <h2>Username</h2>
        <input v-model="user.username" placeholder="Введите никнейм..." type="text">
    </div>
    <div class="form-input">
        <h2>Mail</h2>
        <input v-model="user.mail" placeholder="Введите почту..." type="text">
    </div>
    <div class="form-input">
        <h2>Password</h2>
        <input v-model="user.password" placeholder="Введите пароль..." type="password">
    </div>
    <div class="auth-functions-container">
        <a href="#/profile">Login</a>
    </div>
    <div class="error-container" v-if="errorMessage">
        <h2>{{errorMessage}}</h2>
    </div>
    <div class="form-btn-container">
        <button class="form-btn" type="submit">Войти</button>
    </div>
    </form>
</template>
<style scoped>
h2{
    font-size: 20px;
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}
.form-title{
    font-size: 24px;
    text-align: center;
    margin-top: 10px;
}
.form-input{

    & h2{
    padding:5px;
    }
    & input{
        border-radius: 6px;
        background-color: gainsboro;
        width:100%;
        height:30px;
        font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
        font-size: 17px;
        padding: 0px 5px;;
    }
}
.form-btn{
    padding:5px 10px;
    border-radius: 6px;
    font-size: 16px;
    cursor: pointer;
    background-color: rgb(95, 175, 228);
}
.form-btn-container{
    display: flex;
    justify-content: center;
    margin-top: 10px;
}
.error-container{
    width:100%;
    height: auto;
    margin-top: 10px;
    & h2{
        color:red;
        font-size: 16px;
    }
}
</style>