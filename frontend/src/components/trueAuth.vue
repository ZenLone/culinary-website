<script>
import Cookies from 'js-cookie';
import dayjs from 'dayjs';
import axios from 'axios';
import { ref, watch } from 'vue';
export default{
    name:'trueAuth',
    components:{

    },
    props:{
        isAuthenticated:{
            type:Boolean,
            required:true
        },
        userData:{
            type:Object,
            required:true
        }
    },
    emits:['update-auth'],

    setup(props,{emit}){
        //data
        const avatarPath = ref('');
        //methods
        const logout = () =>{
            Cookies.remove('token');
            emit('update-auth',false);
        };
        const formatDate = (dateString) => {
            if (!dateString) return '';
            return dayjs(dateString).format('DD.MM.YYYY'); // Формат даты: день.месяц.год
        };
        const uploadAvatar = async(event)=>{
            try{
            const file = event.target.files[0];
            if(!file){
                console.log('Файл не был получен');
                return;
            }
            else{
                const userId = props.userData._id;
                const formData = new FormData();
                formData.append('image', file);
                console.log('Object with file',[...formData.entries()]);
            const response = await axios.post(`http://127.0.0.1:8000/api/upload-image/${userId}`,formData,
                {headers:{'Content-Type': 'multipart/form-data',}}

            );
            if(!response.data){
                console.log("Ошибка при загрузке аватара");
            }
            else{
                console.log('Аватар успешно загружен!');
            }
            }
        }
        catch(error){
            console.log('Ошибка при получении данных. ', error.message);
        }
        };

        const fetchUserAvatar = async()=>{
            try{
            const userId = props.userData._id;
            console.log(userId);
            
            const response = await axios.get(`http://127.0.0.1:8000/api/user-image/${userId}`);
            if(!response.data){
                return;
            }
            else{
            console.log(response)
            const imagePath = response.data.imageurl;
            console.log(imagePath)
            const fullImagePath = `http://127.0.0.1:8000/api/user-image/${userId}`;
            console.log('Путь к изображению:', fullImagePath);
            avatarPath.value = fullImagePath;
        }
        }
        catch(error){
            console.error('Ошибка при получении аватара:', error.message);
        }
        };
        //watch
        watch(
        ()=>props.userData,
        (newUserData)=>{
            if(newUserData && newUserData._id){
                console.log('userData updated. Fetching avatar...');
                    fetchUserAvatar();
            }
        },
        { immediate: true }
    );
        return{
            logout,
            formatDate,
            uploadAvatar,
            fetchUserAvatar,
            avatarPath
        };
    }
}
</script>
<template>
<h2 class="profile-title">Профиль</h2>
<div class="container-info">
<div class="picture-container">
    <img class="avatar" :src="avatarPath" alt="">
    <button class="upload-photo" type="file">
        <input class="imgInput" type="file" accept="image/*" name="image" @change="uploadAvatar">
        <svg height="200" width="200" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
	<path d="M18.22 20.75H5.78A2.64 2.64 0 0 1 3.25 18v-3a.75.75 0 0 1 1.5 0v3a1.16 1.16 0 0 0 1 1.25h12.47a1.16 1.16 0 0 0 1-1.25v-3a.75.75 0 0 1 1.5 0v3a2.64 2.64 0 0 1-2.5 2.75ZM16 8.75a.74.74 0 0 1-.53-.22L12 5.06L8.53 8.53a.75.75 0 0 1-1.06-1.06l4-4a.75.75 0 0 1 1.06 0l4 4a.75.75 0 0 1 0 1.06a.74.74 0 0 1-.53.22Z" fill="currentColor"/>
	<path d="M12 15.75a.76.76 0 0 1-.75-.75V4a.75.75 0 0 1 1.5 0v11a.76.76 0 0 1-.75.75Z" fill="currentColor"/>
</svg>
</button>
</div>
<div class="profile-info">
<h2 class="profile-h2">Username: {{ userData?.username || 'Loading...' }}</h2>
<h2 class="profile-h2">Your mail: {{ userData?.mail || 'Loading...' }}</h2>
<h2 class="profile-h2">Дата регистрации: {{ formatDate(userData?.registrationDate) || 'Loading...' }}</h2>
<h2 class="amount-dishes">Количество созданных блюд: {{ }}</h2>
</div>
</div>
<div class="news-info">

</div>
<div class="btn-container-profile">
    <button class="LogoutBtn" @click="logout">Выйти</button>
</div>
</template>
<style scoped>
h2{
    font-size: 24px;;
    font-family: 'Arial';
}
.profile-title{
    padding: 5px 10px 5px 10px;
    border-bottom: 1px solid black;
    border-radius: 1px;
}
.profile-h2{
    font-size: 20px;
    font-family:'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
    background-color: aliceblue;
    margin: 5px 0;
    padding:3px;
    border-radius: 6px;
}

.LogoutBtn{
    padding:5px 10px;
    font-size: 16px;
    font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
    border-radius: 6px;
    box-shadow: 1px 1px 11px 2px rgba(34, 60, 80, 0.31);
    cursor:pointer;
    border:1px solid rgba(142, 204, 138, 0.975);
    transition: all .2s ease-out;
    &:hover{
       background-color: rgb(222, 218, 218);
    }
}
.container-info{
    display: flex;
    padding:10px 5px;
    column-gap: 10px;
    align-items: center;
}
.picture-container{
    width:105px;
    height:105px;
    box-shadow: 1px 1px 11px 2px rgba(34, 60, 80, 0.31);
    position: relative;
    &:hover{
        opacity: 0.4;
        .upload-photo{
            display: flex;
            position: absolute;
            left:50%;
            transform: translateX(-50%);
            align-items: center;
            justify-content: center;
            width:105px;
            height:105px;
            top:0;
            background-color:transparent;
        }
    }
}
.avatar{
    width:105px;
    height:105px;
}
.upload-photo{
    display: none;
    & svg{
        display: flex;
        align-items: center;
        width:30px;
        height:30px;
        background-color: transparent;
    }
}
.amount-dishes{
    font-size: 14px;
    background-color: aliceblue;
    margin: 5px 0;
    padding:3px;
    border-radius: 6px;
}
.btn-container-profile{
    display: flex;
    justify-content: right;
}
.news-info{
    height:125px;
    width:100%;
}
.imgInput{
    position: absolute;
    width:105px;
    height:105px;
    opacity: 0;
    cursor: pointer;
}
</style>