<script setup>
import { ref, watch ,onMounted, watchEffect} from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import main from '@/main';
import Cookies from 'js-cookie';
import * as CONST from '@/lib/const';

const uname = ref('');
const password = ref('');
const phoneNum = ref('');
const verificationCode = ref('');
const errorMessage = ref('');
const infoMessage = ref('');
const router = useRouter();
const loginMethod = ref('username'); // 用于切换登录方式

onMounted(() => {
  if (Cookies.get('userid') !== undefined) {
    router.push('/');
  }
  //console.log(main.url)
});

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

const num = 8 //失效时间是几小时
const expire_time= new Date(new Date().getTime() + num * 60 * 60 * 1000);

// 新增的响应式变量
const verificationButtonDisabled = ref(false); // 控制验证码按钮的状态
const verificationButtonText = ref('获取验证码');
const countdown = ref(60); // 验证码倒计时

// 获取验证码的逻辑
const getVerificationCode = () => {
  if (!phoneNum.value || !/^1[3-9]\d{9}$/.test(phoneNum.value)) {
    ElMessage.error('请输入有效的手机号');
    return;
  }

  verificationButtonDisabled.value = true;
  console.log('phone_num is' + phoneNum);

  axios.post(main.url + '/api/getVerificationCode', {
    'phone_num': phoneNum.value,
    'category': "authentication"
  },{
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(res => {
    if (res.status === 200) {
      ElMessage.success('验证码已发送');
      startCountdown();
    } else {
      ElMessage.error('验证码发送失败');
      verificationButtonDisabled.value = false;
    }
  }).catch(err => {
    console.log(err);
    ElMessage.error('请求失败，请重试');
    verificationButtonDisabled.value = false;
  });
};

// 倒计时逻辑
const startCountdown = () => {
    let countdown = 60; // 倒计时秒数
    verificationButtonText.value = `${countdown}秒后重新获取`;
    
    const timer = setInterval(() => {
        countdown--;
        if (countdown <= 0) {
        clearInterval(timer);
        verificationButtonText.value = '获取验证码';
        verificationButtonDisabled.value = false;
        } else {
        verificationButtonText.value = `${countdown}秒后重新获取`;
        }
    }, 1000);
};

const phoneLogin = () => {
  if (phoneNum.value === '' || verificationCode.value === '') {
    errorMessage.value = '手机号或验证码不能为空';
    return;
  }
  axios.post(main.url+ '/api/phoneLogin', {
    'phone_num': phoneNum.value,
    'code': verificationCode.value
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }
  ).then(res => {
    if (res.status == 200) {
      console.log("result is "+res.data.userid+','+res.data.username);
      Cookies.set('userid',res.data.userid,{expires:expire_time});
      Cookies.set('username',res.data.username,{expires:expire_time});
      infoMessage.value = '登录成功';
      router.push('/');
    }
    else {
      errorMessage.value = '手机号或验证码错误';
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
    else if(error.response.status == 502){
      errorMessage.value = '密码错误';
    }
    else if (error.response.status == CONST.BANNED_USER) {
      errorMessage.value = '账号被封禁，您可以申诉';
      router.push('/appeal');
    }
    else if (error.response.status === 562) {
        errorMessage.value = '请勿用同一手机号码频繁请求!'
    } 
    else if (error.response.status === 563) {
        errorMessage.value = '验证码错误!';
    }
    else {
      errorMessage.value = '请求错误';
    }
  });
};

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

      
      Cookies.set('userid',res.data.userid,{expires:expire_time});
      Cookies.set('username',res.data.username,{expires:expire_time});
      infoMessage.value = '登录成功';
      router.push('/');
    }
    else {
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
    else if(error.response.status == 502){
      errorMessage.value = '密码错误';
    }
    else if (error.response.status == CONST.BANNED_USER) {
      errorMessage.value = '账号被封禁，您可以申诉';
      router.push('/appeal');
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
      <div class="nav-container">
        <el-button :type="loginMethod === 'username' ? 'primary' : 'default'"
                   @click="loginMethod = 'username'"
                   class="nav-button">
          用户登录
        </el-button>
        <el-button :type="loginMethod === 'phone' ? 'primary' : 'default'"
                   @click="loginMethod = 'phone'"
                   class="nav-button">
          手机验证码登录
        </el-button>
      </div>

      <div class="form-container">
        <!-- 用户名密码登录表单 -->
        <form v-if="loginMethod === 'username'" class="login-form" @submit.prevent="login">
          <div class="form-group">
            <label for="uname" class="form-label">用户名：</label>
            <input type="text" id="uname" v-model="uname" class="form-input">
          </div>
          <div class="form-group">
            <label for="password" class="form-label">密&nbsp;码：</label>
            <input type="password" id="password" v-model="password" class="form-input">
          </div>
          <div class="form-button">
          <el-button
          native-type="submit" class="login-button">登录</el-button>
          </div>
        </form>

        <!-- 手机验证码登录表单 -->
        <form v-else class="login-form" @submit.prevent="phoneLogin">
          <div class="form-group">
            <label for="phoneNum" class="form-label">手机号：</label>
            <input type="text" id="phoneNum" v-model="phoneNum" class="form-input">
            <el-button @click="getVerificationCode" :disabled="verificationButtonDisabled" class="verify-button">
              {{ verificationButtonText }}
            </el-button>
          </div>
          <div class="form-group">
            <label for="verificationCode" class="form-label">验证码：</label>
            <input type="text" id="verificationCode" v-model="verificationCode" class="form-input">
          </div>
          <div class="form-button">
            <el-button native-type="submit" class="login-button">登录</el-button>
          </div>
        </form>
      </div> <!-- end of form-container -->
      <router-link
      to="/register" class="go_button">立即注册！</router-link>
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

.nav-container {
  display: flex;
  justify-content: center;
  margin-bottom: 20px; /* 适当的导航栏和表单间距 */
}

.nav-button {
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

.verify-button {
  background-color: #f6bb4e;
  color: #fff;
  border: none;
  border-radius: 5px;
  height: 40px;
  cursor: pointer;
}

.verify-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
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


