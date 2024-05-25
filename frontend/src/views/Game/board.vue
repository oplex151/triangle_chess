<script setup>
import main from '@/main'
import { camps, initChess } from '@/lib/game';
import { GEBI } from '@/utils/utils';
import Cookies from 'js-cookie';
import { registerSockets, socket } from '@/sockets'
import { XYZToPosition, PositionToXYZ } from '@/lib/convert'
import router from '@/router';
import { ElMessage } from "element-plus";
import { lives, changeLives } from '@/chesses/Live';
import { onMounted, ref, onUnmounted, computed, getCurrentInstance } from 'vue';
import { COL, ROWTOP, ROWMID, AREABOT, ROWBOT } from '@/config/config';


const map = new Map();
const getid = (row, col) => (ROWTOP - row - 1) * COL + col + 1;
const camp = ref(0);

let hoverChess;
const isPocus = ref(false);
const focusChess = ref();
const hoverposition = ref();
const hover_xyz = ref([0, 0, 0])
const xyz = ref([0, 0, 0])
const xyzn = ref([0, 0, 0])
const my_camp_str = ['红方', '黑方', '金方']

const props = defineProps(['my_camp'])
const emit = defineEmits(['requireMove'])
const backgroundImageUrls = ref([]);

//核心财产
const chessPoints = [
  [{ x: 0, y: 0 }, { x: 37, y: 4 }, { x: 77, y: 3 }, { x: 111, y: -1 }, { x: 150, y: -1 }, { x: 183, y: -1 }, { x: 222, y: -1 }, { x: 261, y: 2 }, { x: 299, y: 1 }],
  [{ x: -13, y: -30 }, { x: 24, y: -35 }, { x: 64, y: -43 }, { x: 108, y: -47 }, { x: 150, y: -55 }, { x: 192, y: -47 }, { x: 235, y: -41 }, { x: 276, y: -34 }, { x: 316, y: -30 }],
  [{ x: -34, y: -59 }, { x: 12, y: -71 }, { x: 59, y: -83 }, { x: 105, y: -98 }, { x: 150, y: -109 }, { x: 197, y: -97 }, { x: 244, y: -84 }, { x: 288, y: -74 }, { x: 335, y: -59 }],
  [{ x: -51, y: -89 }, { x: -1, y: -108 }, { x: 50, y: -126 }, { x: 100, y: -146 }, { x: 150, y: -163 }, { x: 201, y: -144 }, { x: 252, y: -127 }, { x: 301, y: -106 }, { x: 351, y: -90 }],
  [{ x: -68, y: -119 }, { x: -14, y: -143 }, { x: 41, y: -169 }, { x: 96, y: -194 }, { x: 150, y: -218 }, { x: 206, y: -194 }, { x: 263, y: -169 }, { x: 317, y: -144 }, { x: 370, y: -121 }]
];

function mapChessToPoint(row, col) {
  // Check if row and col are within bounds
  if (row >= 1 && row <= chessPoints.length && col >= 1 && col <= chessPoints[0].length) {
    const x = chessPoints[row - 1][col- 1].x;
    const y = chessPoints[row- 1][col- 1].y;
    return { top: y, left: x };
  } else {
    // Handle out of bounds error
    console.error('Row or column out of bounds:', row, col);
    return { top: 0, left: 0 }; // Return default values or handle error as needed
  }
}

// 定义父组件可以调用的函数（这里只有defineExpose）
function moveSuccess(data) {
  let position_start = XYZToPosition(data.x1, data.y1, data.z1)
  let position_end = XYZToPosition(data.x2, data.y2, data.z2)

  focusChess.value = map.get(position_start);
  // 移动棋子
  moveChess(focusChess.value, position_end);

  // 切换到下一个阵营
  camp.value = (camp.value + 1) % 3;
  while (lives[camp.value] == false) {
    camp.value = (camp.value + 1) % 3;
  }
}

