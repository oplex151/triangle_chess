<script setup>
import * as CONST from '@/lib/const.js'
import axios from 'axios';
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Cookies from 'js-cookie'
import { ElMessage } from 'element-plus'
import main from '@/main.js'

const router = useRouter()

const new_password = ref('')
const confirm_password = ref('')
const vertify_code = ref('')
const vertify_have_send = ref(false)
const vertify_ok = ref(false)
const phone_num = ref('')

onMounted(() => {
    axios.post(main.url + '/api/getUserInfo', {

        'userid': Cookies.get('userid')
    }, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(response => {
        if (response.status === 200) {
            phone_num.value = response.data.phone_num
        }
        else {
            ElMessage.error('获取用户信息失败')
        }
    })
   .catch(error => {
        if (error.response.status == CONST.SESSION_EXPIRED) {
            Cookies.remove('room_id')
            Cookies.remove('userid')
            Cookies.remove('room_info')
            Cookies.remove('username')
            Cookies.remove('camp')
            ElMessage({
                message: '会话过期，请重新登录',
                grouping: true,
                type: 'error',
                showClose: true
            })
            router.replace('/login')
        }
        else
            ElMessage.error('获取用户信息失败')
   });
})

function senOorGetVertifyCode () {
    if(vertify_have_send.value){
        vertifyCode()
    }
    else{
        getVerificationCode()
    }
}

function getVerificationCode() {
  if (phone_num.value.length!== 11) {
    ElMessage.error('手机号码格式错误')
    return
  }
  //verificationButtonDisabled.value = true;
  axios.post(main.url + '/api/getVerificationCode', {
    'phone_num': phone_num.value,
    'category': "authentication"
  },{
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(res => {
    if (res.status === 200) {
      ElMessage.success('验证码已发送');
      vertify_have_send.value = true
      //startCountdown();
    } else {
      ElMessage.error('验证码发送失败');
      //verificationButtonDisabled.value = false;
    }
  }).catch(error => {
    if (error.response.status == 506) {
      // 请求已发出，但服务器响应状态码不在 2xx 范围内
      ElMessage.error('请勿重复登录');
      if (Cookies.get('userid') !== undefined) {
        router.push('/');
      }
    }
    else if(error.response.status == 501){
        ElMessage.error('用户不存在');
    }
    else if (error.response.status == CONST.BANNED_USER) {
        ElMessage.error('账号被封禁，您可以申诉');
      router.push('/appeal');
    }
    else if (error.response.status == 562) {
        ElMessage.error('验证码发送过于频繁，请稍后再试');
    } 
    else if (error.response.status == 563) {
        ElMessage.error('验证码错误');
    }
    else {
        ElMessage.error('请求失败，请重试');
    }
    //verificationButtonDisabled.value = false;
  });
};

function vertifyCode () {
    console.log('vertifyCode')
    if (vertify_code.value.length !== 6) {
        ElMessage.error('验证码格式错误')
        return
    }
    axios.post(main.url + '/api/checkVerificationCode', {
        'phone_num': phone_num.value,
        'code': vertify_code.value,
    }, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(response => {
        if (response.status === 200) {
            vertify_ok.value = true
            ElMessage.success('验证码正确')
        }
    })
    .catch(error => {
        if (error.response.status = 563) 
            ElMessage.error('验证码错误')
        else if (error.response.status = 562) 
            ElMessage.error('请勿用同一手机号码频繁请求')
        else 
            ElMessage.error('请求失败，请重试')
    });
}


function savePassword() {
    if (new_password.value.length < 8) {
        ElMessage.error('密码长度至少6位')
        return
    }

    if (new_password.value !== confirm_password.value) {
        ElMessage.error('两次密码输入不一致')
        return
    }

    axios.post(main.url + '/api/changePassword', {
        'userid': Cookies.get('userid'),
        'password': new_password.value,
    }, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(response => {
        if (response.status === 200) {
            ElMessage.success('密码修改成功')
            router.push('/login')
        }
    })
   .catch(error => {
        if (error.response.status == CONST.USER_NOT_EXIST) {
            ElMessage.error('用户不存在')
        }
        else if (error.response.status == CONST.BANNED_USER) {
            ElMessage.error('账号被封禁，您可以申诉')
            router.push('/appeal')
        }
        else if (error.response.status == CONST.SESSION_EXPIRED) {
            ElMessage.error('会话过期，请重新登录')
            Cookies.remove('room_id')
            Cookies.remove('userid')
            Cookies.remove('room_info')
            Cookies.remove('username')
            Cookies.remove('camp')
            ElMessage({
                message: '会话过期，请重新登录',
                grouping: true,
                type: 'error',
                showClose: true
            })
            router.push('/login')
        }
        else {
            ElMessage.error('请求失败，请重试')
        }
    });
}
</script>

<template>
    <div class="info-container">
        <div class="info-item">
            <span class="info-title">手机号</span>
            <input type="text" v-model="phone_num"
            class="info-text"
            disabled="true">
            <button  class='vertify-code'
            :disabled="vertify_ok"
            @click="senOorGetVertifyCode">
                {{vertify_have_send?'提交验证码':'获取验证码'}}
            </button>
            </input>
        </div>
        <div class="info-item" >
            <span class="info-title">验证码</span>
            <input type="text" v-model="vertify_code"
            class="info-text"
            placeholder="请输入验证码">
            </input>
        </div>
        <div class="info-item" >
            <span class="info-title">密码</span>
            <input type="text" v-model="new_password"
            :disabled="!vertify_ok"
            class="info-text"
            placeholder="请输入新的密码">
            </input>
        </div>
        <div class="info-item" >
            <span class="info-title">确认密码</span>
            <input type="text" v-model="confirm_password"
            :disabled="!vertify_ok"
            class="info-text"
            placeholder="请再次输入密码">
            </input>
        </div>
        <div>
        <button :class="vertify_ok?'save-button':'disabled-button'"
        @click="savePassword">保存</button>
        </div>
    </div>
</template>

<style scoped>


.info-container {
    margin-top: 40px;
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

.edit-button {
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    margin-top: 20px;
    cursor: pointer;
}

.edit-button:hover {
    background-color: #555;
}
.save-button {
    margin-right: -70px;
    margin-left: 100px;
    background-color: #8be516;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    margin-top: 20px;
    cursor: pointer;
    min-width: 100px;
}

.save-button:hover {
    background-color: #70c110;
}

.disabled-button {
    background-color: #ccc;
    margin-top: 20px;
    cursor: not-allowed;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    margin-top: 20px;
    cursor: pointer;
    min-width: 100px;
}

.vertify-code {
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 5px;
    padding: 10px;
    cursor: pointer;
    position:absolute;
    z-index: 100;
}

.vertify-code:hover {
    background-color: #555;
}
</style>