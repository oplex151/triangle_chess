<script setup lang="ts">
import { ref ,watchEffect} from 'vue';
import axios from 'axios';
import { defineEmits, defineProps } from 'vue';
import { useRouter,useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import main from '@/main';
import Cookies from 'js-cookie';

const uname = ref('');
const password = ref('');
const errorMessage = ref('');
const infoMessage = ref('');
const router = useRouter();

watchEffect(() => {
  if (errorMessage.value !== '') {
      ElMessage({
      message: errorMessage.value,
      grouping: true,
      type: 'error',
      showClose: true
  })
    errorMessage.value = '';
  }
  if (infoMessage.value !== '') {
      ElMessage({
      message: infoMessage.value,
      grouping: true,
      type: 'success',
      showClose: true
  })
    infoMessage.value = '';
  }
});

function adminLogin() {
  if ( password.value === '') {
    errorMessage.value = '密码不能为空';
    return;
  }
  axios.post(main.url+ '/api/adminLogin', 
  {
    'password': password.value
  },
  {
      headers: {'Content-Type':'application/x-www-form-urlencoded'},
  }
  ).then(res => {
    if (res.status == 200) {
      Cookies.set('admin_token',res.data.token);
      infoMessage.value = '登录成功';
      router.push('/admin');
    } else {
      errorMessage.value = '用户名或密码错误';
    }
  }).catch(err => {
    //console.log(err);
    errorMessage.value = '登录失败';
  });
}
</script>

<template>
  <div class="outer-container">
    <div class="background-image"></div>
    <div class="login-container">
      <h1 class="login-title">管理员登录</h1>

      <div class="form-container">
        <form class="login2-form" @submit.prevent="adminLogin">
          <div class="form-group">
            <label for="uname" class="form-label">用户名：</label>
            <input type="text" id="uname" v-model="uname" class="form-input">
          </div>
          <div class="form-group">
            <label for="password" class="form-label">密&nbsp;码：</label>
            <input type="password" id="password" v-model="password" class="form-input">
          </div>
          <div class="form-button">
          <button class="admin-button">
          管理员登入</button >
          </div>
        </form>
      </div> <!-- end of form-container -->
    </div>  <!-- end of login-container -->
  </div>   <!-- end of outer-container -->
</template>

<style scoped>
.go_button{
  display: text-indent;
  position: absolute;
  bottom: 10px;
  color: #00b88d;
}
.outer-container {
  display: center;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.background-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('@/assets/images/login/图1.jpg');
  background-size: cover;
  z-index: -1;
}

.login-container {
  min-width: 600px;
  min-height: 500px;
  padding: 20px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border: 1px solid #ccc;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: rgba(248, 234, 171, 0.8); /* 设置一个半透明的背景色 */
}

.login-title {
  text-align: center;
  font-size: 30px;
  margin-top: 10px;
  margin-bottom: 60px;
  font-family: "SimSun";
}

.form-container {
  display: flex;
  justify-content: center;
}

.login2-form {
  display: flex;
  flex-direction: column;
}

/* 让 form-label 和 form-input 上下对齐 */
.form-group {
  margin-bottom: 70px;
  align-items: flex-start; 
}

.form-label {
  font-weight: bold;
  font-size: 15px; /* 增加字体大小 */
  font-family: "SimSun";
}

.form-input {
  padding: 15px;
  border: 2px solid #ccc; /* 增加边框宽度 */
  border-radius: 5px;
  font-size: 18px; /* 增加输入框字体大小 */
}

.form-button{
  display: flex;
  justify-content: center;
}

.login-button:hover {
  background-color: #d59f39;
  color: #fff;
}

.login-button {
  justify-content: center;
  background-color: #f6bb4e;
  color: #fff;
  border: none;
  border-radius: 15px;
  padding: 15px 0; /* 增加垂直内边距 */
  cursor: pointer;
  font-size: 15px;
  height: 50px;
  width: 200px;
}

.admin-button{
  display: block;
  margin: 0 auto;
  margin-top: 50px;
  background-color: #00b88d;
  color: #fff;
  border: none;
  border-radius: 15px;
  padding: 15px 0; /* 增加垂直内边距 */
  cursor: pointer;
  font-size: 15px;
  height: 50px;
  width: 200px;
  margin-bottom: 30px;
}

.admin-button:hover {
  background-color: #00a177;
  color: #fff;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>