const camp_1_style = computed(() => {
  if (props.my_camp == 1) {
    return 'board'
  }
  else if (props.my_camp == 0) {
    return 'board-tilt-right'
  }
  else {
    return 'board-tilt-left'
  }
});
const camp_2_style = computed(() => {
  if (props.my_camp == 1) {
    return 'board-tilt-right'
  }
  else if (props.my_camp == 0) {
    return 'board-tilt-left'
  }
  else {
    return 'board'
  }
});
const camp_0_style = computed(() => {
  if (props.my_camp == 1) {
    return 'board-tilt-left'
  }
  else if (props.my_camp == 0) {
    return 'board'
  }
  else {
    return 'board-tilt-right'
  }
});
const action = (position) => {
  // 未选中
  if (!isPocus.value) {
    if (!hoverChess) return;

    if (hoverChess.camp !== camp.value) return;
    // 如果不是你走，不能选中
    if (camp.value != props.my_camp && props.my_camp >= 0) {
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
      // 发送移动消息
      emit('requireMove', {
        'x1': xyzn.value[0], 'y1': xyzn.value[1], 'z1': xyzn.value[2],
        'x2': xyz.value[0], 'y2': xyz.value[1], 'z2': xyz.value[2]
      })
    }

    // 暂时不启用，重新选择棋子
    else {
      if (!hoverChess) return;
      if (hoverChess.camp !== camp.value) return;
      // 如果不是你走，不能选中
      if (camp.value != props.my_camp && props.my_camp >= 0) {
        return;
      }
      isPocus.value = true;
      focusChess.value = hoverChess;
      GEBI(`${hoverChess.position}`).classList.add('chess_on');
    }
  }
};
const moveChess = (chess, to) => {
  if (map.get(to)?.camp === camp.value) return false;
  map.delete(chess.position);
  chess.move(to);
  map.set(to, chess);
  return true;
};
const initMap = (game_info) => {
  console.log("initMap执行开始")
  // 设置轮到谁走
  camp.value = game_info.turn
  // 设置活着的玩家
  changeLives(game_info.lives)
  // console.log("111111111111")
  initChess(game_info)
  for (const [k, camp] of Object.entries(camps)) {
    camp.get().forEach((chess) => {
      GEBI(`${chess.position}`).innerText = chess.name;
      switch (chess.camp) {
        case 0:
          GEBI(`${chess.position}`).classList.add('camp0');
          chess.image = "src/assets/images/game/chess/realChess/" + chess.name + "白.png";
          break;

        case 1:
          GEBI(`${chess.position}`).classList.add('camp1');
          chess.image = "src/assets/images/game/chess/realChess/" + chess.name + "黑.png";
          break;
        case 2:
          GEBI(`${chess.position}`).classList.add('camp2');
          chess.image = "src/assets/images/game/chess/realChess/" + chess.name + "金.png";
          break;
      }
      GEBI(`${chess.position}`).classList.add('chess-background');  // 添加自定义class
      GEBI(`${chess.position}`).style.background = `url(${chess.image}) center center / contain no-repeat`;
      GEBI(`${chess.position}`).style.backgroundSize = '53px'; // 将背景图片大小设置为 53px，宽度和高度均为 53px
      // element.style.backgroundImage = `url(${chess.image})`;  // 设置背景图片
      console.log(chess.image);
      map.set(chess.position, chess);
    });
  }
  console.log("initMap执行结束")

};

