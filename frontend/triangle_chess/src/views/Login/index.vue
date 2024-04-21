<script setup>
import { ref } from 'vue';

const uname = ref('');
const password = ref('');
const errorMessage = ref('');

const login = async () => {
  try {
    const params = new URLSearchParams();
    params.append('uname', uname.value);
    params.append('password', password.value);
    const paramsString = 'http://localhost:9002/user/login?' + params.toString();
    const response = await fetch(paramsString, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        uname: uname.value,
        password: password.value
      })
    });

    if (!response.ok) {
      throw new Error('登录失败');
    }

    window.location.href = '/';
  } catch (error) {
    errorMessage.value = '用户名或密码错误';
  }
};

const register = async() =>{
  try{

      const params = new URLSearchParams();
      params.append('uname', uname.value);
      params.append('password', password.value);
      const paramsString = 'http://localhost:9002/user/register?' + params.toString();
      const response = await fetch(paramsString, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          uname: uname.value,
          password: password.value
        })
      });
    if (!response.ok) {
      throw new Error('注册失败');
    }
  }
  catch (error) {
    errorMessage.value = '网络异常，请稍后再试';
  }
}
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
            <label for="password" class="form-label">密&nbsp;&nbsp;&nbsp;码：</label>
            <input type="password" id="password" v-model="password" class="form-input">
          </div>
          <div class="form-button">
          <button type="submit" class="login-button">登录</button>
          </div>
        </form>
      </div> <!-- end of form-container -->
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    </div>  <!-- end of login-container -->
  </div>   <!-- end of outer-container -->
</template>

<style scoped>
.outer-container {
  display: flex;
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

  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: rgba(255, 255, 255, 0.8); /* 设置一个半透明的背景色 */
}

.login-title {
  text-align: center;
  font-size: 30px;
  margin-bottom: 80px;
}

.form-container {
  display: flex;
  justify-content: center;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 70px;
  align-items: flex-start; /* 让 form-label 和 form-input 上下对齐 */
}

.form-label {
  font-weight: bold;
  font-size: 25px; /* 增加字体大小 */
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
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 15px;
  padding: 15px 0; /* 增加垂直内边距 */
  cursor: pointer;
  font-size: 25px;
  height: 70px;
  width: 250px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>


