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
import { GEBI } from '@/utils/utils';

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
const avatars = ref({})
const timer = ref(30);
const interval = ref(null);
const startTimer = (time) => {
  console.log(time)
  if(time == undefined){
    timer.value = 30;
  }
  else{
    timer.value = (time - Date.now())/1000;
  }
  GEBI('timer-info').classList.add('timer-info-on')
  interval.value = setInterval(() => {
    timer.value--;
    ElMessage.info('剩余时间：' + timer.value + 's')
    
    if (timer.value === 0) {
      clearInterval(interval.value);

      ElMessage.error('时间到!')
      socket.value.io.emit('requestSurrender', {
          'userid': Cookies.get('userid')
      })
      timer.value = 30;
      GEBI('timer-info').classList.remove('timer-info-on')
    }
  }, 1000);
};
const copy = async (anything) => {
  try {
    await toClipboard(anything)
    //console.log('Copied to clipboard')
  } catch (e) {
    //console.error(e)
  }
}

const sendMessage = (message) => {
  //console.log(message)
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
      //console.log(res.data)
      board.value.initMap(res.data.game_info)
      if(board.value.camp == my_camp.value){
        startTimer(res.data.next_time);
      }
    }
    else {
      ElMessage.error('获取房间信息失败')
      return
    }
  }).catch(error => {
    //console.log(error)
    if(error.response.status == 550){ //Session expired
      Cookies.remove('room_id')
      Cookies.remove('userid')
      Cookies.remove('room_info')
      Cookies.remove('username')
      Cookies.remove('camp')
      ElMessage({
        message: '会话过期，请重新登录',
        grouping: true,
        type: 'error',
        showClose: true
      })
      router.replace('/login')
    }
  })
  //console.log(socket.value)
  let userids = room_info.users.map(user => {
    return user.userid;
  }) 
  axios.post(main.url + '/api/getAvatars', {'userids': userids.join(',')},
  {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  }
  )
  .then(res => {
      //console.log(res.data)
      avatars.value = res.data
  })
  .catch(err => {
      //console.error(err)
    if(err.response.status == 550){ //Session expired
      Cookies.remove('room_id')
      Cookies.remove('userid')
      Cookies.remove('room_info')
      Cookies.remove('username')
      Cookies.remove('camp')
      ElMessage({
        message: '会话过期，请重新登录',
        grouping: true,
        type: 'error',
        showClose: true
      })
      router.replace('/login')
    }
  })

});

