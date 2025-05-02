<script>
import NotFound from './NotFound.vue';
import { inject, computed, onMounted,onUnmounted, reactive, ref } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
export default{
    name:'AdminPage',
    components:{
        NotFound
    },
    setup(){
        const userData = inject('userData');
        const users = ref(['']);
        const apiUrl = import.meta.env.VITE_API_URL;
        const searchUser = reactive({
          username:'',
          mail:'',
          _id:'',
        });
        const isAdmin = computed(()=>{
            console.log(userData.value.role);
            return userData.value.role === 'admin'
        });

        //methods
        const searchUsers = async()=>{
          const token = Cookies.get('token');
          if(!token){
            console.log('Token not found!');
          }
          const response = await axios.get(`${apiUrl}/api/allUsers/`, {
                headers:{Authorization:`Bearer ${token}`}
            },);

            users.value = response.data.users;
        } 
        const searchUserByUsername = async()=>{
          const token = Cookies.get('token');
          if(!token){
            console.log('Token not found!');
          }
          if(searchUser.username){
            const response = await axios.get(`${apiUrl}/api/deleteIUserByUsername/${searchUser.username}/`,{
                headers:{Authorization:`Bearer ${token}`}});
            if(response.data.resultUser && response.data.resultUser.length > 0){
              const resultUser = response.data.resultUser[0];
              searchUser.mail =  resultUser.mail;
              searchUser._id = resultUser._id;
              console.log(searchUser);
              console.log(response.data.resultUser);
            }
            else{
              console.log('Пользователь не найден!');
            }
          }
          else{
            console.log(`Username required!`);
            
          }
        }
        const deleteUser = async(id)=>{
          if(id){
            await axios.delete(`${apiUrl}/api/deleteUser/${id}/`);
            console.log('User destroyed!')
            searchUsers();
          }
          else{
            console.log('Id required!')
          }
        }
        onMounted(()=>{
          const appContainer = document.querySelector('.app-container');
          appContainer.style.height = '700px';
          appContainer.style.width = '1175px';
        });
        onUnmounted(()=>{
          const appContainer = document.querySelector('.app-container');
          appContainer.style.height = 'auto';
          appContainer.style.width = '450px';
        });
        return{isAdmin,userData,
          searchUsers,users,deleteUser,
          searchUser, searchUserByUsername, 
        };
    }
}

</script>
<template>
    <div v-if="isAdmin">
      <h1>Админ-панель</h1>
      <ul class="functions-container">
        <li>
          <h2 class="title-delete">Удаление пользователей</h2>
          <div class="delete-container">
            <div class="delete-item" v-for="(user,index) in users ":key="index">
              <div class="user-info-container">
                <div class="user-username">{{ user.username }} </div>
                <div class="user-mail">{{ user.mail }}</div>
              </div> 
              <div class="deleteBtn" @click="deleteUser(user._id)">
                <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 15 15" fill="none">
              <path d="M7.5 0C3.35719 0 0 3.35812 0 7.5C0 11.6419 3.35719 15 7.5 15C11.6428 15 15 11.6419 15 7.5C15 3.35812 11.6428 0 7.5 0ZM10.9753 9.64969C11.1511 9.82548 11.2499 10.0639 11.2499 10.3125C11.2499 10.5611 11.1511 10.7995 10.9753 10.9753C10.7995 11.1511 10.5611 11.2499 10.3125 11.2499C10.0639 11.2499 9.82548 11.1511 9.64969 10.9753L7.5 8.82562L5.35031 10.9753C5.26345 11.0627 5.16017 11.132 5.04642 11.1793C4.93267 11.2266 4.8107 11.251 4.6875 11.251C4.5643 11.251 4.44233 11.2266 4.32858 11.1793C4.21483 11.132 4.11155 11.0627 4.02469 10.9753C3.93755 10.8883 3.86842 10.785 3.82126 10.6713C3.77409 10.5575 3.74981 10.4356 3.74981 10.3125C3.74981 10.1894 3.77409 10.0675 3.82126 9.95372C3.86842 9.83999 3.93755 9.73668 4.02469 9.64969L6.17438 7.5L4.02469 5.35031C3.8489 5.17452 3.75014 4.9361 3.75014 4.6875C3.75014 4.4389 3.8489 4.20048 4.02469 4.02469C4.20048 3.8489 4.4389 3.75014 4.6875 3.75014C4.9361 3.75014 5.17452 3.8489 5.35031 4.02469L7.5 6.17438L9.64969 4.02469C9.82548 3.8489 10.0639 3.75014 10.3125 3.75014C10.5611 3.75014 10.7995 3.8489 10.9753 4.02469C11.1511 4.20048 11.2499 4.4389 11.2499 4.6875C11.2499 4.9361 11.1511 5.17452 10.9753 5.35031L8.82562 7.5L10.9753 9.64969Z" fill="black"/>
            </svg>
            </div>
            </div>
          </div>
          <button class="searchUserBtn" @click="searchUsers()">Поиск пользователей</button>
        </li>
        <li>
          <h2 class="title-delete">Удаление пользователя</h2>
          <div class="delete-container">
            <div class="delete-item">
              <div class="user-info-container">
                <div class="user-username">{{ searchUser.username }} </div>
                <div class="user-mail">{{ searchUser.mail }}</div>
              </div> 
              
            </div>
            <div class="input-item-user">
              <input v-model="searchUser.username" type="text" placeholder="Напишите пользователя...">
              <div class="svg-search-container" @click="searchUserByUsername()">
                <svg class="svg-search" height="200" width="200" viewBox="0 0 26 26" xmlns="http://www.w3.org/2000/svg">
	          <path d="M10 .188A9.812 9.812 0 0 0 .187 10A9.812 9.812 0 0 0 10 19.813c2.29 0 4.393-.811 6.063-2.125l.875.875a1.845 1.845 0 0 0 .343 2.156l4.594 4.625c.713.714 1.88.714 2.594 0l.875-.875a1.84 1.84 0 0 0 0-2.594l-4.625-4.594a1.824 1.824 0 0 0-2.157-.312l-.875-.875A9.812 9.812 0 0 0 10 .188zM10 2a8 8 0 1 1 0 16a8 8 0 0 1 0-16zM4.937 7.469a5.446 5.446 0 0 0-.812 2.875a5.46 5.46 0 0 0 5.469 5.469a5.516 5.516 0 0 0 3.156-1a7.166 7.166 0 0 1-.75.03a7.045 7.045 0 0 1-7.063-7.062c0-.104-.005-.208 0-.312z" fill="currentColor"/>
            </svg>
              </div>
              
            </div>
          </div>
          <button class="searchUserBtn" @click="deleteUser(searchUser._id)">Удалить пользователя</button>
        </li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
      </ul>
    </div>
    <div v-else>
      <h1>Доступ запрещён</h1>
    </div>
  </template>
