<script setup>
import { ref, watch ,onMounted} from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import main from '@/main';
import Cookies from 'js-cookie';

const uname = ref('');
const password = ref('');
const errorMessage = ref('');
const router = useRouter();

onMounted(() => {
  if (Cookies.get('userid') !== undefined) {
    router.push('/');
  }
});

watch(errorMessage, (oldValue ,newValue) => {
  if (newValue !== oldValue && errorMessage.value !== '') {
      ElMessage({
      message: errorMessage.value,
      grouping: true,
      type: 'error',
      showClose: true
  })
    errorMessage.value = '';
  }
});


const login = () => {
  if (uname.value === '' || password.value === '') {
    errorMessage.value = '用户名或密码不能为空';
    
    return;
  }
  axios.post(main.url+ '/api/login', {
    'username': uname.value,
    'password': password.value
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }
  ).then(res => {
    if (res.status == 200) {
      Cookies.set('userid',res.data.userid);
      // errorMessage.value=Cookies.get('userid');
      router.push('/');
    } else {
      errorMessage.value = '用户名或密码错误';
    }
  })  
  .catch(error => {
    // 捕获错误
    if (error.response.status == 506) {
      // 请求已发出，但服务器响应状态码不在 2xx 范围内
      errorMessage.value = '请勿重复登录';
      if (Cookies.get('userid') !== undefined) {
        router.push('/');
      }
    } 
    else if(error.response.status == 501){
      errorMessage.value = '用户不存在';
    }
    else {
      errorMessage.value = '请求错误';
    }
    
  });
};

</script>

<template>
  <div class="outer-container">
    <div class="background-image"></div>
    <div class="login-container">
      <h1 class="login-title">用户登录</h1>

      <div class="form-container">
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="uname" class="form-label">用户名：</label>
            <input type="text" id="uname" v-model="uname" class="form-input">
          </div>
          <div class="form-group">
            <label for="password" class="form-label">密&nbsp;码：</label>
            <input type="password" id="password" v-model="password" class="form-input">
          </div>
          <div class="form-button">
          <el-button native-type="submit" class="login-button">登录</el-button>
          </div>
        </form>
      </div> <!-- end of form-container -->
      <router-link to="/register" class="go_button">立即注册！</router-link>
    </div>  <!-- end of login-container -->
  </div>   <!-- end of outer-container -->
</template>

<style scoped>
.go_button{
  display: text-indent;
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
  width: 600px;
  height: 500px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 20px;
  position: relative;
  transform: translate(-0%, -0%);
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

.login-form {
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

.error-message {
  color: red;
  margin-top: 10px;
}
</style>


