<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { onMounted, ref, getCurrentInstance ,computed} from 'vue'
import { registerSockets, socket, registerSocketsForce, removeSockets } from '@/sockets'
import axios from 'axios'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router';
import { ElDivider, ElInput, ElMessage } from 'element-plus'
import * as CONST from '@/lib/const.js'
import { lives, resetLives } from '@/chesses/Live';
import { User, HomeFilled } from '@element-plus/icons-vue'

import Avatar from '@/components/views/Avatar.vue'
import Report from '@/components/views/Report.vue'

const { proxy } = getCurrentInstance()
const router = useRouter()
const room_id = ref(null)
const new_room_id = ref(null)
const room_info = ref(null)
const i_message = ref('')
const o_message = ref([])

const to_report_id= ref(0)
const vis = ref(false)

const avatars = ref({})
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
const my_name = computed(() => {
  if (room_info.value) {
    for (let user of room_info.value.users) {
      if (user.userid == Cookies.get('userid')) {
        return user.username
      }
    }
  }
  return ''
})
// const i_am_holder = computed(() => {
//   if (room_info.value) {
//     return room_info.value.holder.userid == Cookies.get('userid')
//   }
//   return false
// })  

const sockets_methods = {
  createRoomSuccess(data){
    Cookies.set('room_id',data.room_id)
    room_id.value = data.room_id
    room_info.value = data.room_info
    avatars.value[Cookies.get('userid')] = data.avatar
    ElMessage.success('创建房间成功')

  },
  joinRoomSuccess(data){
    if (data.userid == Cookies.get('userid')){
      Cookies.set('room_id',data.room_id)
      room_id.value = data.room_id
      room_info.value = data.room_info
      ElMessage.success('加入房间成功')
      avatars.value[data.userid] = data.avatar
      let userids = data.room_info.users.map(user => {
        return user.userid;
      })      
      axios.post(main.url + '/api/getAvatars', {'userids': userids.join(',')},
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      }
      )
      .then(res => {
        console.log(res.data)
        avatars.value = res.data
      })
      .catch(err => {
        console.error(err)
      })
    }
    else{
      room_info.value = data.room_info
      ElMessage.success('玩家'+data.username+'加入房间')
      avatars.value[data.userid] = data.avatar
    }
  },
  processWrong(data){
    switch(data.status){
      case CONST.ALREADY_IN_ROOM:
        ElMessage.error('已经在房间中')
        break
      case CONST.ROOM_NOT_EXIST:
        ElMessage.error('不存在此房间')
        Cookies.remove('room_id')
        Cookies.remove('room_info')
        room_id.value = null
        room_info.value = null
        break
      case CONST.NOT_IN_ROOM:
        ElMessage.error('不在房间中')
        Cookies.remove('room_id')
        Cookies.remove('room_info')
        room_id.value = null
        room_info.value = null
        break
      case CONST.ROOM_NOT_ENOUGH:
        ElMessage.error('房间人数不足')
        break
      case CONST.GAME_CREATE_FAILED:
        ElMessage.error('游戏创建失败:未知错误')
        break
      case CONST.ROOM_FULL:
        ElMessage.error('房间已满')
        break
      case CONST.USER_NOT_LOGIN:
        ElMessage.error('用户未登录')
        router.push('/login')
        break
      default:
        console.error(data.status)
        ElMessage.error('未知错误')
    }
  },
  leaveRoomSuccess(data){
    if (data.userid == -1){
      Cookies.remove('room_id')
      Cookies.remove('room_info')
      room_id.value = null
      room_info.value = null
      ElMessage.success('房主离开，房间解散！')
    }
    else if (data.userid == Cookies.get('userid')){
      Cookies.remove('room_id')
      Cookies.remove('room_info')
      room_id.value = null
      room_info.value = null
      ElMessage.success('离开房间成功')
      avatars.value = {}
    }
    else{
      ElMessage.success('玩家'+data.username+'离开房间')
      if (room_info.value.holder.userid != Cookies.get('userid') && data.room_info.holder.userid == Cookies.get('userid')) 
        ElMessage.success('房主离开房间，你是新的房主')
      room_info.value = data.room_info
      avatars.value[data.userid] = null
    }
  },
  rejoinGameSuccess(data){
    removeSockets(sockets_methods, socket.value, proxy)
    Cookies.set('room_id',data.room_id)
    router.replace('/game')
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
    resetLives()
    if (camp>=-1){
      Cookies.set('camp',camp)
      console.log(Cookies.get('camp'))
      ElMessage.success('游戏开始,你是'+(camp>0?(camp>1?'金方玩家':'黑方玩家'):(camp==0?'红方玩家':'观战者')))
    }
    removeSockets(sockets_methods, socket.value, proxy)
    router.replace('/game')
  },
  receiveMessage(data){
    if(data.username!=my_name.value)
      o_message.value.push({ 'user': data.username, 'message': data.message })
  },
}

