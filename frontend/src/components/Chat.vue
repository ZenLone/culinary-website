<script>
import { io } from 'socket.io-client';
import Cookies from 'js-cookie';
import { onMounted,onUnmounted, ref, watch, computed, inject,nextTick } from 'vue';
import axios from 'axios';
const apiUrl = import.meta.env.VITE_API_URL;
const socket = io(apiUrl); // адрес бэка
export default {
  name: 'Chat',
  setup() {
    const inChat = ref(false); 
    const messages = ref([]);
    const sendNewMessage = ref('');
    const userData = inject('userData');
    const chatId = ref('');
    const chatRoomId = ref('');
    const token = Cookies.get('token');
    const messagesContainer = ref(null);
    
    const searchAndJoinInChatRoom = ()=>{
      if(!chatRoomId){
        console.log('chatRoomId required!');
      }
      else{
      inChat.value = true;
      socket.emit('join-chat', chatRoomId.value);
      fetchChatHistory();
      }
    };
    const searchAndJoinInChat = ()=>{
      if(!chatId){
        console.log('ChatId required!');
      }
      else{
      inChat.value = true;
      socket.emit('join-chat', chatId.value);
      fetchChatHistory();
      }
    };
    socket.on('connect', () => {
  console.log('Connected to server');
});

socket.on('disconnect', () => {
  console.log('Disconnected from server');
});
    // Слушаем событие 'new-message'
    socket.on('new-message', (message) => {
      messages.value.push(message);
      nextTick(() => {
      scrollToBottom();
      });
    });
    const  fetchChatHistory = async()=>{
      const token = Cookies.get('token');
      const response = await axios.get(`${apiUrl}/api/chat/history/${chatRoomId.value}/`, {
        headers:{Authorization:`Bearer ${token}`}});
      messages.value = response.data;
      nextTick(() => {
      scrollToBottom();
      });
    }
    const sendMessage = ()=>{
      if(!sendNewMessage.value.trim()){
        return;
      }
      if(!token){
        alert('Для совершения этого действия вы должны быть авторизованы!');
        return;
      }
      axios.post(`${apiUrl}/api/chat/send/`,{
        chatId:chatRoomId.value,
        senderId:userData.value.username,
        text:sendNewMessage.value
      });
      // fetchChatHistory();
      sendNewMessage.value = '';
      scrollToBottom();
    }

    const scrollToBottom = () => {
      if (messagesContainer.value) {
    console.log('scrolling to bottom...');
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  } else {
    console.warn('messagesContainer is null');
  }
    };
    onMounted(()=>{
        const appContainer = document.querySelector('.app-container');
        appContainer.style.height = '650px';
        appContainer.style.width = '1000px';
      });
      onUnmounted(()=>{
        const appContainer = document.querySelector('.app-container');
        appContainer.style.height = 'auto';
        appContainer.style.width = '450px';
      });

    return {
      inChat,chatId,sendNewMessage,
      messages,sendMessage,fetchChatHistory,searchAndJoinInChatRoom,
      searchAndJoinInChat,chatRoomId,scrollToBottom,messagesContainer
    };
  },
};
</script>
<template>
<div class="false-chat-container" v-show="!inChat">
  <!-- <div class="false-chat-container-mini">
  <h2 class="false-h2-title">Кому вы хотите написать?</h2>
  <input class="false-input" v-model="chatId" type="text" placeholder="Напишите имя пользователя...">
  <button class="false-btn" @click="searchAndJoinInChat()">Написать</button>
</div> -->
<div class="false-chat-container-mini">
  <h2 class="false-h2-title">Вход в комнату по коду</h2>
  <input class="false-input" v-model="chatRoomId" @keydown.enter="searchAndJoinInChat"
   type="text" placeholder="Напишите код комнаты...">
  <button class="false-btn" @click="searchAndJoinInChatRoom()">Войти</button>
</div>
</div>
<div class="true-chat-container" v-show="inChat">
  <h2 class="true-c-h2" v-if="chatRoomId">Код комнаты: {{ chatRoomId }}</h2>
  <ul class="messages-list" ref="messagesContainer">
    
    <li class="message-item" v-for="(msg,index) in messages">
      <h2 class="messageUser">{{msg.text}}</h2>
      <h3 class="messageSender">{{msg.senderId}}</h3>
    </li>

  </ul>
  <div class="true-c-send-container">
    <input type="text" v-model="sendNewMessage" class="sendInput"
    @keydown.enter="sendMessage()">
    <button class="sendBtn" @click="sendMessage()">Отправить</button>
  </div>
</div>
</template>
<style>
.false-chat-container{
  display: flex;
  justify-content: center;
  align-items: center;
  height:100%;
  column-gap: 50px;
}
.false-chat-container-mini{
  display: grid;
  row-gap: 5px;
}
.false-h2-title{
  font-size: 20px;
  font-family: 'Helvetica';
}
.false-input{
  font-family: 'Helvetica';
  font-size: 16px;
  background-color: #D9D9D9;
  padding:13px 10px;
  border-radius:6px;
}
.false-btn{
  font-family: 'Helvetica';
  font-size: 16px;
  background-color: black;
  color:white;
  text-align: center;
  padding:5px 45px;
  border-radius:6px;
  cursor: pointer;
  width:165px;
  margin: 0 auto;
}

.true-c-h2{
  font-size: 20px;;
  font-family: 'Helvetica';
  margin-bottom: 8px;
}
.true-chat-container{
  padding:10px 25px;
}
.messages-list{
  display: grid;
  row-gap: 10px;
  height:415px ;
  overflow-y: auto;
}

.message-item{
  width:524px;
  height:auto;
  /* height: 45px; */
  background-color: #D9D9D9;
  border-radius: 6px;
  position: relative;
  padding:8px 15px;
  display: flex;
  align-items: center;
}
.messageSender{
  position: absolute;
  right:5px;
  bottom:0px;
  font-family: 'Helvetica';
  font-size: 12px;
}
.messageUser{
font-size: 20px;
font-family: 'Helvetica';
white-space: pre-wrap; /* Сохраняет переносы строк */
  word-break: break-word; /* Переносит длинные слова */
}
.true-c-send-container{
margin-top: 41px;
background-color: #D9D9D9;
height:87px;
border-radius: 6px;
display: flex;
column-gap: 15px;
align-items: center;
padding:0 21px;

}
.sendInput{
  width:500px;
  height:40px;
  display: flex;
  align-items: center;
  padding: 0px 15px;
  font-size: 20px;
  font-family: 'Helvetica';
  border-radius: 6px;
}
.sendBtn{
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-family: 'Helvetica';
  width:120px;
  height:35px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color .3s;
  &:active{
    background-color: rgb(186, 186, 186);
  }
}
</style>