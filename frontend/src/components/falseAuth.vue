<script>
import{ref} from 'vue';
import axios from 'axios';
export default{
    name:'falseAuth',
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
        const loginUser = async()=>{
            errorMessage.value = '';
            if(!user.username || !user.mail || !user.password){
                errorMessage.value = 'All fields are required';
                console.log(errorMessage.value);
            }
            else{
                try{
                    console.log('Success!');
                    const response = await axios.post('/api/login/', user);
                    // Check server response
                if (response.data.success) {
                    console.log('Token:', response.data.token); // Save token for future use
                } else {
                    errorMessage.value = response.data.message || 'Login failed. Please try again.';
                }
                }
                catch(error){
                    errorMessage.value = 'Login failed. Please try again.';
                    console.log(error.message);
                }
            }
        }
        //Хуки

        return {
            user,
            errorMessage,
            loginUser
        };
    }
}
</script>
<template>
<form @submit.prevent="loginUser">
    <h2 class="form-title">Login</h2>
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
        <a href="#/register">Register</a>
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