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
import { resetLives } from '@/chesses/Live';
import { User, HomeFilled } from '@element-plus/icons-vue'

import Avatar from '@/components/views/Avatar.vue'
import Report from '@/components/views/Report.vue'

const TIME_INTERVAL = 40

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

const creating = ref(false)
const joining = ref(false)
const rooms = ref([])
const locked = ref(0)
const room_password = ref('')
const time_interval = ref(TIME_INTERVAL)

const ready_status = computed(() => {
  if (room_info.value) {
    try{
      let user_ready = room_info.value.readys[Cookies.get('userid')]
      if (user_ready)
        return true
      else
        return false
    }
    catch(e){
      return false
    }
  }
  return false
})

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

const getUserReadyStatus = (userid) => {
  if (room_info.value) {
    try{
      let user_ready = room_info.value.readys[userid]
      if (user_ready)
        return true
      else
        return false
    }
    catch(e){
      return false
    }
  }
  return false
}

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
        avatars.value = res.data
      })
      .catch(err => {
        //console.error(err)
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
        getAllRooms()
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
      case CONST.NOT_ALL_READY:
        ElMessage.error('还有玩家未准备')
        break
      case CONST.GAME_CREATE_FAILED:
        ElMessage.error('游戏创建失败:未知错误')
        break
      case CONST.ROOM_FULL:
        ElMessage.error('房间已满')
        getAllRooms()
        break
      case CONST.USER_NOT_LOGIN:
        ElMessage.error('用户未登录')
        router.push('/login')
        break
      case CONST.ROOM_PASSWORD_ERROR:
        ElMessage.error('房间密码错误')
        getAllRooms()
        break
      case CONST.GAME_ALREADY_START:
        ElMessage.error('游戏已经开始，请前往观战入口进入观战')
        break
      case CONST.SESSION_EXPIRED: //Session expired
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
        break;
      default:
        //console.error(data.status)
        ElMessage.error('未知错误')
        getAllRooms()
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
  userRemovedSuccess(data){
    // if (data.userid == -1){
    //   Cookies.remove('room_id')
    //   Cookies.remove('room_info')
    //   room_id.value = null
    //   room_info.value = null
    //   ElMessage.success('房主离开，房间解散！')
    // }
    // else 
    if (data.userid == Cookies.get('userid')){
      Cookies.remove('room_id')
      Cookies.remove('room_info')
      room_id.value = null
      room_info.value = null
      ElMessage.success('你已被请离房间')
      avatars.value = {}
      getAllRooms()
    }
    else{
      if(room_info.value.holder.userid == Cookies.get('userid')) 
        ElMessage.success('玩家'+data.username+'被你移除房间')
      else
        ElMessage.success('玩家'+data.username+'被房主移除房间')
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
      //console.log(Cookies.get('camp'))
      ElMessage.success('游戏开始,你是'+(camp>0?(camp>1?'金方玩家':'黑方玩家'):(camp==0?'红方玩家':'观战者')))
    }
    removeSockets(sockets_methods, socket.value, proxy)
    router.replace('/game')
  },
  receiveMessage(data){
    if(data.username!=my_name.value)
      o_message.value.push({ 'user': data.username, 'message': data.message })
  },
  changeReadyStatusSuccess(data){
    room_info.value = data.room_info
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
      //console.log(res.data)
      avatars.value = res.data
    })
    .catch(err => {
      //console.error(err)
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
    })
  }
  else{
    Cookies.remove('room_id')
    Cookies.remove('room_info')
    getAllRooms()
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
  //console.log(socket.value)
}
function createRoom() {
  if (locked.value=='1' && !room_password.value) {
    ElMessage.error('请输入房间密码')
    return
  }
  else if (locked.value=='1' &&
  room_password.value && 
  (room_password.value.length != 6
  || !/^[0-9]{6}$/.test(room_password.value))){
    ElMessage.error('房间密码为6位数字')
    return
  }
  if (time_interval.value < 30 || time_interval.value > 120) {
    ElMessage.error('最大思考时间为30-120秒')
    return
  }
  creating.value = false
  socket.value.io.emit('createRoom', { 'userid': Cookies.get('userid'),
                                    'password': room_password.value , 
                                    'locked': locked.value,
                                    'time_interval': time_interval.value })
}

function joinRoomBefore(room_id) {
  room_password.value = ''
  new_room_id.value = room_id
  joining.value = true
}


