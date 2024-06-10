<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { onMounted, ref, getCurrentInstance} from 'vue'
import { registerSockets, socket, registerSocketsForce, removeSockets } from '@/sockets'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router';
import { ElDivider, ElMessage } from 'element-plus'
import * as CONST from '@/lib/const.js'
import { HomeFilled } from '@element-plus/icons-vue'
import axios from 'axios'

const { proxy } = getCurrentInstance()
const router = useRouter()
const room_id = ref(null)
const new_room_id = ref(null)
const room_info = ref(null)

const joining = ref(false)
const rooms = ref([])
const room_password = ref('')

const sockets_methods = {
  watchGameSuccess(data){
    room_info.value = data.room_info
    room_id.value = data.room_info.room_id
    Cookies.set('room_info',JSON.stringify(data.room_info))
    Cookies.set('room_id',room_id.value)
    Cookies.set('game_info',JSON.stringify(data.game_info))
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
      //console.log(Cookies.get('camp'))
      ElMessage.success('你是'+(camp>0?(camp>1?'金方玩家':'黑方玩家'):(camp==0?'红方玩家':'观战者')))
    }
    removeSockets(sockets_methods, socket.value, proxy)
    router.replace('/game')
  },
  processWrong(data){
    switch(data.status){
      case CONST.PARAM_ERROR:
        ElMessage.error('参数错误')
        break
      case CONST.ROOM_NOT_EXIST:
        ElMessage.error('不存在此房间')
        getAllRooms()
        if(data.message){
          ElMessage.error(data.message)
        }
        break
      case CONST.NOT_JOIN_GAME:
        ElMessage.error('加入观战失败')
        break
      case CONST.ROOM_FULL:
        ElMessage.error('房间已满')
        getAllRooms()
        break
      case CONST.ROOM_PASSWORD_ERROR:
        ElMessage.error('房间密码错误')
        break
      case CONST.OTHER_ERROR:
        ElMessage.error('其他错误')
        break
      case CONST.SESSION_EXPIRED:
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
        ElMessage.error('未知错误')
    }
  },
}

onMounted(() => {
  establishConnection()
  if (Cookies.get('room_id') && Cookies.get('room_info')) {
    room_id.value = Cookies.get('room_id')
    room_info.value = JSON.parse(Cookies.get('room_info'))
  }
  getAllRooms()
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
function watchGame(room_id) {
  socket.value.io.emit('watchGame', { 'room_id': room_id, 'userid': Cookies.get('userid') })
  new_room_id.value = null
}

function watchGameBefore(room_id) {
  joining.value = true
  new_room_id.value = room_id
}

function watchGameByPassword(room_id, password) {
  socket.value.io.emit('watchGameByPassword', { 'room_id': room_id, 'password': password, 'userid': Cookies.get('userid') })
  new_room_id.value = null
}

function goBackHome(){
  removeSockets(sockets_methods, socket.value, proxy)
  Cookies.remove('room_id')
  Cookies.remove('room_info')
  socket.value.io.disconnect()
  socket.value = null
  router.push('/')
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
  
  <el-dialog v-model="joining"
  title="输入密码"
  width="400"
  :before-close="()=>{room_password='';joining=false}">
    <input v-model="room_password"
        class="info-text"
        placeholder="密码（6位数字）">
      </input>
      <div style="padding-top: 20px; text-align: right">
      <button class="button-create" @click="watchGameByPassword(new_room_id,room_password)">加入</button>
      </div>
  </el-dialog>

  <div class="container">
    <button class="button-home" @click="goBackHome()">
      <el-icon style="vertical-align: middle" size="30px">
        <HomeFilled />
      </el-icon>
    </button>
    <div class="all-rooms-table"> 
      <div>
        <button class="refresh-button" @click="getAllRooms()">刷新</button>
      </div>
      <div class="room-table-title">房间列表</div>
      <div>注：只有已经开始的房间模式可以观战</div>
      <div class="room-item-container">
          <div class="room-item"
          style="width: 300px!important;">
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
          style="width: 100px!important;">
            {{"房间状态"}}
          </div>
          <div class="room-item"
          style="width: 100px!important;">
            {{"房间按钮"}}
          </div>
        </div>
      <template v-for="room in rooms">
        <div class="room-item-container" v-if='room.started==1 && room.room_type==0'>
          <div class="room-item"
          style="width: 300px!important;">
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
          style="width: 100px!important;">
            {{room.locked!=1?'开放':'加密'}}
          </div>
          <div class='button-join'
          @click="room.locked!=1? watchGame(room.room_id):
          watchGameBefore(room.room_id)">
            观战
          </div>
        </div>
      </template>
    </div>
    <!-- <div class="join-room">
      <input
          class = "input-join"
          v-if="!room_id"
          v-model="new_room_id"
          placeholder="输入房间号"/>
      <button class="button-join" v-if="!room_id"  @click="watchGame()">
        加入房间
      </button>
    </div> -->
    <!-- <ElDivider/> -->
  </div>

</template>

<style>
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