<style>
.functions-container{
  flex-wrap: wrap;
  display: flex;
  column-gap:60px;
  row-gap: 30px;
  & li{
    width:314px;
    height:266px;
    background-color: transparent;
    padding:3px 7px;
    border-radius: 3px;
    border: 1px solid black;
  }
}
.title-delete{
  width:185px;
  height:20px;
  color:white;
  background-color: black;
  font-family: 'Roboto Serif';
  font-size: 13px;
  font-weight: 500;
  margin: 0 auto;
  margin-bottom: 3px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 3px;
}
.delete-container{
  width:300px;
  margin: 0 auto;
  border-radius: 3px;
  background-color: white;
  margin-bottom: 5px;
  padding:5px;
  height: 200px;
  overflow-y: auto;
  display: grid;
  row-gap: 10px;
  position: relative;
}
.searchUserBtn{
  width:175px;
  height:30px;
  background-color: #6BF298;
  font-family: 'Roboto Serif';
  font-size: 14px;
  font-weight: 500;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 3px;
}
.delete-item{
  padding:2px 5px;
  background-color: #D9D9D9;
  height:40px;
  border-radius: 6px;
  position: relative;
}
.user-info-container{
  display: grid;
  row-gap: 0px;
}
.deleteBtn{
  position: absolute;
  width:25px;
  height:25px;
  display: flex;
  align-items: center;
  right:10px;
  bottom:5px;
  background-color: white;
  border-radius: 6px;
  justify-content: center;
  cursor: pointer;
  transition: background-color .4s;
  &:active{
    background-color: gray;
  }
}
h1{
  font-family: 'Helvetica';

}
.input-item-user{
  height:40px;
  background-color: #D9D9D9;
  border-radius: 6px;
  position: absolute;
  top:55px;
  left:25px;
  display: flex;
  align-items: center;
  width:250px;
  padding:0 5px;
  column-gap: 10px;
  & input{
  height:40px;
  background-color: #D9D9D9;
  border-radius: 6px;
  width:215px;
  padding:5px 0px;
  font-size: 15px;
  font-family: 'Helvetica';
  }
}
.svg-search{
width:16px;
cursor: pointer;
height:16px;
margin: 0 auto;
}
.svg-search-container{
  width:27px;
  height:25px;
  background-color: white;
  border-radius: 6px; 
  display: flex;
  align-items: center;
  justify-items: center;
}
</style>