function joinRoomByPassword(room_id,password) {
  socket.value.io.emit('joinRoom', { 'room_id': room_id, 'userid': Cookies.get('userid') ,'password': password })
  joining.value = false
  new_room_id.value = null
}

function joinRoom(room_id) {
  socket.value.io.emit('joinRoom', { 'room_id': room_id, 'userid': Cookies.get('userid') })
  new_room_id.value = null
}
function leaveRoom() {
  socket.value.io.emit('leaveRoom', { 'room_id': Cookies.get('room_id'), 'userid': Cookies.get('userid') })
  i_message.value = ''
  o_message.value = []

}

function createRoomBefore(){
  room_password.value = ''
  locked.value = false
  creating.value = true
}

function createGame() {
  axios.post(main.url + '/api/game/create',
    { 'room_id': room_id.value, 'userid': Cookies.get('userid') },
    {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).catch(error => {
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

function changeReadyStatus(){
  socket.value.io.emit('changeReadyStatus', { 'room_id': room_id.value, 'userid': Cookies.get('userid') })
}


function goBackHome(){
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
    //console.error('room_info 或 room_info.room_id 未定义');
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

const canremove = (id) =>{
  if (room_info.value && room_info.value.holder.userid == Cookies.get('userid') && id != Cookies.get('userid'))
    return true
  return false
}

const removeUser = (id) => {
  if(Cookies.get('userid')!= room_info.value.holder.userid)
  {
    ElMessage.error('只有房主可以移除玩家')
    return
  }  
  socket.value.io.emit('removeUserFromRoom', { 'room_id': room_id.value, 'userid': Cookies.get('userid'), 'target_userid': id })
}

function getAllRooms() {
  axios.post(main.url + '/api/getAllRooms',{
    'userid': Cookies.get('userid')  //后端确认用
  },
  {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, 
  }).then(res => {
    if (res.status==200){
      //console.log(res.data.rooms)
      rooms.value = res.data.rooms
    }
    else{
      rooms.value = []
    }
  }).catch(error => {
    if (error.response.status == CONST.SESSION_EXPIRED){
      Cookies.remove('room_id')
      Cookies.remove('userid')
      Cookies.remove('room_info')
      Cookies.remove('username')
      Cookies.remove('camp')
      ElMessage({
        message: '会话过期，请重新登录!!!',
        grouping: true,
        type: 'error',
        showClose: true
      })
      router.replace('/login')
    }
    rooms.value = []
  })
}

</script>

<template>
  <div class="background-image">  </div>

  <el-dialog v-model="creating"
  title="房间设置"
  width="400"
  :before-close="()=>{locked=0;room_password='';time_interval=TIME_INTERVAL;creating=false}">
    <div class="create-room-cfg">
      <div style="padding-bottom: 10px; text-align: left;">
      设置最大思考时间（30秒-120秒）
      <input type="number" v-model="time_interval"
        class="info-text"
        placeholder="设置最大思考时间（秒）">
      </input>
      </div>
      <el-radio-group v-model="locked"
        class="info-text">
          <el-radio value='1' size="large">上锁</el-radio>
          <el-radio value='0' size="large">不上锁</el-radio>
      </el-radio-group>
      <div
      style="height: 10px;"
      ></div>
      <input type="text" v-model="room_password" v-if="locked==1"
        class="info-text"
        placeholder="密码（6位数字）">
      </input>
      <div style="padding-top: 20px; text-align: right">
      <button class="button-create" @click="createRoom()">创建</button>
      </div>
    </div>
  </el-dialog>>

  <el-dialog v-model="joining"
  title="输入密码"
  width="400"
  :before-close="()=>{room_password='';joining=false}">
    <input v-model="room_password"
        class="info-text"
        placeholder="密码（6位数字）">
      </input>
      <div style="padding-top: 20px; text-align: right">
      <button class="button-create" @click="joinRoomByPassword(new_room_id,room_password)">加入</button>
      </div>
  </el-dialog>

  <div class="container">
    <button class="button-home" @click="goBackHome()">
      <el-icon style="vertical-align: middle" size="30px">
        <HomeFilled />
      </el-icon>
    </button>
    <div v-if="room_id">
      <div class="room-title">
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
    </div>

    <div v-if="!room_id">
      <div class="create-room">
        <button class="button-create"
        @click="createRoomBefore()">
        创建房间
        </button>
      </div>

      <div class="all-rooms-table"> 
        <div>
          <button class="refresh-button" @click="getAllRooms()">刷新</button>
        </div>
        <div class="room-table-title">房间列表</div>
        <div class="room-item-container">
            <div class="room-item"
            style="width: 290px!important;">
              {{"房间id"}}
            </div>
            <div class="room-item"
            style="width: 100px!important;">
              {{"房主"}}
            </div>
            <div class="room-item"
            style="width: 100px!important;">
              {{"房间人数"}}
            </div>
            <div class="room-item"
            style="width: 150px!important;">
              {{"房间状态"}}
            </div>
            <div class="room-item"
            style="width: 100px!important;">
              {{"房间按钮"}}
            </div>
          </div>
        <template v-for="room in rooms">
          <div class="room-item-container">
            <div class="room-item"
            style="width: 290px!important;">
              {{room.room_id}}
            </div>
            <div class="room-item"
            style="width: 100px!important;">
              {{room.holder.username}}
            </div>
            <div class="room-item"
            style="width: 100px!important;">
              {{room.user_num+'/3'}}
            </div>
            <div class="room-item"
            style="width: 150px!important;">
              {{(room.locked!=1?'开放':'加密')+'| '+(room.started?'已开始':'未开始')}}
            </div>
            <div class='button-join'
            @click="room.locked!=1? joinRoom(room.room_id):
            joinRoomBefore(room.room_id)">
              加入房间
            </div>
          </div>
        </template>
      </div>

      <!-- <div class="join-room">
        <input 
        class = "input-join"
        v-model="new_room_id" 
        placeholder="输入房间号"
        />
        <button class="button-join"  @click="joinRoom()">
          加入房间
        </button>
      </div> -->
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
      <button v-else-if="room_id" @click="changeReadyStatus()"
      :class="ready_status?'button-cancel':'button-create-game'">
        {{ready_status?'取消准备':'准备'}}
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
              <template #custom>
                <button v-if="canremove(user.userid)" class="remove-user-button" @click="removeUser(user.userid)">移除</button>
              </template>
            </Avatar>
            <span :class="getUserReadyStatus(user.userid)?'ready-user-name':'user-name'" style="vertical-align: middle">{{ user.username }}</span>
          
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
        <el-button @click="sendMessage" style="width:60px;border-radius:5px; margin-top: 10px;" type="primary">发送消息</el-button>
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

.remove-user-button {
    justify-content: center;
    background-color: #f6bb4e;
    color: #fff;
    border: none;
    border-radius: 15px;
    /* 增加垂直内边距 */
    margin: auto;
    cursor: pointer;
    font-size: 15px;
    margin: 5px;
    width: 70px;
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
  background-color: #ecb920;
  color: white;
  border: none;
  padding: 10px;
  border-radius: 5px;
  font-size: 16px;
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
  width:112px;
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
  width:112px;
}

.button-create-game:hover {
  background-color: #bbe62d;
}

.button-cancel {
  margin-top: 10px;
  background-color: #f47710;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  margin-left: 20px;
  width:112px;
}

.button-cancel:hover {
  background-color:#f8903b
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
  position: relative;
  margin: 20px;
  padding-top: 10px;
  padding-bottom: 10px;
  height: 60px;
  display:flex;
  color: #ecb920;
  text-align: left;
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

.ready-user-name{
  color: #a7d413;
  margin-left: 20px;
  font-size: 18px;
  font-weight: bold;
  max-width: 40%;
  overflow: hidden;
}

/* 添加其他样式以美化页面 */

.all-rooms-table{
  margin-top: 20px;
  max-width: 900px;
  position: relative;
  left: 50%; 
  transform: translateX(-50%);
  background-color: bisque;
  border-radius: 10px;
  padding: 10px 10px;
  height: 500px;
  overflow-y: auto;
}

.refresh-button{
  background-color: #ecb920;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  position: absolute;
  right: 10px;
}

.refresh-button:hover{
  transform: scale(1.05);
  background-color: #e0a61b;
}

.create-room-cfg{
  margin-top: 20px;
  max-width: 300px;
  padding: 20px;
  text-align: center;
  display: block;
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

.room-table-title{
  font-size: 24px;
  font-weight: bold;
  color: #ecb920;
  font-family:'Times New Roman', Times, serif;  
  margin-bottom: 20px;

}

.room-item-container{
  display: inline-flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding: 10px;
}

.room-item{
  margin-top: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #101010;
  font-family:'Times New Roman', Times, serif;
  background-color: rgb(253, 242, 229);
  padding: 10px;
  border-radius: 5px;
}
</style>
