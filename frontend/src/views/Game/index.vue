<script setup >
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import Cookies from 'js-cookie';
import { registerSockets, socket, registerSocketsForce,removeSockets} from '@/sockets'
import router from '@/router';
import {ElMessage,ElMessageBox} from "element-plus";

import { onMounted, ref ,onUnmounted,computed,getCurrentInstance,onBeforeUnmount} from 'vue';
import Board from '@/views/Game/board.vue'
import axios from "axios";

let my_camp = Cookies.get('camp')
const userid =  Cookies.get('userid')
const {proxy} = getCurrentInstance()
const board = ref(null)
const winner_name = ref(null)
const step_count = ref(null)
const match_duration = ref(null)


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
    match_duration.value = data.match_duration;

    // 从后端接收到了比赛持续时间的整数值
    let matchDurationSeconds = data.match_duration;

    // 将整数值转换为毫秒
    let matchDurationMilliseconds = matchDurationSeconds * 1000;

    // 使用 Date 对象创建一个新的日期时间
    let matchDurationDate = new Date(matchDurationMilliseconds);

    // 将日期时间格式化为您需要的格式
    let formattedMatchDuration = matchDurationDate.toISOString().substr(11, 8); // 格式化为 HH:mm:ss

    ElMessageBox.alert(
        `游戏总步数：${data.step_count} 游戏赢家：${data.winner_name} 游戏时长：${formattedMatchDuration} `,
        '游戏结算',
        {
          confirmButtonText: 'OK',
          callback: (action) => {
            ElMessage({
              type: 'info',
              message: `action: ${action}`,
            })
          },
        }
    )

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

  // playerSurrender(data){
  //   ElMessage.info("用户"+data.userid+"投降！");
  // },

  processWrong(data){
    let status1 = data.status
    ElMessage.error("Error due to "+status1)
  },
}

function requestSurrender(){
  axios.post(main.url + '/api/game/surrender',{
        'userid': Cookies.get('userid')
      },{
    headers: {'Content-Type':'application/x-www-form-urlencoded'},
  }
  ).then(res => {
    if(res.status==200) {
      ElMessage.info("用户"+res.data.userid+"投降！");
    }
    else{
      ElMessage.error('投降失败')
      return
    }
  }).catch(error => {
    console.log(error)
  })

}


const Move = (data) => {
  console.log(board.value)
  data.userid = userid
  socket.value.io.emit('movePiece',data)
}

</script>

<template>
  <div class="background-image"></div>
  <div>
    <button class="surrender-button" @click="requestSurrender">投降</button>
  </div>
  <Board  :my_camp="my_camp"  ref="board" @requireMove="Move"/>
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

.surrender-button{
  background-color: #ecb920;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 20px 50px;
  transition-duration: 0.4s;
  cursor: pointer;
  border-radius: 8px;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19); /* Add shadows */
}

.surrender-button:hover{
  background-color: #b48d17;
  color: white;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2), 0 12px 40px 0 rgba(0,0,0,0.19); /* Add more shadows */
}

</style>