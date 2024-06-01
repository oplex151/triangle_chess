<script setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import Cookies from 'js-cookie';
import { registerSockets, socket, registerSocketsForce, removeSockets } from '@/sockets'
import router from '@/router';
import { ElMessage, ElMessageBox } from "element-plus";

import { onMounted, ref, onUnmounted, computed, getCurrentInstance, onBeforeMount, watch } from 'vue';
import Board from '@/views/Game/board.vue'
import axios from "axios";
import { lives } from '@/chesses/Live';
import * as CONST from '@/lib/const.js'
import Report from '@/components/views/Report.vue'
import Avatar from '@/components/views/Avatar.vue'
import Messager from '@/components/views/Messager.vue';

import useClipboard from 'vue-clipboard3';

const my_camp = ref(Cookies.get('camp'))
const { toClipboard } = useClipboard()



const userid = Cookies.get('userid')
const { proxy } = getCurrentInstance()
const board = ref(null)
const winner_name = ref(null)
const step_count = ref(null)
const match_duration = ref(null)
const record_id = ref(null)
const vis = ref(false)
const to_report_id = ref(-1)
const room_info = JSON.parse(Cookies.get('room_info'))

const game_status = ref(CONST.STATUS_ONING)
const draw_responser = ref([])

const o_message = ref([])
const i_message = ref('')
const my_name = Cookies.get('username')


const copy = async (anything) => {
  try {
    await toClipboard(anything)
    console.log('Copied to clipboard')
  } catch (e) {
    console.error(e)
  }
}

