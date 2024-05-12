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
import {Chariot} from "@/chesses/Chariot.js";
import {AREABOT, AREAMID, AREATOP, COL} from "@/config/config.js";
import {Warhosre} from "@/chesses/Warhosre.js";
import {Gun} from "@/chesses/Gun.js";
import {Soilder} from "@/chesses/Soilder.js";
import {Bishop} from "@/chesses/Bishop.js";
import {Advisor} from "@/chesses/Advisor.js";
import {Leader} from "@/chesses/Leader.js";


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
  initGame(data){
    console.log(data.game_info)
    const camps_temp = data.game_info.pieces;
    // console.log(data.game_info.pieces)
    console.log("initGame执行")
    ElMessage.info('获取棋盘数据成功')

    current_camp.value = data.game_info.turn
    console.log('current_camp的值是：'+current_camp.value)
    camps.value = [
      new Chariot(XYZToPosition(camps_temp[7].px, camps_temp[7].py, camps_temp[7].pz), 0),
      new Chariot(XYZToPosition(camps_temp[8].px, camps_temp[8].py, camps_temp[8].pz), 0),
      new Warhosre(XYZToPosition(camps_temp[5].px, camps_temp[5].py, camps_temp[5].pz), 0),
      new Warhosre(XYZToPosition(camps_temp[6].px, camps_temp[6].py, camps_temp[6].pz), 0),
      new Gun(XYZToPosition(camps_temp[9].px, camps_temp[9].py, camps_temp[9].pz), 0),
      new Gun(XYZToPosition(camps_temp[10].px, camps_temp[10].py, camps_temp[10].pz), 0),
      new Soilder(XYZToPosition(camps_temp[11].px, camps_temp[11].py, camps_temp[11].pz), 0),
      new Soilder(XYZToPosition(camps_temp[12].px, camps_temp[12].py, camps_temp[12].pz), 0),
      new Soilder(XYZToPosition(camps_temp[13].px, camps_temp[13].py, camps_temp[13].pz), 0),
      new Soilder(XYZToPosition(camps_temp[14].px, camps_temp[14].py, camps_temp[14].pz), 0),
      new Soilder(XYZToPosition(camps_temp[15].px, camps_temp[15].py, camps_temp[15].pz), 0),
      new Bishop(XYZToPosition(camps_temp[3].px, camps_temp[3].py, camps_temp[3].pz), 0),
      new Bishop(XYZToPosition(camps_temp[4].px, camps_temp[4].py, camps_temp[4].pz), 0),
      new Advisor(XYZToPosition(camps_temp[1].px, camps_temp[1].py, camps_temp[1].pz), 0),
      new Advisor(XYZToPosition(camps_temp[2].px, camps_temp[2].py, camps_temp[2].pz), 0),
      new Leader(XYZToPosition(camps_temp[0].px, camps_temp[0].py, camps_temp[0].pz), 0),
      new Chariot(XYZToPosition(camps_temp[23].px, camps_temp[23].py, camps_temp[23].pz), 1),
      new Chariot(XYZToPosition(camps_temp[24].px, camps_temp[24].py, camps_temp[24].pz), 1),
      new Warhosre(XYZToPosition(camps_temp[21].px, camps_temp[21].py, camps_temp[21].pz), 1),
      new Warhosre(XYZToPosition(camps_temp[22].px, camps_temp[22].py, camps_temp[22].pz), 1),
      new Gun(XYZToPosition(camps_temp[25].px, camps_temp[25].py, camps_temp[25].pz), 1),
      new Gun(XYZToPosition(camps_temp[26].px, camps_temp[26].py, camps_temp[26].pz), 1),
      new Soilder(XYZToPosition(camps_temp[27].px, camps_temp[27].py, camps_temp[27].pz), 1),
      new Soilder(XYZToPosition(camps_temp[28].px, camps_temp[28].py, camps_temp[28].pz), 1),
      new Soilder(XYZToPosition(camps_temp[29].px, camps_temp[29].py, camps_temp[29].pz), 1),
      new Soilder(XYZToPosition(camps_temp[30].px, camps_temp[30].py, camps_temp[30].pz), 1),
      new Soilder(XYZToPosition(camps_temp[31].px, camps_temp[31].py, camps_temp[31].pz), 1),
      new Bishop(XYZToPosition(camps_temp[19].px, camps_temp[19].py, camps_temp[19].pz), 1),
      new Bishop(XYZToPosition(camps_temp[20].px, camps_temp[20].py, camps_temp[20].pz), 1),
      new Advisor(XYZToPosition(camps_temp[17].px, camps_temp[17].py, camps_temp[17].pz), 1),
      new Advisor(XYZToPosition(camps_temp[18].px, camps_temp[18].py, camps_temp[18].pz), 1),
      new Leader(XYZToPosition(camps_temp[16].px, camps_temp[16].py, camps_temp[16].pz), 1),

      new Chariot(XYZToPosition(camps_temp[39].px, camps_temp[39].py, camps_temp[39].pz), 2),
      new Chariot(XYZToPosition(camps_temp[40].px, camps_temp[40].py, camps_temp[40].pz), 2),
      new Warhosre(XYZToPosition(camps_temp[37].px, camps_temp[37].py, camps_temp[37].pz), 2),
      new Warhosre(XYZToPosition(camps_temp[38].px, camps_temp[38].py, camps_temp[38].pz), 2),
      new Gun(XYZToPosition(camps_temp[41].px, camps_temp[41].py, camps_temp[41].pz), 2),
      new Gun(XYZToPosition(camps_temp[42].px, camps_temp[42].py, camps_temp[42].pz), 2),
      new Soilder(XYZToPosition(camps_temp[43].px, camps_temp[43].py, camps_temp[43].pz), 2),
      new Soilder(XYZToPosition(camps_temp[44].px, camps_temp[44].py, camps_temp[44].pz), 2),
      new Soilder(XYZToPosition(camps_temp[45].px, camps_temp[45].py, camps_temp[45].pz), 2),
      new Soilder(XYZToPosition(camps_temp[46].px, camps_temp[46].py, camps_temp[46].pz), 2),
      new Soilder(XYZToPosition(camps_temp[47].px, camps_temp[47].py, camps_temp[47].pz), 2),
      new Bishop(XYZToPosition(camps_temp[35].px, camps_temp[35].py, camps_temp[35].pz), 2),
      new Bishop(XYZToPosition(camps_temp[36].px, camps_temp[36].py, camps_temp[36].pz), 2),
      new Advisor(XYZToPosition(camps_temp[33].px, camps_temp[33].py, camps_temp[33].pz), 2),
      new Advisor(XYZToPosition(camps_temp[34].px, camps_temp[34].py, camps_temp[34].pz), 2),
      new Leader(XYZToPosition(camps_temp[32].px, camps_temp[32].py, camps_temp[32].pz), 2)

    ];

    board.value.loadMap(camps.value);

  }
}

const Move = (data) => {
  console.log(board.value)
  data.userid = userid
  socket.value.io.emit('movePiece',data)
}

</script>

<template>
  <Board :my_camp="my_camp" :current_camp="current_camp" ref="board" @requireMove="Move"/>
</template>


<style scoped lang="scss">

</style>