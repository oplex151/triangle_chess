<script setup >
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import Cookies from 'js-cookie';
import { registerSockets, socket, registerSocketsForce,removeSockets} from '@/sockets'
import router from '@/router';
import {ElMessage} from "element-plus";

import { onMounted, ref ,onUnmounted,computed,getCurrentInstance,onBeforeUnmount, watch} from 'vue';
import Board from '@/views/Game/board.vue'
import axios from 'axios';
const userid =  Cookies.get('userid')
let my_camp = Cookies.get('camp')
let status1 = ''
const {proxy} = getCurrentInstance()
const board = ref(null)
const dialogVisible = ref(false)
const winner_name = ref('')
const step_count = ref(0)
const room_type = ref(0)
onMounted(()=>{
  if (!Cookies.get('camp')){
    router.replace('/room')
    return
  }
  if (!socket.value){
    socket.value = new VueSocketIO({
      debug: true,
      connection: SocketIO(main.url),
    })
    // 重新加入房间
    socket.value.io.emit('joinRoom',{'userid':userid,'room_id':Cookies.get('room_id')})
  }
  registerSocketsForce(sockets_methods,socket.value,proxy);
  axios.post(main.url + '/api/game/init',{
        'room_id': Cookies.get('room_id')
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }
    ).then(res => {
        if(res.status==200){
          console.log(res.data)
          board.value.initMap(res.data.game_info)
        }
        else{
            ElMessage.error('获取房间信息失败')
            return
        }
    }).catch(error => {
        console.log(error)
    })
  console.log(socket.value)
});

const sockets_methods={
  movePieceSuccess(data){
    if(userid == data.userid){
      ElMessage.info('移动成功')
    }
    else {
      ElMessage.info('玩家'+data.username+'移动成功')
    }
    // 移动棋子_切换阵营
    board.value.moveSuccess(data);
  },
  joinRoomSuccess(data){
    if (data.userid == Cookies.get('userid')){
      Cookies.set('room_id',data.room_id)
      ElMessage.success('加入房间成功')
    }
    else{
      ElMessage.success('玩家'+data.username+'加入房间')
    }
  },
  leaveRoomSuccess(data){
    if (data.userid == Cookies.get('userid')){
      Cookies.remove('room_id')
      Cookies.remove('room_info')
      ElMessage.success('离开房间成功')
    }
    else{
      ElMessage.success('玩家'+data.username+'离开房间')
    }
  },
  gameEnd(data){
    ElMessage.info('游戏结束'+"获胜者为"+data.winner_name)
    // 模态框位置(待加入)
    step_count.value = data.step_count;
    winner_name.value = data.winner_name;
    room_type.value = data.room_type;
    dialogVisible.value = true;
    // 匹配模式退回主页面
  },
  processWrong(data){
    status1 = data.status
    ElMessage.error("Error due to "+status1)
  },
}

const EndGame = () => {
  dialogVisible.value = false
  if(room_type.value == 0){
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods,socket.value,proxy);
      router.replace('/')
    }
    // 创房间模式
    else {
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods,socket.value,proxy);
      router.replace('/room')
    }
}

const Move = (data) => {
  data.userid = userid
  socket.value.io.emit('movePiece',data) 
}
</script>

<template>
  <div class="background-image"></div>


  <el-button plain @click="dialogVisible = true">
    Click to open the Dialog
  </el-button>
  <el-dialog
      title="游戏结束"
      v-model="dialogVisible"
      width="30%"
      :before-close="EndGame"
  >
    <p>获胜者为{{winner_name}}</p>
    <p>步数为{{step_count}}</p>
    <template #footer>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="EndGame">关闭</el-button>
    </div>
    </template>
  </el-dialog>
  <Board :my_camp="my_camp"  ref="board" @requireMove="Move"/>
</template>


<style scoped lang="scss">
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

</style>