<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { onMounted, ref, getCurrentInstance } from 'vue'
import { registerSockets, socket } from '@/sockets'
import axios from 'axios'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'
import * as CONST from '@/lib/const.js'
import { User, HomeFilled } from '@element-plus/icons-vue'

const { proxy } = getCurrentInstance()
const router = useRouter()
const room_id = ref(null)
const new_room_id = ref(null)
const room_info = ref(null)
// 格式提示：
// room_info:{
//   room_id:xxx,
//   room_type:xxx,
//   users:[
//     {
//       userid:1,
//       username:'user1',
//     },
//     ...
//   ],
//   holder:{
//     userid:1,
//     username:'user1'
//   }
//}

const sockets_methods = {
  createRoomSuccess(data){
    Cookies.set('room_id',data.room_id)
    room_id.value = data.room_id
    room_info.value = data.room_info

    //debug
    console.log(room_id.value)
    console.log(room_info.value)

    ElMessage.success('创建房间成功')
  },
  joinRoomSuccess(data){
    if (data.userid == Cookies.get('userid')){
      Cookies.set('room_id',data.room_id)
      room_id.value = data.room_id
      room_info.value = data.room_info
      ElMessage.success('加入房间成功')
    }
    else{
      room_info.value = data.room_info
      ElMessage.success('玩家'+data.username+'加入房间')
    }
  },
  processWrong(data){
    switch(data.status){
      case CONST.ALREADY_IN_ROOM:
        ElMessage.error('已经在房间中')
        break
      case CONST.ROOM_NOT_EXIST:
        ElMessage.error('不存在此房间')
        if(data.message){
          ElMessage.error(data.message)
        }
        break
      case CONST.NOT_IN_ROOM:
        ElMessage.error('不在房间中')
        break
      case CONST.ROOM_NOT_ENOUGH:
        ElMessage.error('房间人数不足')
        break
      case CONST.GAME_CREATE_FAILED:
        ElMessage.error('游戏创建失败:未知错误')
        break
      default:
        ElMessage.error('未知错误')
    }
  },
  leaveRoomSuccess(data){
    if (data.userid == Cookies.get('userid')){
      Cookies.remove('room_id')
      Cookies.remove('room_info')
      room_id.value = null
      room_info.value = null
      ElMessage.success('离开房间成功')
    }
    else{
      ElMessage.success('玩家'+data.username+'离开房间')
      if (room_info.value.holder.userid != Cookies.get('userid') && data.room_info.holder.userid == Cookies.get('userid')) 
        ElMessage.success('房主离开房间，你是新的房主')
      room_info.value = data.room_info
    }
  },
  createGameSuccess(data){
    
    Cookies.set('room_info',JSON.stringify(data.room_info))

    ElMessage.info('创建成功')
    room_info.value = data.room_info
    var camp = -1
    for (let i = 0; i < data.room_info.users.length; i++){
      Cookies.set('user'+i,data.room_info.users[i].userid)
      if (data.room_info.users[i].userid == Cookies.get('userid')){
        camp = i
      }
    }
    if (camp>=-1){
      Cookies.set('camp',camp)
      console.log(Cookies.get('camp'))
      ElMessage.success('游戏开始,你是'+camp>0?(camp>1?'金方玩家':'黑方玩家'):camp==0?'红方玩家':'观战者')
    }
    router.replace('/game')
  }

}

onMounted(() => {
  establishConnection()
  if (Cookies.get('room_id') && Cookies.get('room_info')) {
    room_id.value = Cookies.get('room_id')
    room_info.value = JSON.parse(Cookies.get('room_info'))
  }
})

