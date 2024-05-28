<script setup>
import main from '@/main';
import { User, HomeFilled } from '@element-plus/icons-vue'
import axios from 'axios';
import Cookies from 'js-cookie';
import { onMounted, ref } from 'vue';
import { getRankLevel } from '@/config/rank';
import { ElMessage } from 'element-plus';
import { on } from '@svgdotjs/svg.js';

const userinfo= ref({
    username: 'John Doe',
    email: 'johndoe@example.com',
    phone_num: '123-456-7890',
    gender :'male',
    rank: '无',
    score: 0,
})

onMounted(() => {
    getUserInfo();
});

function getUserInfo() {
    // get user info from server and update userinfo ref
    axios.post(main.url + '/api/getUserInfo', 
    {
        'userid': Cookies.get('userid')
    },
    {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    ).then(response => {
        if (response.status == 200){
            userinfo.value.username = response.data.username;
            userinfo.value.email = response.data.email;
            userinfo.value.phone_num = response.data.phone_num;
            userinfo.value.gender = response.data.gender;
            userinfo.value.rank = getRankLevel(response.data.score);
            userinfo.value.score = response.data.score;
        }
        else{
            ElMessage.error('获取用户信息失败，请稍后再试');
        }
    }).catch(error => {
        console.log(error);
    });
}

</script>

<template>
  <div class="container">
    <div class="row">
      <div>
        <User class="user-icon" />
      </div>
      <div class="info-container">
        <div class="info-item">
            <span class="info-title">用户名</span>
            <span class="info-text">{{userinfo.username}}</span>
        </div>
        <div class="info-item">
            <span class="info-title">性别</span>
            <span class="info-text">{{userinfo.gender}}</span>
        </div>
        <div class="info-item">
            <span class="info-title">邮箱</span>
            <span class="info-text">{{userinfo.email}}</span>
        </div>
        <div class="info-item">
            <span class="info-title">手机号</span>
            <span class="info-text">{{userinfo.phone_num}}</span>
        </div>
        <div class="info-item">
            <span class="info-title">段位</span>
            <span class="info-text">{{userinfo.rank}}</span>
        </div>
        <div class="info-item">
            <span class="info-title">积分</span>
            <span class="info-text">{{userinfo.score}}</span>
        </div>

       </div> 
    </div>
  </div>
</template>

<style>
.container {
  text-align: center;
  background-color: #fdeec4;
}
.user-icon {
    border-color: #333;
    border-width: 1px;
    border-style: solid;
    border-radius: 50%;
    width: 50px;
    position: relative;
    top: 50%;
    max-width: 50px;
    color: #333;
}

.info-container {
    margin-top: 10px;
}

.info-item {
    width: 350px;
    margin-right: 20px;
    margin-bottom: 15px;
    align-items: center;
    display: inline-flex;
}


.info-title {
    width: 100px;
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
    margin-right: 10px;
}

.info-text {
    text-align: left;
    width: 300px;
    display: inline-block;
    height: 50px;
    padding: 10px;
    font-size: 16px;
    border-color: #333;
    border-width: 1px;
    border-style: solid;
    border-radius: 5px;
}

</style>