<script setup>
import main from '@/main';
import axios from 'axios';
import Cookies from 'js-cookie';
import { onMounted, ref } from 'vue';
import { getRankLevel } from '@/lib/rank';
import { ElMessage } from 'element-plus';
import FaceGenerator from '../FaceGen/FaceGenerator.vue';
import router from '@/router';
import * as CONST from "@/lib/const.js";
 

const userinfo= ref({
    username: '',
    email: '',
    phone_num: '',
    gender :'',
    rank: '无',
    score: 0,
})

const image_path = ref()
const base64 = ref()


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
            userinfo.value.rank = getRankLevel(response.data.rank);
            userinfo.value.score = response.data.score;
            //console.log(response.data.image_path)
            image_path.value = main.url + response.data.image_path;
        }
        else{
            ElMessage.error('获取用户信息失败，请稍后再试');
        }
    }).catch(error => {
        //console.log(error);
        if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
    });
}

const imgPreview = ref()
const is_select_img = ref(false)
const haven_upload = ref(true)

function chooseImg (event) {
    let file = event.target.files[0]
    let reader = new FileReader()
    let img = new Image()
    // 读取图片
    reader.readAsDataURL(file)
    // 读取完毕后的操作
    reader.onloadend = (e) => {
        img.src = e.target.result
        // 这里的e.target就是reader
        // //console.log(reader.result)
        // reader.result就是图片的base64字符串
        base64.value = reader.result
        // //console.log(base64.value)
    }
    // 预览图片
    let canvas = imgPreview.value
    let context = canvas.getContext('2d')
    img.onload = () => {
        img.width = 100
        img.height = 100
        // 设置canvas大小
        canvas.width = 100
        canvas.height = 100
        // 清空canvas
        context.clearRect(0, 0, 100, 100)
        // 画图
        context.drawImage(img, 0, 0, 100, 100)
    }
    haven_upload.value = false
}

function uploadImg () {
    axios.post(main.url + '/api/uploadImage', {
        'image': base64.value,
        'userid': Cookies.get('userid')
    },
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    ).then(response => {
        if (response.status == 200) {
            image_path.value =  main.url+response.data.image_path
            window.location.reload();
            haven_upload.value = true
        }
        else {
            //console.log('上传失败')
        }
    }).catch(error => {
        //console.log(error)
        if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
    })
}

function justIt (data) {
    is_select_img.value = false
    base64.value = data.src
    //console.log(data.src)
    let img = new Image()
    img.src = data.src
    let canvas = imgPreview.value
    let context = canvas.getContext('2d')
    img.onload = () => {
        img.width = 100
        img.height = 100
        // 设置canvas大小
        canvas.width = 100
        canvas.height = 100
        // 清空canvas
        context.clearRect(0, 0, 100, 100)
        // 画图
        context.drawImage(img, 0, 0, 100, 100)
    }
    haven_upload.value = false
}

const email = ref(userinfo.value.email)
const phone_num = ref(userinfo.value.phone_num)
const gender = ref(userinfo.value.gender)
const vertify_code = ref('')
const vertify_ok = ref(false)
const vertify_have_send = ref(false)
const editMode = ref(false)

function cancelEdit () {
    editMode.value = false
    email.value = userinfo.value.email
    phone_num.value = userinfo.value.phone_num
    gender.value = userinfo.value.gender
    vertify_code.value = ''
    vertify_ok.value = false
    vertify_have_send.value = false
}

function senOorGetVertifyCode () {
    if(vertify_have_send.value){
        vertifyCode()
    }
    else{
        getVerificationCode()
    }
}