const sendMessage = (message) => {
  console.log(message)
  socket.value.io.emit('sendMessage', {
    'userid': userid,
    'message': i_message.value
  }
  )
  o_message.value.push({ 'user': my_name, 'message': i_message.value })
}
onMounted(() => {
  if (!Cookies.get('camp')) {
    router.replace('/room')
    return
  }
  if (!socket.value) {
    socket.value = new VueSocketIO({
      debug: true,
      connection: SocketIO(main.url),
    })
    // 重新加入房间
    socket.value.io.emit('joinRoom', { 'userid': userid, 'room_id': Cookies.get('room_id') })
  }
  registerSocketsForce(sockets_methods, socket.value, proxy);

  axios.post(main.url + '/api/game/init', {
    'room_id': Cookies.get('room_id')
  },
    {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
  ).then(res => {
    if (res.status == 200) {
      console.log(res.data)
      board.value.initMap(res.data.game_info)
    }
    else {
      ElMessage.error('获取房间信息失败')
      return
    }
  }).catch(error => {
    console.log(error)
  })
  console.log(socket.value)
});

const sockets_methods = {
  movePieceSuccess(data) {
    if (userid == data.userid) {
      ElMessage.info('移动成功')
    }
    else {
      ElMessage.info('玩家' + data.username + '移动成功')
    }
    // 移动棋子_切换阵营
    board.value.moveSuccess(data);
  },
  joinRoomSuccess(data) {
    if (data.userid == Cookies.get('userid')) {
      Cookies.set('room_id', data.room_id)
      ElMessage.success('加入房间成功')
    }
    else {
      ElMessage.success('玩家' + data.username + '加入房间')
    }
  },
  receiveMessage(data){
    if(data.username!=userid)
      o_message.value.push({ 'user': data.username, 'message': data.message })
  },
  leaveRoomSuccess(data) {
    if (data.userid == Cookies.get('userid')) {
      Cookies.remove('room_id')
      Cookies.remove('room_info')
      ElMessage.success('离开房间成功')
    }
    else {
      ElMessage.success('玩家' + data.username + '离开房间')
    }
  },
  gameEnd(data) {
    if (data.winner_name == null){
      winner_name.value = '无';
      ElMessage.info("游戏结束" + "无获胜者")
    }
    else{
      winner_name.value = data.winner_name;
      ElMessage.info('游戏结束' + "获胜者为" + winner_name.value)
    }

    // 模态框位置(待加入)
    step_count.value = data.step_count;
    match_duration.value = data.match_duration;
    record_id.value = data.record_id;
    // 从后端接收到了比赛持续时间的整数值
    let matchDurationSeconds = data.match_duration;

    // 将整数值转换为毫秒
    let matchDurationMilliseconds = matchDurationSeconds * 1000;

    // 使用 Date 对象创建一个新的日期时间
    let matchDurationDate = new Date(matchDurationMilliseconds);

    // 将日期时间格式化为您需要的格式
    let formattedMatchDuration = matchDurationDate.toISOString().substr(11, 8); // 格式化为 HH:mm:ss

    ElMessageBox.confirm(
      `游戏总步数：${data.step_count} 游戏赢家：${data.winner_name} 游戏时长：${formattedMatchDuration} `,
      '游戏结算',
      {
        cancelButtonText: 'OK',
        confirmButtonText: 'share'
      }
    )
    .then((action) => {
      if (action === 'confirm') {
          copy(main.self_url + '/publicShare?recordId=' + record_id.value)
          ElMessage({
            type: 'info',
            message: "分享连接已经复制到剪贴板！",
          })
        }
    })
    .catch((action) => {})
    // 匹配模式退回主页面
    console.log(data.room_type)
    if (data.room_type == 1) {
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods, socket.value, proxy);
      socket.value.io.disconnect()
      socket.value = null
      router.replace('/')
      return
    }
    // 天梯模式
    else if (data.room_type == 2) {
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods, socket.value, proxy);
      socket.value.io.disconnect()
      socket.value = null
      router.replace('/rank')
      return
    }
    // 创房间模式
    else {
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods, socket.value, proxy);
      router.replace('/room')
      return
    }
  },
  surrenderSuccess(data) {
    for (let i = 0; i < 3; i++) {
      if (data.userid == Cookies.get('user' + i))
        lives[i] = false
      board.value.camp = data.game_info.turn
    }
    if (data.userid == Cookies.get('userid')) {
      ElMessage.info('你投降了')
    }
    else {
      ElMessage.info('用户' + data.username + '投降')
    }
  },
  waitForOthers(data){
    draw_responser.value.push({ 'userid': data.userid, 'username': data.username ,'agree':data.agree})
  },
  drawRequest(data) {
    if (my_camp.value>=0){
      if (lives[my_camp.value]) {
        draw_responser.value.push({ 'userid': data.userid, 'username': data.username ,'agree':true})
        game_status.value = CONST.STATUS_DRAWING
        let agree = false
        ElMessageBox.confirm(
          `玩家${data.username}希望求和，您是否同意？`,
          {
            cancelButtonText: '否',
            confirmButtonText: '是'
          }
        )
        .then((action) => {
          if (action === 'confirm') 
            agree = true
          else 
            agree = false
          console.log(agree)
          socket.value.io.emit('respondDraw', {
            'userid': Cookies.get('userid'),
            'agree': agree
          })
        }).catch((action) => {
          console.log(agree)
          socket.value.io.emit('respondDraw', {
            'userid': Cookies.get('userid'),
            'agree': agree
          })
        })
      }
    }
  },
  gameOngoing(data){
    draw_responser.value.push({ 'userid': data.userid, 'username': data.username ,'agree':false})
    ElMessage.info('游戏继续')
    setTimeout(() => {
      game_status.value = CONST.STATUS_ONING
      draw_responser.value = []
    }, 1000)
  },
  processWrong(data) {
    let status1 = data.status
    ElMessage.error("Error due to " + status1)
    if (status1 == CONST.ROOM_NOT_EXIST) {
      router.replace('/room')
    }
    else if (status1 == CONST.NOT_IN_ROOM) {
      ElMessage.error('你不在房间中')
      router.replace('/room')
    }
    else if (status1 == CONST.USER_NOT_LOGIN) {
      ElMessage.error('用户未登录')
      router.replace('/login')
    }
  }
}

function requestSurrender() {
  if(my_camp.value >= 0)
    if(lives[my_camp.value])
      socket.value.io.emit('requestSurrender', {
        'userid': Cookies.get('userid')
      })
    else{
      ElMessage.error('你已经输了，不能投降')
    }
  else{
    ElMessage.error('你不是本游戏的玩家，不能投降')
  }
}


function requestDraw(){
  if(my_camp.value >= 0){
    if(lives[my_camp.value]){
      socket.value.io.emit('requestDraw', {
        'userid': Cookies.get('userid')
      })
      game_status.value = CONST.STATUS_DRAWING
      draw_responser.value.push({ 'userid': userid, 'username': my_name ,'agree':true})
    }
    else{
      ElMessage.error('你已经输了，不能求和')
    }
  }
  else
    ElMessage.error('你不是本游戏的玩家，不能求和')
}

const Move = (data) => {
  data.userid = userid
  socket.value.io.emit('movePiece', data)
}

