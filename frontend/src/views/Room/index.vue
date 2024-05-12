<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { onMounted,ref,getCurrentInstance } from 'vue'
import { registerSockets, socket } from '@/sockets'
import axios from 'axios'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'
import * as CONST from '@/lib/const.js'
import Board from '@/views/Game/board.vue';



const {proxy} = getCurrentInstance()
const router = useRouter()
const msg = ref('')
const receive = ref('')
const room_id = ref('')
const new_room_id = ref('')   // 加入房间时临时使用的room_id
const userid = ref(Cookies.get('userid'))
const camp = ref(-1) 
const y2 = ref(0)


const sockets_methods={
  createRoomSuccess(data){
    Cookies.set('room_id',data.room_id)
    room_id.value = data.room_id
    ElMessage.success('创建房间成功')
  },
  joinRoomSuccess(data){
    if (data.userid == userid.value){
      Cookies.set('room_id',data.room_id)
      room_id.value = data.room_id
      ElMessage.success('加入房间成功')
    }
    else{
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
    if (data.userid == userid.value){
      Cookies.set('room_id',null)
      room_id.value = null
    }
  },
  createGameSuccess(data){
    console.log(data)
    ElMessage.info('创建成功')
    camp.value = -1
    for (let i = 0; i < data.users.length; i++){
      Cookies.set('user'+i,data.users[i])
      if (data.users[i] == userid.value){
        camp.value = i
      }
    }
    if (camp.value>=-1){
      Cookies.set('camp',camp.value)
      console.log(Cookies.get('camp'))
      ElMessage.success('游戏开始,你是'+camp.value>0?(camp.value>1?'金方玩家':'黑方玩家'):camp.value==0?'红方玩家':'观战者')
    }
    router.replace('/game')
  },

}


onMounted(() => {
  establishConnection()
  if (Cookies.get('room_id')){
    room_id.value = Cookies.get('room_id')
  }
  // 注册socket监听
  registerSockets(sockets_methods,socket.value,proxy)
})

function establishConnection(){
  if (!socket.value){
    socket.value = new VueSocketIO({
      debug: true,
      connection: SocketIO(main.url),
    })
  }
  socket.value.io.on('disconnect',()=>{
    socket.value = null
  })
}
function createRoom(){
  socket.value.io.emit('createRoom',{'userid':userid.value})
}
function joinRoom(){
  // alert(new_room_id.value)
  // alert(userid.value)
  socket.value.io.emit('joinRoom',{'room_id':new_room_id.value,'userid':userid.value})
}

function leaveRoom(){
  socket.value.io.emit('leaveRoom',{'room_id':Cookies.get('room_id'),'userid':userid.value})
}
function createGame(){
  axios.post(main.url+'/api/game/create',
  {'room_id':room_id.value,
    'userid':userid.value},
  {
      headers: {'Content-Type':'application/x-www-form-urlencoded'},
  })
}

</script>

<template>
  <div>
    <h1>Hello World</h1>
  </div>
  <div>
    <span>你的用户id：{{userid}}</span>
  </div>
  <div>
    当前房间{{room_id}}
  </div>
  <el-button type="primary" @click="createRoom">创建房间</el-button>
  <div>
    <el-input v-model="new_room_id"></el-input>
  </div>
  <el-button type="primary" @click="joinRoom">加入房间</el-button>
  <div>
    <el-button type="primary" @click="leaveRoom">离开房间</el-button>
  </div >
  <div>
    <el-button type="primary" @click="createGame">创建游戏</el-button>
  </div >

</template>