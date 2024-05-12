<script setup >


import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { camps } from '@/lib/game';
import { GEBI } from '@/utils/utils';
import Cookies from 'js-cookie';
import { registerSockets, socket} from '@/sockets'
import {XYZToPosition, PositionToXYZ} from '@/lib/convert'
import router from '@/router';
import {ElMessage} from "element-plus";
import { lives } from '@/chesses/Live';
import { onMounted, ref ,onUnmounted,computed,getCurrentInstance} from 'vue';
import {COL, ROWTOP, ROWMID, AREABOT, ROWBOT} from '@/config/config';



const map = new Map();
const getid = (row, col) => (ROWTOP - row - 1) * COL + col + 1;
const camp = ref(0);

const userid =  Cookies.get('userid')
const my_camp = Cookies.get('camp')
let hoverChess;
const isPocus = ref(false);
const focusChess = ref();
const hoverposition = ref();
const hover_xyz = ref([0,0,0])
const xyz = ref([0,0,0])
const xyzn = ref([0,0,0])
const my_camp_str = ['红方','黑方','金方']

const move_succ = ref(false)
const {proxy} = getCurrentInstance()
const sockets_methods={
  movePieceSuccess(data){
    move_succ.value = true
    if(userid == data.userid){
      ElMessage.info('移动成功')
    }
    else {
      ElMessage.info('玩家'+data.username+'移动成功')
    }
    // 移动棋子
    board.value.movePieceSuccess(data);

    // 切换到下一个阵营
    camp.value = (camp.value + 1)%3;
    while(lives[camp.value]==false){
      camp.value = (camp.value + 1)%3;
    }
  },
  gameEnd(data){
    ElMessage.info('游戏结束'+"获胜者为"+data.winner_name)
    Cookies.remove('game_id')
    Cookies.remove('camp')
    router.replace('/room')
  },
  processWrong(data){
    status = data.status
    ElMessage.info(status)
  }
}

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
  registerSockets(sockets_methods,socket.value,proxy);
  board.value.initMap(); // 初始化棋盘

});
onUnmounted(Destory);
const board = ref(null)
const Move = (data) => {
  my_camp.value = (my_camp.value+1)%3
  board.value.movePieceSuccess(data)
}

</script>

<template>
  <Board :my_camp=my_camp ref="board" @requireMove="Move"/>
</template>


<style scoped lang="scss">

</style>