const hover = (position) => {
  hoverposition.value = position;

  if (hoverChess)
    GEBI(`${hoverChess.position}`).classList.remove('chess_hover');

  if (!map.has(position)) return;

  hoverChess = map.get(position);

  if (hoverChess.camp != props.my_camp) return;

  GEBI(`${hoverChess.position}`).classList.add('chess_hover');
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

onMounted(() => {
  // initMap(); // 初始化棋盘，改成相应后端消息来哦初始化棋盘
});

onUnmounted(Destory);
// 一定要写在最后
defineExpose({
  moveSuccess,
  initMap,
  camp,
})
</script>
<template>
  <div class="Game">
    <div class="camp">
      目前行动: {{ camp == 1 ? '黑方' : (camp == 0 ? '红方' : '金方') }}
      我的阵营: {{ props.my_camp >= 0 ? my_camp_str[props.my_camp] : '未知' }}
    </div>
    <!--2号-->
    <div :class="camp_2_style">
      <div v-for="(row, index) in ROWTOP" :key="row" class="row">
        <div class="block chess" :id="getid(index, i) + ''" v-for="(col, i) in COL" :key="col"
             @mouseover="hover(getid(index, i))" @mouseout="out(getid(index, i))" @click="action(getid(index, i))"
             v-if="index <= 4" :style="{ top: mapChessToPoint(row, col).top + 'px', left: mapChessToPoint(row, col).left + 'px'}">
        </div>
      </div>
    </div>

    <div :class="camp_1_style">
      <div v-for="(row, index) in ROWTOP" :key="row" class="row">
        <div class="block chess" :id="getid(index, i) + ''" v-for="(col, i) in COL" :key="col"
             @mouseover="hover(getid(index, i))" @mouseout="out(getid(index, i))" @click="action(getid(index, i))"
             v-if="index > 4 && index <= 9" :style="{ top: mapChessToPoint(row - 5, col).top + 'px', left: mapChessToPoint(row - 5, col).left + 'px' }">
        </div>
      </div>
    </div>

    <div :class="camp_0_style">
      <div v-for="(row, index) in ROWTOP" :key="row" class="row">
        <div class="block chess" :id="getid(index, i) + ''" v-for="(col, i) in COL" :key="col"
             @mouseover="hover(getid(index, i))" @mouseout="out(getid(index, i))" @click="action(getid(index, i))"
             v-if="index > 9 && index <= 14" :style="{ top: mapChessToPoint(row - 10 , col).top + 'px', left: mapChessToPoint(row - 10, col).left + 'px'}">
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped lang="scss">
// 样式说明：挂载的时候，如果这个元素挂载到0,0处，那么left 540px, top 400px对应棋盘中央
// 换句话说棋盘大小是1080*800 px

.chess-background {
  opacity: 1.0; /* Adjust opacity as needed */
  background-size: cover;  // 确保背景图片覆盖整个元素
  background-repeat: no-repeat;  // 防止背景图片重复
}

.camp {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 24px;
  color: #e9b526;
}

// 红方阵营
.camp0 {
  //background-color: transparent !important;
}

// 黑方阵营
.camp1 {
  //background-color: transparent !important;
}

// 金方阵营
.camp2 {
  //background-color: transparent !important;
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
  //color: wheat;
  color: transparent;
  //background-image: url("@/assets/images/game/chess/realChess/车白.png");
  // 文本不可选中
  user-select: none;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
  border-radius: 20px;
  box-shadow: #383a3f;
  border-width: 4px;
  border-color: white;
  border-style: inset;
  background-size: contain; // Ensure the chess piece image fits within the block
  background-repeat: no-repeat; // Prevent the image from repeating
}

.chess_hover {
  border-color: #fff !important;
  border-left-width: -8px !important;
  border-top-width: -8px !important;
  border-left-style: inset !important;
  border-top-style: inset !important;
  border-bottom-width: 8px !important;
  border-right-width: 8px !important;
  border-bottom-style: outset !important;
  border-right-style: outset !important;
}

//定义一个动画时间戳
@keyframes vary {
  0% {
    color: rgba(rgb(244, 8, 47), 0.6);
  }

  50% {
    color: rgba(rgb(244, 8, 47), 1.2);
  }

  100% {
    color: rgba(rgb(244, 8, 47), 0.6);
  }
}

.chess_on {
  animation: vary 2s !important;
  animation-iteration-count: infinite !important;
}

.invert {
  transform: rotate(180deg);
}

.block {
  width: 50px;
  height: 50px;
  border: 1px transparent;
  &:hover {
    background-color: skyblue;
  }

  position: absolute;
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
  top: 685px;
  left: 466px;
  transform: translate(-50%, -50%) rotate(0deg);
  transform-origin: top left;
  //width: 100vh; /* 设置宽度为视口高度，确保棋盘在旋转时不会溢出 */
  //height: 100vh; /* 设置高度为视口高度，确保棋盘在旋转时不会溢出 */
  display: flex;
  flex-direction: column;
  align-items: center;

}

.board :deep(.chess) {
  rotate: 180deg !important;
  // 某些浏览器（例如小智双核）不支持 ::v-deep 伪元素选择器，这个我也没办法，只能这样了
  // 御三家firefox,chrome,edge都支持
}

// = 1
.board-tilt-left {
  position: absolute;
  top: 178px;
  left: 525px;
  transform: translate(-50%, -50%) rotate(120deg);
  transform-origin: top left;
  //width: 100vh; /* 设置宽度为视口高度，确保棋盘在旋转时不会溢出 */
  //height: 100vh; /* 设置高度为视口高度，确保棋盘在旋转时不会溢出 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.board-tilt-right {
  position: absolute;
  top: 482px;
  left: 933px;
  transform: translate(-50%, -50%) rotate(-120deg);
  transform-origin: top left;
  //width: 100vh; /* 设置宽度为视口高度，确保棋盘在旋转时不会溢出 */
  //height: 100vh; /* 设置高度为视口高度，确保棋盘在旋转时不会溢出 */
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>