const handleReportEnd = (id) => {

  vis.value = false;
}
const handleReport = () => {
  console.log(id);
  to_report_id.value = id;
  console.log(to_report_id.value);
  vis.value = true;
}
const camp_1_style = computed(() => {
  if (my_camp.value == 1) {
    return 'board'
  }
  else if (my_camp.value == 0) {
    return 'board-tilt-right'
  }
  else {
    return 'board-tilt-left'
  }
});
const camp_2_style = computed(() => {
  if (my_camp.value == 1) {
    return 'board-tilt-right'
  }
  else if (my_camp.value == 0) {
    return 'board-tilt-left'
  }
  else {
    return 'board'
  }
});
const camp_0_style = computed(() => {
  if (my_camp.value == 1) {
    return 'board-tilt-left'
  }
  else if (my_camp.value == 0) {
    return 'board'
  }
  else {
    return 'board-tilt-right'
  }
});
</script>

<template>
  <Messager :o_message="o_message" v-model:i_message="i_message" @sendMessage="sendMessage" class="messager"/>

  <div class="background-image"></div>
  <div class="chessboard-overlay"></div>
  <div>
    <button class="surrender-button" @click="requestSurrender">投降</button>
  </div>
  <div>
    <button class="surrender-button" @click="requestDraw">求和</button>
  </div>
  <div class="wait-draw-info" v-if="game_status == CONST.STATUS_DRAWING">
    <div v-for="user in draw_responser" :key="user.userid">
      <div class="wait-draw-user-agree" v-if="user.agree">
        {{user.username}}
      </div>
      <div class="wait-draw-user" v-else>
        {{user.username}}
      </div>
    </div>
  </div>
  <div  :class="camp_0_style">
    <Avatar :my_userid=userid :userid=room_info.users[0].userid @reportUser="handleReport">
      <template #name>
        <p>{{room_info.users[0].username}}</p>
      </template>
      <template #avatar>
        {{ room_info.users[0].username }}
      </template>
    </Avatar>
  </div>
    <!---------1号位---------->
    <div  :class="camp_1_style">
    <Avatar :my_userid=userid :userid=room_info.users[1].userid @reportUser="handleReport">
      <template #name>
        <p>{{room_info.users[1].username}}</p>
      </template>
      <template #avatar>
        {{ room_info.users[1].username }}
      </template>
    </Avatar>
    </div>
    <!---------2号位---------->
    <div  :class="camp_2_style">
    <Avatar :my_userid=userid :userid=room_info.users[2].userid @reportUser="handleReport">
      <template #name>
        <p>{{room_info.users[2].username}}</p>
      </template>
      <template #avatar>
        {{ room_info.users[2].username }}
      </template>
    </Avatar>
    </div>
    <Board ref="board" :my_camp ="my_camp" :game_status="game_status" @requireMove="Move" />
    <Report :toreportid=to_report_id :myuserid="userid" :dialogFormVisible=vis @reportEnd="handleReportEnd" />
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

.chessboard-overlay {
  position: absolute;
  top: 35px;
  left: -42px;
  width: 1280 * 1.01px;
  height: 800 * 1.01px;
  background-image: url('@/assets/images/game/chessBoard.jpg');
  background-size: cover;
  opacity: 1.0; /* Adjust opacity as needed */
  z-index: -1;
}

.wait-draw-info{
  margin-top: 20px;
  margin-left: 20px;
  position: relative;
  font-size:20px;
  color: #fff;
  display: inline-flex;
  padding: 10px;
  background-color: #d3a61f;
  border-radius: 10px;
}

.wait-draw-user{
  max-width: 100px;
  min-width: 60px;
  margin: 10px 10px;
  padding: 5px;
  border-radius: 5px;
  background-color: #f56e34;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.wait-draw-user-agree{
  max-width: 100px;
  min-width: 60px;
  margin: 10px 10px;
  padding: 5px;
  border-radius: 5px;
  background-color: #a7d413;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.board{
  position: absolute;
  top: 700px;
  left: 950px;
  z-index: 1;
}
.board-tilt-right{
  position: absolute;
  top: 100px;
  left: 950px;

}
.board-tilt-left{
  position: absolute;
  top: 100px;
  left: 250px;

}
.surrender-button {
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
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  z-index: 99;
  /* Add shadows */
}

.surrender-button:hover {
  background-color: #b48d17;
  color: white;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2), 0 12px 40px 0 rgba(0, 0, 0, 0.19);
  /* Add more shadows */
}
.messager{
  position:absolute;
  top:200px;
  left:1000px;
  max-width: 18%;
  z-index: 1;
  --text-width:190px;
  --text-padding-right:10px;
  --message-height:500px;
  --message-width:10px;
  --message-margin-bottom: 10px;
  // 卧槽原来是这么实现的吗，太逆天了
}
</style>