onMounted(() => {
  establishConnection()
  let fromGame = sessionStorage.getItem('fromGame')
  if (fromGame == 'true') {
    room_id.value = Cookies.get('room_id')
    room_info.value = JSON.parse(Cookies.get('room_info'))
    let userids = room_info.value.users.map(user => {
      return user.userid;
    })      
    axios.post(main.url + '/api/getAvatars', {'userids': userids.join(',')},
    {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    )
    .then(res => {
      console.log(res.data)
      avatars.value = res.data
    })
    .catch(err => {
      console.error(err)
    })
  }
  else{
    Cookies.remove('room_id')
    Cookies.remove('room_info')
  }
  sessionStorage.removeItem('fromGame')
})

function establishConnection() {
  if (!socket.value) {
    socket.value = new VueSocketIO({
      debug: true,
      connection: SocketIO(main.url),
    })
  }
  registerSocketsForce(sockets_methods, socket.value, proxy)
  console.log(socket.value)
}
function createRoom() {
  socket.value.io.emit('createRoom', { 'userid': Cookies.get('userid') })
}
function joinRoom() {
  if (!new_room_id.value) {
    ElMessage.error('请输入房间号')
    return
  }
  socket.value.io.emit('joinRoom', { 'room_id': new_room_id.value, 'userid': Cookies.get('userid') })
  new_room_id.value = null
}
function leaveRoom() {
  socket.value.io.emit('leaveRoom', { 'room_id': Cookies.get('room_id'), 'userid': Cookies.get('userid') })
  i_message.value = ''
  o_message.value = []

}
function createGame() {
  axios.post(main.url + '/api/game/create',
    { 'room_id': room_id.value, 'userid': Cookies.get('userid') },
    {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
}
function goBackHome(){
  // if (Cookies.get('room_id')){
  //   leaveRoom()
  // }
  // 不知道到底需不需要离开房间
  removeSockets(sockets_methods, socket.value, proxy)
  Cookies.remove('room_id')
  Cookies.remove('room_info')
  socket.value.io.disconnect()
  socket.value = null
  router.push('/')
}

const copyRoomId = () => {
  if (room_info.value && room_info.value.room_id) {
    const textarea = document.createElement('textarea');
    textarea.value = room_info.value.room_id;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    ElMessage.success('已复制房间号')
  } else {
    console.error('room_info 或 room_info.room_id 未定义');
  }
}

const sendMessage = () => {
  if (i_message.value) {
    socket.value.io.emit('sendMessage', { 'room_id': room_id.value, 'userid': Cookies.get('userid'), 'message': i_message.value })
    o_message.value.push({ 'user': my_name.value, 'message': i_message.value })
    i_message.value = ''
  }
}
const handleReportEnd = () => {
  vis.value = false;
}
const handleReport = (id) => {
  to_report_id.value = id;
  vis.value = true;
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
        <button class = "copy-button" 
        @click="copyRoomId">复制</button>
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
      placeholder="输入房间号"
      />
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
    <div class="in-room">
      <div class="room-info">
        <div v-if="room_info" class="room-tag">
          参战者
        </div>
        <div v-if="room_info">
          <li v-for="user in room_info.users" class="user" @mouseover="get_info">
            <Avatar :my_userid="Cookies.get('userid')" :userid=user.userid @reportUser="handleReport" class="avas">
              <template #name>
                <p>{{user.username}}</p>
              </template>
              <template #avatar>
                <img :src="main.url+avatars[user.userid]" alt="头像" />
              </template>
            </Avatar>
            <span class="user-name" style="vertical-align: middle">{{ user.username }}</span>
          </li>
        </div>
      </div>

      <div class="message" v-if="room_id">

        <div class="message-show">
          <li v-for="(item, index) in o_message">
            {{item.user}} - {{ item.message }}
          </li>
        </div>
        <el-input class="custom-input" v-model="i_message" maxlength=80 show-word-limit placeholder="Please input" />
        <el-button @click="sendMessage" style="width:60px" type="primary">发送消息</el-button>
      </div>
      <div class="room-info">
        <div v-if="room_info" class="room-tag" >
          观战者
        </div>
        <div v-if="room_info">
          <li v-for="viewer in room_info.viewers" class="user" @mouseover="get_info">
            <Avatar :my_userid="Cookies.get('userid')" :userid=viewer.userid @reportUser="handleReport" class="avas">
              <template #name>
                <p>{{viewer.username}}</p>
              </template>
              <template #avatar>
                <User/>
              </template>
            </Avatar>
            <span class="user-name" style="vertical-align: middle">{{ viewer.username }}</span>
          </li>
        </div>
      </div>
    </div>
  </div>
  <Report :toreportid=to_report_id :myuserid="Cookies.get('userid')" :dialogFormVisible=vis @reportEnd="handleReportEnd" />
</template>


<style>
.litter{
  min-width: 50px;
  max-width: 50px;
  font-size: 10px;
  color: #4d4533;
  background-color: #f2d683;
}
.custom-input{
  max-width: 90%;
  padding-right: 3%;
}
  .custom-input .el-input__inner{
    background-color: beige !important; /* 背景色 */
    border-color: #dcdfe6; /* 边框色 */
    color: #606266; /* 文本颜色 */
  }
  .message .el-button{
    color: white;
    background-color: #ecb920;
  }
  .message .el-button:hover{
    background-color: #ffe7b0;
  }
  .custom-input .el-input__inner:focus {
    border-color: #569eee; /* 聚焦时边框色 */
  }
  .custom-input .el-input__wrapper{
    width: 240px;
    background-color: beige;
  }
  .custom-input .el-input__count-inner{
    background-color:  beige !important;
  }

.in-room{
  display: flex;
}
.message{
  margin-left: 20px;
  margin-right: 20px;
  width: 60%;

}
.message-show{
  margin-top: 20px;
  background-color: bisque;  
  margin-bottom: 20px;
  overflow-y: auto;
  border-radius: 10px;
  height:300px;
  text-align:left;
}
.message-show li{
  margin: 10px;
  font-size: 18px;
  color: darkgrey;
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

.container {
  margin-top: 60px !important;
  border-radius: 10px;
  padding: 30px !important;
}

.copy-button{
  background-color: #ecb920;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  position: relative;
  bottom: 4px;
}

.copy-button:hover{
  background-color: #e0a61b;
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
.avas{
  min-width: 400px;
}
.button-create-game:hover {
  background-color: #bbe62d;
}

.room-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
  margin-left: 20px;
  margin-right: 20px;
  display: flex;
  max-width: 30%;
  background-color:bisque;
  border-radius: 10px;
}

.room-tag{
  font-size: 24px;
  font-weight: bold;
  color: #ecb920;
  font-family:'Times New Roman', Times, serif;
  margin-top: 20px;
  margin-left: 20px;
  margin-right: 20px;
  display: flex;
  max-width: 30%;
  background-color:bisque;
  border-radius: 10px;
}


.user{
  margin: 20px;
  padding-top: 10px;
  padding-bottom: 10px;
  margin-right: 200px;
  height: 60px;
  display: flex;
  color: #ecb920;
}

.user .user-show{
    display: none;
    height: 100px;
    color: #fff;
    background: #ecb920;
    line-height: 40px;
    cursor: pointer;
    opacity: 0.8;
    border-radius: 10px;
    transform: translate(-100px);
}
.user:hover .user-show{
  position: fixed;
  display:flex;
}
.user-name{
  margin-left: 20px;
  font-size: 18px;
  font-weight: bold;
  max-width: 40%;
  overflow: hidden;
}


/* 添加其他样式以美化页面 */
</style>
