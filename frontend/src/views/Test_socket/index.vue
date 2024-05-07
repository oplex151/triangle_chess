<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
// 先导入包npm install vue-socket.io --save
import { onMounted,ref,getCurrentInstance } from 'vue'
import { registerSockets, socket } from '@/sockets'
import axios from 'axios'
import Game from '@/views/Game/index.vue'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus'
const {proxy} = getCurrentInstance()
const router = useRouter()
const msg = ref('')
const receive = ref('')
const room_id = ref('')
const userid = ref(Cookies.get('userid'))
const camp = ref(-1) 
const y2 = ref(0)
// 建立连接

const sockets_methods={
  createRoomSuccess(data){
    room_id.value = data.room_id
    console.log(data)
  },
  joinRoomSuccess(data){
    console.log(data)
  },
  processWrong(data){
    console.log(data)
  },
  receiveMessage(data){
    console.log(data)
    ElMessage.info('收到消息')
    receive.value = data.message
  },
  leaveRoomSuccess(data){
    console.log(data)
    if (data.userid == userid.value){
      room_id.value = ''
    }
  },
  createGameSuccess(data){
    console.log(data)
    ElMessage.info('创建成功')
    for (let i = 0; i < data.users.length; i++){
      Cookies.set('user'+i,data.users[i])
      if (data.users[i] == userid.value){
        camp.value = i
      }
    }
    if (camp.value>=0){
      Cookies.set('camp',camp.value)
      console.log(Cookies.get('camp'))
      ElMessage.success('游戏开始,你是'+(Cookies.get('camp'))+'号玩家')
    }
    router.replace('/game')
  },
  // movePieceSuccess(data){
  //   if(userid.value == data.userid){
  //     ElMessage.info('移动成功')
  //   }
  //   else {
  //     ElMessage.info(data.userid+'移动成功')
  //   }
  // },
  message(data){
    ElMessage.info(data)
  },
  processWrong(data){
    status = data.status
    ElMessage.info(status)
  }

}
// emit('movePieceSuccess',{'userid':userid,'status':status, 
//                                      'x1':x1, 'y1':y1, 'z1':z1, 
//                                      'x2':x2, 'y2':y2, 'z2':z2},
//                                      
onMounted(() => {
  ElMessage.info('连接成功')
  establishConnection()
  // 注册socket监听
  registerSockets(sockets_methods,socket.value,proxy)
})

function establishConnection(){
  socket.value = new VueSocketIO({
    debug: true,
    connection: SocketIO(main.url),
  })
  
}
function createRoom(){
  socket.value.io.emit('createRoom',{'userid':userid.value})
}
function joinRoom(){
  socket.value.io.emit('joinRoom',{'room_id':room_id.value,'userid':userid.value})
}
function sendMessage(){
  ElMessage.info('发送')
  socket.value.io.emit('sendMessage',{'room_id':room_id.value,'userid':userid.value,'message':msg.value})
}
function leaveRoom(){
  socket.value.io.emit('leaveRoom',{'room_id':room_id.value,'userid':userid.value})
}
function createGame(){
  axios.post(main.url+'/api/game/create',
  {'room_id':room_id.value,
    'userid':userid.value},
  {
      headers: {'Content-Type':'application/x-www-form-urlencoded'},
  }
  )
}

function movePiece(){

  if (y2.value != 0){
    y2.value = 0
  }
  else{
    y2.value = 1
  }
  // ElMessage.info("走你！")
  // socket.value.io.emit('movePiece',{'userid':userid.value,'chess_type':1, 
  //                                 'x1':0, 'y1':0, 'z1':camp.value, 
  //                                 'x2':0, 'y2':y2.value, 'z2':camp.value})

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
    <el-input v-model="room_id"></el-input>
  </div>
  <el-button type="primary" @click="joinRoom">加入房间</el-button>
  <div>
    <el-button type="primary" @click="leaveRoom">离开房间</el-button>
  </div >
  <div>
    <el-input v-model="msg"></el-input>
  </div>
  <el-button type="primary" @click="sendMessage">Send Message</el-button>
  <div>{{receive}}</div>
  <div>
    <el-button type="primary" @click="createGame">创建游戏</el-button>
  </div >
  <div>
    <el-button type="primary" @click="movePiece">你尝试走了一下！</el-button>
  </div>
</template>