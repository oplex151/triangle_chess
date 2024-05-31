<script setup>
import main from '@/main';
import { User, HomeFilled } from '@element-plus/icons-vue'
import axios from 'axios';
import Cookies from 'js-cookie';
import { onMounted, ref } from 'vue';
import { getRankLevel } from '@/config/rank';
import { ElMessage } from 'element-plus';
import FaceGenerator from '../FaceGen/FaceGenerator.vue';

 

const userinfo= ref({
    username: 'John Doe',
    email: 'johndoe@example.com',
    phone_num: '123-456-7890',
    gender :'male',
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
            userinfo.value.rank = getRankLevel(response.data.score);
            userinfo.value.score = response.data.score;
            console.log(response.data.image_path)
            image_path.value = main.url + response.data.image_path;
        }
        else{
            ElMessage.error('获取用户信息失败，请稍后再试');
        }
    }).catch(error => {
        console.log(error);
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
        // console.log(reader.result)
        // reader.result就是图片的base64字符串
        base64.value = reader.result
        // console.log(base64.value)
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
            console.log('上传失败')
        }
    }).catch(error => {
        console.log(error)
    })
}

function justIt (data) {
    is_select_img.value = false
    base64.value = data.src
    console.log(data.src)
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
    margin-left: 200px;
    width: 100px;
    height: 100px;
    bottom: 30px;
}

.user-imgs{
    position: relative; 
    right: 150px;
    top:130px;
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
    color: #555;
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
    bottom: 10px;
    left: 100px;
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

</style>