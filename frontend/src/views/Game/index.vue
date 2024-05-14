<script setup >
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import Cookies from 'js-cookie';
import { registerSockets, socket, registerSocketsForce,removeSockets} from '@/sockets'
import router from '@/router';
import {ElMessage} from "element-plus";

import { onMounted, ref ,onUnmounted,computed,getCurrentInstance,onBeforeUnmount} from 'vue';
import Board from '@/views/Game/board.vue'

const userid =  Cookies.get('userid')
let my_camp = Cookies.get('camp')
let status1 = ''
const {proxy} = getCurrentInstance()
const board = ref(null)
const dialogVisible = ref(false)
const winner_name = ref('')
const step_count = ref(0)

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
    dialogVisible.value = true;

    // 匹配模式退回主页面
    if(data.room_type == 0){
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

  },
  processWrong(data){
    status1 = data.status
    ElMessage.error("Error due to "+status1)
  },
}

const Move = (data) => {
  console.log(board.value)
  data.userid = userid
  socket.value.io.emit('movePiece',data)
}

</script>

<template>
  <div class="background-image"></div>
  <el-dialog
      title="游戏结束"
      :visible.sync="dialogVisible"
      width="30%"
      :close-on-click-modal="false"
  >
    <p>当前的胜者是：{{ winner_name }}</p>
    <p>当前的步数是：{{ step_count }}</p>
    <div slot="footer" class="dialog-footer">
      <el-button type="primary" @click="dialogVisible = false">关闭</el-button>
    </div>
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