function establishConnection() {
  if (!socket.value) {
    socket.value = new VueSocketIO({
      debug: true,
      connection: SocketIO(main.url),
    })
    // 注册socket监听
    registerSockets(sockets_methods, socket.value, proxy)
  }
  socket.value.io.on('disconnect', () => {
    socket.value = null
  })
}
function createRoom() {
  socket.value.io.emit('createRoom', { 'userid': Cookies.get('userid') })
}
function joinRoom() {
  socket.value.io.emit('joinRoom', { 'room_id': new_room_id.value, 'userid': Cookies.get('userid') })
  new_room_id.value = null
}
function leaveRoom() {
  socket.value.io.emit('leaveRoom', { 'room_id': Cookies.get('room_id'), 'userid': Cookies.get('userid') })
}
function createGame() {
  axios.post(main.url + '/api/game/create',
    { 'room_id': room_id.value, 'userid': Cookies.get('userid') },
    {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
}
function goBackHome(){
  if (Cookies.get('room_id')){
    leaveRoom()
  }
  router.push('/')
}
</script>

<template>
  <div class="background-image">  </div>
  <div class="container">
    <button class="button-home" @click="goBackHome()">
      <el-icon style="vertical-align: middle" size="30px">
        <HomeFilled />
      </el-icon>
    </button>
    <div class="room-title" v-if="room_id">
      <span >用户 </span>
      <span class="emphasis-text">
        {{ room_info.holder.username }}  
      </span>
      <span> 的房间 </span>
      <span class="emphasis-text">
        {{ room_info.room_id }}
      </span>
    </div>


    <div class="create-room">
      <button class="button-create"
      v-if="!room_id"
      @click="createRoom()">
      创建房间
      </button>
    </div>



    <div class="join-room">
      <input 
      class = "input-join"
      v-if="!room_id" 
      v-model="new_room_id" 
      placeholder="输入房间号"/>
      <button class="button-join" v-if="!room_id"  @click="joinRoom()">
        加入房间
      </button>
    </div>
    <div>
      <button
      class="button-leave" 
      v-if="room_id" @click="leaveRoom()">
        离开房间
      </button>
      <button 
      class="button-create-game" 
      v-if="room_id && room_info.holder.userid == Cookies.get('userid')" 
      @click="createGame()">
        开始游戏
      </button>
    </div>
    <ElDivider/>
    <div class="room-info">
      <div v-if="room_info">
        <li v-for="user in room_info.users" class="user"> 
          <el-icon  style="vertical-align: middle" size="40px">
            <User />
          </el-icon>
          <span class="user-name" style="vertical-align: middle">{{ user.username }}</span>
        </li>
      </div>
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
}

.button-home:hover {
  background-color: #e0a61b;
}

.emphasis-text {
  color: #ecb920 ;
  font-weight: bold;
  border-radius: 10px;
  padding: 5px 10px;
  background-color:bisque;
}

.room-title {
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: bold;
  color: #ecb920;
  font-family:'Times New Roman', Times, serif
}

.button-create {
  background-color: #ecb920;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.button-create:hover {
  background-color: #e0a61b;
}

.create-room {
  margin-top: 20px;
  max-width: 200px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

.input-join {
  padding: 10px;
  border-radius: 5px;
  border: none;
  font-size: 18px;
  width: 100%;
  background-color: bisque;
}

.button-join {
  margin-top: 10px;
  background-color: #ecb920;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.button-join:hover {
  background-color: #e0a61b;
}

.join-room {
  margin-top: 20px;
  max-width: 400px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
}

.button-leave { 
  background-color: #f47710;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-right: 20px;
}

.button-leave:hover {
  background-color:#f8903b
}

.button-create-game {
  margin-top: 10px;
  background-color: #a7d413;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-left: 20px;
}

.button-create-game:hover {
  background-color: #bbe62d;
}

.room-info {
  margin-top: 20px;
  max-width: 400px;
  position: relative;
  left: 50%;
  transform: translateX(-50%);
  background-color:bisque;
  border-radius: 10px;
}

.user{
  margin: 20px;
  padding-top: 10px;
  padding-bottom: 10px;
  margin-right: 200px;
  color: #ecb920;
}

.user-name{
  margin-left: 20px;
  font-size: 18px;
  font-weight: bold;
}


/* 添加其他样式以美化页面 */
</style>
