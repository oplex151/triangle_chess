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
    let position_start = XYZToPosition(data.x1,data.y1,data.z1)
    let position_end = XYZToPosition(data.x2,data.y2,data.z2)
    
    focusChess.value = map.get(position_start);
    // 移动棋子
    moveChess(focusChess.value,position_end);

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


// const front_position = computed(() => {
//   switch (my_camp) {
//     case 0:
//       return 2;
//     case 1:
//       return 1;
//     case 2:
//       return 0;
//     default:
//       return 2;
// }}
// );
// const back_position = computed(() => {
//   switch (my_camp) {
//     case 0:
//       return 1;
//     case 1:
//       return 2;
//     case 2:
//       return 0;
//     default:
//       return 1;
// }}
// );
const camp_1_style = computed(() => {
  if (my_camp==1){
    return 'board'
  }
  else if(my_camp==0){
    return 'board-tilt-right'
  }
  else{
    return 'board-tilt-left'
  }
});
const camp_2_style = computed(() => {
  if(my_camp==1){
    return 'board-tilt-right'
  }
  else if(my_camp==0){
    return 'board-tilt-left'
  }
  else{
    return 'board'
  }
});
const camp_0_style = computed(() => {
  if (my_camp==1){
    return 'board-tilt-left'
  }
  else if(my_camp==0){
    return 'board'
  }
  else{
    return 'board-tilt-right'
  }
});
const action = (position) => {
  // 未选中
  if (!isPocus.value) {
    if (!hoverChess) return;
    if (hoverChess.camp !== camp.value) return;
    // 如果不是你走，不能选中
    if (camp.value != my_camp && my_camp>=0){
      return;
    }
    isPocus.value = true;
    GEBI(`${hoverChess.position}`).classList.add('chess_on');
    focusChess.value = hoverChess;
  }
  // 选中
  else {
    isPocus.value = false;
    GEBI(`${focusChess.value.position}`).classList.remove('chess_on');    
    if (
        focusChess.value.canMove().includes(position) 
        // 暂时不启用, 阻止自己的棋子吃掉自己的棋子
        && map.get(position)?.camp !== camp.value
    ) {
      xyz.value = PositionToXYZ(position)
      xyzn.value = PositionToXYZ(focusChess.value.position)
      socket.value.io.emit('movePiece',{'userid':userid,'chess_type':1, 
                                      'x1':xyzn.value[0], 'y1':xyzn.value[1], 'z1':xyzn.value[2], 
                                      'x2':xyz.value[0], 'y2':xyz.value[1], 'z2':xyz.value[2]})
    }

    // 暂时不启用，重新选择棋子
    else{
      if (!hoverChess) return;
      if (hoverChess.camp !== camp.value) return;
      // 如果不是你走，不能选中
      if (camp.value != my_camp && my_camp>=0){
        return;
      }
      isPocus.value = true;
      focusChess.value = hoverChess;
      GEBI(`${hoverChess.position}`).classList.add('chess_on');
    }
  }
};

let y1 = 0
let y2 = 1


const moveChess = (chess, to) => {
  if (map.get(to)?.camp === camp.value) return false;
  map.delete(chess.position);
  chess.move(to);
  map.set(to, chess);
  return true;
};
const initMap = () => {
  for (const [k, camp] of Object.entries(camps)) {
    camp.get().forEach((chess) => {
      GEBI(`${chess.position}`).innerText = chess.name;
      switch (chess.camp){
        case 0:
          GEBI(`${chess.position}`).classList.add('camp0');
          break;
        case 1:
          GEBI(`${chess.position}`).classList.add('camp1');
          break;
        case 2:
          GEBI(`${chess.position}`).classList.add('camp2');
          break;
      }
      
      map.set(chess.position, chess);
    });
  }
  // 注册socket监听
  registerSockets(sockets_methods,socket.value,proxy);
};

const hover = (position) => {
  hoverposition.value = position;
  
  if (!map.has(position)) return;
  hoverChess = map.get(position);
  hoverChess.canMove().forEach((posi) => {
    GEBI(`${posi}`).classList.add('moviable');
  });
};

const out = (position) => {
  if (!map.has(position)) return;
  hoverChess.canMove().forEach((posi) => {
    GEBI(`${posi}`).classList.remove('moviable');
  });
};

const Destory = () => {
};

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
  initMap(); // 初始化棋盘，改成相应后端消息来哦初始化棋盘
});
onUnmounted(Destory);
</script>

