<script setup >
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import Cookies from 'js-cookie';
import { registerSockets, socket, registerSocketsForce} from '@/sockets'
import router from '@/router';
import {ElMessage} from "element-plus";

import { onMounted, ref ,onUnmounted,computed,getCurrentInstance,onBeforeUnmount} from 'vue';
import Board from '@/views/Game/board.vue'

const userid =  Cookies.get('userid')
let my_camp = Cookies.get('camp')
let status1 = ''
const {proxy} = getCurrentInstance()
const board = ref(null)


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
  console.log(board.value)
  registerSocketsForce(sockets_methods,socket.value,proxy);

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
    console.log(board.value)
    board.value.movePieceSuccess(data);
  },
  gameEnd(data){
    ElMessage.info('游戏结束'+"获胜者为"+data.winner_name)
    Cookies.remove('game_id')
    Cookies.remove('camp')
    router.replace('/room')
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
  <Board :my_camp="my_camp"  ref="board" @requireMove="Move"/>
</template>


<style scoped lang="scss">

</style>