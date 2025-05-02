<script>
import {ref} from 'vue';
import axios from 'axios';
import { Howl } from 'howler';
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
        const isRegister = ref(false);
        const errorMessage = ref('');
        const apiUrl = import.meta.env.VITE_API_URL;
        //methods
        const registerUser = async()=>{
            errorMessage.value = '';
            if(!user.username || !user.mail || !user.password){
                errorMessage.value = 'All fields are required';
            }
            else{
                try{
                    const response = await axios.post(`${apiUrl}/api/register/`, user);
                    // Check server response
                if (response.data.token) {
                    console.log('Token:', response.data.token); // Save token for future use
                    console.log('New user registered!');
                    isRegister.value = true;
                    const successSound = new Howl({
                    src: ['../assets/audio/Record (online-voice-recorder.com) (6).mp3'] // Убедитесь, что путь правильный
                    });
                    successSound.play();
                    setTimeout(() => {
                    document.querySelector('.registerSuccessModal').classList.add('visible');
                    setTimeout(()=>{
                        document.querySelector('.registerSuccessModal').classList.remove('visible');
                    },3000)
                    }, 100);
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
            registerUser,
            isRegister
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
        <a href="/profile">Login</a>
    </div>
    <div class="error-container" v-if="errorMessage">
        <h2>{{errorMessage}}</h2>
    </div>
    <div class="form-btn-container">
        <button class="form-btn" type="submit">Зарегистрироваться</button>
    </div>
    </form>
    <img class="registerSuccessModal" src="../assets/images/success-register.png" alt="">
    <audio id="successSound" src="../assets/audio/Record (online-voice-recorder.com) (6).mp3"></audio>
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
.registerSuccessModal{
    position: fixed;
    bottom:0px;
    right:20px;
    visibility: hidden;
    transition: all .4s;
    opacity: 0;
}
.visible{
    visibility: visible;
    transform: translateY(-20px);
    opacity: 1;
}
</style>