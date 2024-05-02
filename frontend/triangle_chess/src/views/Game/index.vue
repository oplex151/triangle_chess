<script setup >
import { onMounted, ref } from 'vue';
import { Chess } from '@/chesses/Chess';
import {COL, ROWTOP, ROWMID, AREABOT, ROWBOT} from '@/config/config';
import { camps } from '@/lib/game';
import { GEBI } from '@/utils/utils';

const map = new Map();
const getid = (row, col) => (ROWTOP - row - 1) * COL + col + 1;
const camp = ref(0);
let hoverChess;
const isPocus = ref(false);
const focusChess = ref();

const action = (position) => {
  // 未选中
  if (!isPocus.value) {
    if (!hoverChess) return;
    if (hoverChess.camp !== camp.value) return;
    isPocus.value = true;
    focusChess.value = hoverChess;
  }
  // 选中
  else {
    isPocus.value = false;
    if (
        focusChess.value.canMove().includes(position) &&
        moveChess(focusChess.value, position)
    ) {
      // 根据当前棋子的阵营进行切换
      switch (focusChess.value.camp) {
        case 0:
          camp.value = 1;
          break;
        case 1:
          camp.value = 2;
          break;
        case 2:
          camp.value = 0;
          break;
        default:
          // 在这里处理默认情况
          break;
      }
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
      // GEBI(`${chess.position}`).classList.add(chess.camp ? 'camp1' : 'camp0');

      map.set(chess.position, chess);
    });
  }
};

const hover = (position) => {
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

onMounted(initMap);

</script>

<template>
  <div class="Game">
    <div class="camp">目前行动:{{camp == 1 ?'黑方':(camp == 0 ? '红方':'金方')}}</div>

    <div class="board">
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

    <div class="board-tilt-left">
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

    <div class="board-tilt-right">
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