const sockets_methods = {
  movePieceSuccess(data) {
    if (userid == data.userid) {
      ElMessage.info('移动成功')
      clearInterval(interval.value);
    }
    else {
      ElMessage.info('玩家' + data.username + '移动成功')
    }
    // 移动棋子_切换阵营
    board.value.moveSuccess(data);
    if(board.value.camp == my_camp.value){
      startTimer(data.next_time);
    }
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
      if (Cookies.get('camp') == -1) {
        Cookies.remove('game_id')
        Cookies.remove('camp')
        removeSockets(sockets_methods, socket.value, proxy);
        socket.value.io.disconnect()
        socket.value = null
        router.replace('/')
        return
      }
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
    //console.log(data.room_info)
    
    // 创房间模式
    if(data.room_type == 0){
      // Cookies.set('room_info',data.room_info)
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods, socket.value, proxy);
      sessionStorage.setItem('fromGame', 'true')
      router.replace('/room')
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
    // 匹配模式退回主页面
    //console.log(data.room_type)
    else {
      Cookies.remove('game_id')
      Cookies.remove('camp')
      removeSockets(sockets_methods, socket.value, proxy);
      socket.value.io.disconnect()
      socket.value = null
      router.replace('/')
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
      clearInterval(interval.value);
    }
    else {
      ElMessage.info('用户' + data.username + '投降')
    }
    if (board.value.camp == my_camp.value){
      startTimer(data.next_time);
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
          //console.log(agree)
          socket.value.io.emit('respondDraw', {
            'userid': Cookies.get('userid'),
            'agree': agree
          })
        }).catch((action) => {
          //console.log(agree)
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
    //ElMessage.error("Error due to " + status1)
    if (status1 == CONST.ROOM_NOT_EXIST) {
      ElMessage.error('房间不存在')
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
    else if (status1 == CONST.REPEAT_DRAW_REQUEST) {
      ElMessage.error('重复的求和请求或者有求和决议在进行')
    }
    else if(status1 == CONST.SESSION_EXPIRED){
      Cookies.remove('room_id')
      Cookies.remove('userid')
      Cookies.remove('room_info')
      Cookies.remove('camp')
      Cookies.remove('username')

      ElMessage({
        message: '会话过期，请重新登录',
        grouping: true,
        type: 'error',
        showClose: true
      })
      router.replace('/login')
    }
  }
}

onUnmounted(() => {
  clearInterval(interval.value);
})

function requestSurrender() {
  if(my_camp.value >= 0)
    if ((!lives[my_camp.value])){
      ElMessage.error('你已经输了，不能投降')
      return
    }
    else if(my_camp.value!=board.value.camp){
      ElMessage.error('现在不是你的回合，不能投降')
      return
    }
    else
      ElMessageBox.confirm('确定要投降吗？', '投降', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        socket.value.io.emit('requestSurrender', {
          'userid': Cookies.get('userid')
        })
      }).catch(() => {
        ElMessage.info('已取消')
      })
  else{
    ElMessage.error('你不是本游戏的玩家，不能投降')
  }
}



function leaveRoom() {
  socket.value.io.emit('leaveRoom', { 'room_id': Cookies.get('room_id'), 'userid': Cookies.get('userid') })
  //console.log("点击了退出房间")
  i_message.value = ''
  o_message.value = []
}

function requestDraw(){
  if(my_camp.value >= 0){
    if(lives[my_camp.value]){
      socket.value.io.emit('requestDraw', {
        'userid': Cookies.get('userid')
      })
      game_status.value = CONST.STATUS_DRAWING
      if (draw_responser.value.length == 0) {  // 只有请求为空时才可以发起请求
        draw_responser.value.push({ 'userid': userid, 'username': my_name ,'agree':true})
      }
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
const handleReport = (id) => {
  to_report_id.value = id;
  //console.log(to_report_id.value);
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
  <Messager :o_message="o_message" v-model:i_message="i_message" @sendMessage="sendMessage" class="messager" v-if="my_camp >= 0"/>
  
  <div class="background-image"></div>
  <div class="chessboard-overlay"></div>
  <div class="timer-info" id="timer-info">剩余时间：{{timer}}
  </div>
  <div v-if="my_camp >= 0">
    <button class="surrender-button" @click="requestSurrender">投降</button>
  </div>
  <div v-if="my_camp >= 0">
    <button class="surrender-button" @click="requestDraw">求和</button>
  </div>
  <div v-if="my_camp == -1">
    <button class="leave-button" @click="leaveRoom">退出房间</button>
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
        <img :src="main.url+avatars[room_info.users[0].userid]" alt="头像" />
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
        <img :src="main.url+avatars[room_info.users[1].userid]" alt="头像" />
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
        <img :src="main.url+avatars[room_info.users[2].userid]" alt="头像" />
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
  margin-left: 40px;
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

.leave-button {
  background-color: #ecb920;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 20px 30px;
  transition-duration: 0.4s;
  cursor: pointer;
  border-radius: 8px;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
  z-index: 99;
  /* Add shadows */
}

.leave-button:hover {
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
}
.timer-info{
  position:absolute;
  top:600px;
  left:50px;
  background-color: #dbf685;
  padding: 10px;
  border-radius: 10px;
  z-index: 99;
}
.timer-info-on{
  animation: colorChange 30s infinite;
}
@keyframes colorChange {
    0% {
      background-color: #c4ffa0;
    }
    75% {
      background-color: #f68585;
    }
    100% {
      background-color: #d73b3b;
    }
  }
</style>