function getVerificationCode() {
    console.log('getVerificationCode')
  //verificationButtonDisabled.value = true;
  axios.post(main.url + '/api/getVerificationCode', {
    'phone_num': userinfo.value.phone_num,
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
    if(error.response.status == 501){
      ElMessage.error('用户不存在')
    }
    else if (error.response.status == CONST.BANNED_USER) {
        ElMessage.error('用户被封禁，您可以申诉');
      router.push('/appeal');
    }
    else if (error.response.status == 562) {
        ElMessage.error('请勿用同一手机号码频繁请求');
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
        'phone_num': userinfo.value.phone_num,
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

function startEdit(){
    editMode.value = true
    email.value = userinfo.value.email
    phone_num.value = userinfo.value.phone_num
    gender.value = userinfo.value.gender
}

function saveEdit () {
    editMode.value = false
    axios.post(main.url + '/api/changeUserInfo', {
        'userid': Cookies.get('userid'),
        'email': email.value,
        'phone_num': phone_num.value,
        'gender': gender.value
    },
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    ).then(response => {
        if (response.status == 200) {
            userinfo.value.email = email.value
            userinfo.value.phone_num = phone_num.value
            userinfo.value.gender = gender.value
            ElMessage.success('修改成功')
            cancelEdit()
        }
        else {
            ElMessage.error('修改失败，请稍后再试')
            cancelEdit()
        }
    }).catch(error => {
        //console.log(error)
        cancelEdit()
        if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
    })
}

</script>

<template>
  <div class="container">
    <div class="row">
        <div >
            <div class="user-imgs">
                <img class="user-img" 
                :src="image_path" 
                v-if="image_path"/>
                <!-- 预览图片 -->
                <canvas 
                ref="imgPreview" 
                class="user-img"
                ></canvas>
            </div>
            <span class="img-upload-container">
                <!-- 选择图片 -->
                <div class="image-upload" >
                    上传图片
                    <input class="file-input"  type="file"
                    accept="image/*"
                    @change="chooseImg" />
                </div>
                <!-- 提交图片 -->
                <button class="file-upload-buttun" @click="uploadImg">提交图片
                </button> 
                <span v-if="!haven_upload" class="waring">还没有提交哦!</span>
            </span>
            <button class="random-button"
            @click="is_select_img = true">
                想要一张随机的抽象头像吗？
            </button>
            <div class="select-img" v-if="is_select_img">
                <FaceGenerator class="face-generator"
                @cancelSelect="is_select_img = false"
                @justIt="justIt"/>
            </div>
        </div>
        <div class="info-container">
            <div class="info-item">
                <span class="info-title">用户名</span>
                <span class="info-text">{{userinfo.username}}</span>
            </div>
            <div class="info-item">
                <span class="info-title">性别</span>
                <span class="info-text" v-if="!editMode">
                    {{userinfo.gender== 'female' ? '女' : userinfo.gender== 'male' ? '男' : '不愿透露'}}
                </span>
                <el-radio-group v-if="editMode" v-model="gender"
                class="info-text">
                    <el-radio value="male" size="large">男</el-radio>
                    <el-radio value="female" size="large">女</el-radio>
                    <el-radio value="" size="large">不愿透露</el-radio>
                </el-radio-group>
            </div>
            <div class="info-item">
                <span class="info-title">邮箱</span>
                <span class="info-text" v-if="!editMode">{{userinfo.email}}</span>
                <input type="email" v-model="email"
                v-if="editMode"
                class="info-text"
                placeholder="请输入邮箱">
                </input>
            </div>
            <div class="info-item">
                <span class="info-title">手机号</span>
                <span class="info-text" v-if="!editMode || !vertify_ok"
                >{{userinfo.phone_num ? userinfo.phone_num : '(未绑定，您将无法申诉)'}}</span>
                <input type="text" v-model="phone_num"
                v-if="editMode && vertify_ok"
                class="info-text"
                placeholder="请输入手机号">
                <button v-if="editMode" class='vertify-code'
                :disabled="vertify_ok"
                @click="senOorGetVertifyCode">
                    {{vertify_have_send?'提交验证码':'获取验证码'}}
                </button>
                </input>
            </div>
            <div class="info-item" v-if="editMode">
                <span class="info-title">验证码</span>
                <input type="text" v-model="vertify_code"
                class="info-text"
                placeholder="请输入验证码">
                </input>
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
        <button class="edit-button" @click="startEdit"
        v-if="!editMode"
        >修改</button>
        <button class="edit-button" @click="cancelEdit"
        v-if="editMode"
        >放弃</button>
        <button class="save-button" @click="saveEdit"
        v-if="editMode"
        >提交</button>
    </div>
  </div>
</template>

<style>

.select-img {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: 9999;
}

.face-generator {
    position: relative;
    width: 600px;
    height: 700px;
}

.img-upload-container {
    display: inline-block;
    position: relative;
    left: 200px;
    width: 100px;
    height: 100px;
    bottom: 40px;
}

.user-imgs{
    position: relative;
    top: 100px;
    right: 150px;
}

.user-img{
    width: 150px;
    height: 150px;
    border-radius: 50%;
    position: absolute;
    bottom: 20px;
}

.image-upload{
    position: relative;
    display: inline-block;
    overflow: hidden;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30px;
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.image-upload:hover{
    background-color: #555;
}

.file-input{
    position: absolute;
    overflow: hidden;
    right: 0;
    top: 0;
    opacity: 0;
}

.file-upload-buttun{
    font-size: 16px;
    display: inline-block;
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 30px;
    background-color: #333;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.file-upload-buttun:hover{
    background-color: #555;
}

.waring {
    color: #f40404;
    font-size: 14px;
    position: absolute;
    bottom: 30px;
    left: 10px;
}

.random-button {
    background-color: #fdeec4;
    border-color: #fdeec4;;
    display: inline-block;
    border-width: 0px;
    color:chocolate;
    position: relative;
    left: 70px;
    top: 60px;
}

.random-button:hover {
    color: #f7c78e;
}

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
}

.save-button:hover {
    background-color: #70c110;
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