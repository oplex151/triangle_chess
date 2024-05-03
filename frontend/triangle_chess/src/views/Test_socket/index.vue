<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
// 先导入包npm install vue-socket.io --save
import { onMounted,ref,getCurrentInstance } from 'vue'
import { registerSockets, socket } from '@/sockets'
import axios from 'axios'
import Game from '@/views/Game/index.vue'
const {proxy} = getCurrentInstance()

const msg = ref('')
const receive = ref('')
const room_id = ref('')
const userid = ref(1)

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
    alert('创建成功')
  },
  movePieceSuccess(data){
    if(userid.value == data.userid){
      alert('移动成功')
    }

    console.log(data)
  }

}
// emit('movePieceSuccess',{'userid':userid,'status':status, 
//                                      'x1':x1, 'y1':y1, 'z1':z1, 
//                                      'x2':x2, 'y2':y2, 'z2':z2},
//                                      
onMounted(() => {
  alert('连接成功')
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
  ).then(res=>{
    console.log(res)
  })
}
</script>

<template>
  <div>
    <h1>Hello World</h1>
  </div>
  <div>
    <el-input v-model="userid"></el-input>
    <span>设置用户id</span>
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
  <Game></Game> 
</template>