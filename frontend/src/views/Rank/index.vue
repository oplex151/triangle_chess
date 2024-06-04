<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import Cookies from 'js-cookie';
import { registerSockets, socket, registerSocketsForce, removeSockets } from '@/sockets'
import { ElMessage ,ElMessageBox} from "element-plus";
import { useRouter } from 'vue-router';
import { lives, resetLives } from '@/chesses/Live';
import { onMounted, ref, onUnmounted, computed, getCurrentInstance } from 'vue';
import { User, HomeFilled } from '@element-plus/icons-vue'
import axios from 'axios';
import {getRankLevel} from '@/config/rank.js'
import * as CONST from "@/lib/const.js";
const { proxy } = getCurrentInstance()
const router = useRouter()
const room_id = ref(null)
const room_info = ref(null)
const matching = ref(false)
const userid = Cookies.get('userid')
const totalscore = ref(0)
const rank = ref(0)

onMounted(() => {
    if (!socket.value) {
        socket.value = new VueSocketIO({
            debug: true,
            connection: SocketIO(main.url),
        })
        // // 重新加入房间
        // socket.value.io.emit('joinRoom',{'userid':userid,'room_id':Cookies.get('room_id')})
    }
    registerSockets(sockets_methods, socket.value, proxy);
    console.log(socket.value)

    axios.post(main.url + '/api/getRankScore', {
        'userid': userid,
    },
        {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
    ).then(res => {
        if (res.status == 200) {
            console.log(res.data)
            totalscore.value = res.data.totalscore
            rank.value = res.data.rank
        } else {
            ElMessageBox.alert(
                '网络错误，现在无法获取分数。请稍后再试。',
                {
                    confirmButtonText: 'OK',
                    callback: (action) => {
                        goBackHome()
                },}
        )}
    }).catch(err => {
      if(err.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
    ElMessageBox.alert(
        '网络错误，现在无法进行排位模式。请稍后再试。',
        {
            confirmButtonText: 'OK',
            callback: (action) => {
                goBackHome()
            },
        }
    )
    })
});

const rankname = computed(()=>{
    return getRankLevel(rank.value)
})

//需要注册的监听时间，离开页面记得销毁
const sockets_methods = {
    startRankSuccess(data) {
        matching.value = false;
        room_id.value = data.room_info.room_id;
        room_info.value = data.room_info;
        Cookies.set('room_id', room_id.value);
        Cookies.set('room_info', JSON.stringify(room_info.value));
        ElMessage.success('匹配成功')

        var camp = -1
        for (let i = 0; i < data.room_info.users.length; i++) {
            Cookies.set('user' + i, data.room_info.users[i].userid)
            if (data.room_info.users[i].userid == Cookies.get('userid')) {
                camp = i
            }
        }
        resetLives()
        if (camp >= -1) {
            Cookies.set('camp', camp)
            ElMessage.success('游戏开始,你是' + (camp > 0 ? (camp > 1 ? '金方玩家' : '黑方玩家') : (camp == 0 ? '红方玩家' : '观战者')))
        }
        removeSockets(sockets_methods, socket.value, proxy)
        router.push('/game')
    },
    processWrong(data) {
        ElMessage.error('匹配失败，请重新匹配' + data.status)
        if(data.status == CONST.SESSION_EXPIRED){ //Session expired
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
    },
}

function startRank() {
    matching.value = true;
    socket.value.io.emit('startRank', { userid: Cookies.get('userid') })
}

function goBackHome() {
    removeSockets(sockets_methods, socket.value, proxy)
    Cookies.remove('room_id')
    Cookies.remove('room_info')
    socket.value.io.disconnect()
    socket.value = null
    router.push('/')
}

</script>

<template>
    <div class="background-image"></div>
    <div class="container">
        <button class="button-home" @click="goBackHome()">
            <el-icon style="vertical-align: middle" size="30px">
                <HomeFilled />
            </el-icon>
        </button>
        <p class="background">
        <h1 class="title">排位页面</h1>
        </p>
        
        <p>
            <h3 class = "score" :class="rankname">
                {{rankname}}    <br/> 
                {{totalscore}} 分
            </h3>
        </p>
        <button class="button-match" @click="startRank">开始排位</button>

        <div v-if="matching" class="loading">
            <div class="spinner">
                <div class="cube1"></div>
                <div class="cube2"></div>
            </div>
            <p class="info_text">正在匹配排位对手，请稍候...</p>
        </div>
    </div>
</template>

<style>
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

.container {
    text-align: center;
    margin-top: 20px;
}

.background {
    margin-top: 100px;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 400px;
    border-radius: 10px;
    text-align: center;
}

.button-home {
    position: absolute;
    top: 20px;
    left: 20px;
    background-color: #ecb920;
    border: none;
    padding: 10px 20px;
    border-radius: 40px;
    font-size: 18px;
    cursor: pointer;
    z-index: 9999;
}

.button-home:hover {
    background-color: #e0a61b;
}

.title {
    font-size: 24px;
    font-weight: bold;
    font-family: "KaiTi", "楷体";
    color: #000;
    text-align: center;
}

@font-face {
    font-family: "阿里妈妈东方大楷 Regular";font-weight: 400;src: url("//at.alicdn.com/wf/webfont/uWrOvAFUee6Z/j21mxPjobcF7.woff2") format("woff2"),
    url("//at.alicdn.com/wf/webfont/uWrOvAFUee6Z/V0SgC0T8YlgT.woff") format("woff");
    font-display: swap;
}
@font-face {
        font-family: "Bitstream Vera Serif Bold";
        src: url("https://mdn.github.io/css-examples/web-fonts/VeraSeBd.ttf");
        
    }
.score{
    font-size: 24px;
    font-family: "Bitstream Vera Serif Bold","阿里妈妈东方大楷 Regular","楷体";
    color: #000;
    background-color: #f1d88c;
    text-align: center;
    max-width: 40%;
    margin: auto;
    margin-top: 2%;
    border-radius: 10px;
}
.loading {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 9998;
    text-align: center;
}

.button-match {
    font-family: "阿里妈妈东方大楷 Regular","楷体";
    display: block;
    
    margin: 10% auto;
    padding: 10px 20px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    cursor: pointer;
}

.button-match:hover {
    background-color: #f1d88c;
}

.info_text {
    font-size: 20px;
    font-weight: bold;
    color: #333;
}

.spinner {
    position: relative;
    top: 50%;
    margin: 0 auto;
    width: 50px;
    height: 50px;
}


.cube1,
.cube2 {
    background-color: #ecb920;
    width: 30px;
    height: 30px;
    position: absolute;
    top: 0;
    left: 0;

    -webkit-animation: sk-cubemove 1.8s infinite ease-in-out;
    animation: sk-cubemove 1.8s infinite ease-in-out;
}

.cube2 {
    -webkit-animation-delay: -0.9s;
    animation-delay: -0.9s;
}

@-webkit-keyframes sk-cubemove {
    25% {
        -webkit-transform: translateX(42px) rotate(-90deg) scale(0.5)
    }

    50% {
        -webkit-transform: translateX(42px) translateY(42px) rotate(-180deg)
    }

    75% {
        -webkit-transform: translateX(0px) translateY(42px) rotate(-270deg) scale(0.5)
    }

    100% {
        -webkit-transform: rotate(-360deg)
    }
}

@keyframes sk-cubemove {
    25% {
        transform: translateX(42px) rotate(-90deg) scale(0.5);
        -webkit-transform: translateX(42px) rotate(-90deg) scale(0.5);
    }

    50% {
        transform: translateX(42px) translateY(42px) rotate(-179deg);
        -webkit-transform: translateX(42px) translateY(42px) rotate(-179deg);
    }

    50.1% {
        transform: translateX(42px) translateY(42px) rotate(-180deg);
        -webkit-transform: translateX(42px) translateY(42px) rotate(-180deg);
    }

    75% {
        transform: translateX(0px) translateY(42px) rotate(-270deg) scale(0.5);
        -webkit-transform: translateX(0px) translateY(42px) rotate(-270deg) scale(0.5);
    }

    100% {
        transform: rotate(-360deg);
        -webkit-transform: rotate(-360deg);
    }
}


/* 段位颜色 */
.无{
    background-color: transparent;
}
.菜鸟{
    background-color: #918e8b;
}
.青铜{
    background-color: #cd7f32;
}
.白银{
    background-color: #f2f2f2;
}
.黄金{
    background-color: #ffd700;
}
.白金{
    background-color: #cff4e9f2;
}
.钻石{
    background-color: #b9f2ff;
}
.王者{
    background-color: #e87000;
}
.超神{
    background-image: url("@/assets/images/game/超神.jpg");
}
</style>