<template>
  <div class="Game">
    <div class="camp">
      目前行动:{{camp == 1 ?'黑方':(camp == 0 ? '红方':'金方')}}
      我的阵营:{{my_camp>=0?my_camp_str[my_camp]:'未知'}}
      位置：{{hoverposition}}
      XYZ：{{[hover_xyz[0],hover_xyz[1],hover_xyz[2]]}}
      金色:{{camp_2_style}}
      Mycamp:{{my_camp}}
    </div>
    <!--2号-->
    <div :class="camp_2_style">
      <!-- 遍历成棋盘 -->
      <!-- 渲染所要的行数 -->
      <div v-for="(row, index) in ROWTOP"
           :key="row"
           class="row"
      >
        <!-- 渲染所要的列数 -->
        <div class="block chess"
             :id="getid(index, i) + ''"
             v-for="(col, i) in COL"
             :key="col"
             @mouseover="hover(getid(index, i))"
             @mouseout="out(getid(index, i))"
             @click="action(getid(index, i))"
             v-if="index <= 4"
        >
        </div>
      </div>
    </div>
    
    <div :class="camp_1_style">
      <div v-for="(row, index) in ROWTOP"
           :key="row"
           class="row"
      >
        <!-- 渲染所要的列数 -->
        <div class="block chess"
             :id="getid(index, i) + ''"
             v-for="(col, i) in COL"
             :key="col"
             @mouseover="hover(getid(index, i))"
             @mouseout="out(getid(index, i))"
             @click="action(getid(index, i))"
             v-if="index > 4 && index <= 9"
        >
        </div>
      </div>
    </div>

    <div :class="camp_0_style">
      <div v-for="(row, index) in ROWTOP"
           :key="row"
           class="row"
      >
        <!-- 渲染所要的列数 -->
        <div class="block chess"
             :id="getid(index, i) + ''"
             v-for="(col, i) in COL"
             :key="col"
             @mouseover="hover(getid(index, i))"
             @mouseout="out(getid(index, i))"
             @click="action(getid(index, i))"
             v-if="index > 9 && index <= 14"
        >
        </div>
      </div>
    </div>

  </div>
</template>


<style scoped lang="scss">

.camp {
  position: absolute;
  top: 0;
  left: 0;
}
// 红方阵营
.camp0 {
  background-color: #ec7357 !important;
}
// 黑方阵营
.camp1 {
  background-color: #383a3f !important;
}
// 金方阵营
.camp2 {
  background-color: #999900 !important;
}


//定义一个动画时间戳
@keyframes fade {
  0% {
    background-color: rgba(pink, 0.4);
  }
  50% {
    background-color: rgba(pink, 1);
  }
  100% {
    background-color: rgba(pink, 0.4);
  }
}
// 定义一个动画
.moviable {
  background-color: pink;
  animation: fade 2s;
  animation-iteration-count: infinite;
}
.chess {
  color: wheat;
  // 文本不可选中
  user-select: none;
  display: flex;
  justify-content: center;
  align-items: center;
}
.chess_on{
  color: red !important;
}
.invert{
  transform: rotate(180deg);
}
.block {
  width: 50px;
  height: 50px;
  border: 1px solid skyblue;
  &:hover {
    background-color: skyblue;
  }
}
.row {
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translate(-50%, -50%) rotate(0deg);
}

.row-tilt-left {
  display: flex;
  align-items: center;
  justify-content: center;
  transform: translate(-50%, -50%) rotate(0deg);
}

.board {
  position: absolute;
  top: 900px;
  left: 800px;
  transform: translate(-50%, -50%) rotate(180deg);
  transform-origin: top left;
  //width: 100vh; /* 设置宽度为视口高度，确保棋盘在旋转时不会溢出 */
  //height: 100vh; /* 设置高度为视口高度，确保棋盘在旋转时不会溢出 */
  display: flex;
  flex-direction: column;
  align-items: center;
}
.board :deep(.chess){
  rotate: 180deg;
  // 某些浏览器（例如小智双核）不支持 ::v-deep 伪元素选择器，这个我也没办法，只能这样了
  // 御三家firefox,chrome,edge都支持
}
// = 1
.board-tilt-left {
  position: absolute;
  top: 368px;
  left: 492px;
  transform: translate(-50%, -50%) rotate(-60deg);
  transform-origin: top left;
  //width: 100vh; /* 设置宽度为视口高度，确保棋盘在旋转时不会溢出 */
  //height: 100vh; /* 设置高度为视口高度，确保棋盘在旋转时不会溢出 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.board-tilt-right {
  position: absolute;
  top: 368px;
  left: 1105px;
  transform: translate(-50%, -50%) rotate(60deg);
  transform-origin: top left;
  //width: 100vh; /* 设置宽度为视口高度，确保棋盘在旋转时不会溢出 */
  //height: 100vh; /* 设置高度为视口高度，确保棋盘在旋转时不会溢出 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

</style>