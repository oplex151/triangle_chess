<script setup>
import { onMounted, ref, onUnmounted, computed, getCurrentInstance, onBeforeUnmount, watch, nextTick } from 'vue';
import { ElMessage } from "element-plus";
import { useRouter } from 'vue-router';
import Cookies from 'js-cookie'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { User, HomeFilled, Share } from '@element-plus/icons-vue'
import { registerSockets, socket, removeSockets } from '@/sockets'
import Board from '@/views/Game/board.vue'
import game_info from '@/assets/jsons/game_info.json'
import Report from '@/components/views/Report.vue'
import Avatar from '@/components/views/Avatar.vue'

const start = ref(false)
const options = ref([])
const value = ref('')
const loading = ref(true)
const { proxy } = getCurrentInstance()
const router = useRouter()
const userid = Cookies.get('userid')
const moves = ref([])
const my_camp = ref(-1)
const step = ref(0)
const board = ref(null)
const map_state = ref(game_info)
import useClipboard from 'vue-clipboard3';


const { toClipboard } = useClipboard()


let status1 = ''

const userids = computed(() => {
    let names = [-1,-1,-1]    
    for (let item=0 ; item <options.value.length; item++){
        if(options.value[item]['recordId']==value.value){            
            names[0] = options.value[item]['p1']
            names[1] = options.value[item]['p2']
            names[2] = options.value[item]['p3']
            break
        }
    }
    return names

})
const name = computed(()=>{
    return userids.value
})
const EndGo = () => {
    console.log('EndGo')
    start.value = false
    moves.value = []
    step.value = 0
    my_camp.value = -1
}
const sockets_methods = {
    gameRecord(data) {
        options.value = data.record[0]
        console.log(options.value)
        loading.value = false
    },
    gameMoveRecord(data) {
        console.log(data)
        moves.value = data.record[0]
        loading.value = false
        start.value = true
        console.log(game_info)
        map_state.value = game_info
        // 使用nextTick等board初始化完成
        nextTick(() => {
            board.value.initMap(map_state.value)
        });

    },
    processWrong(data) {
        status1 = data.status
        ElMessage.error("Error due to " + status1)
    },
}
const getCamp = (game_head) => {
    if (game_head.p1 == userid) {
        return 0
    }
    else if (game_head.p2 == userid) {
        return 1
    }
    else if (game_head.p3 == userid) {
        return 2
    }
    else
        return -1
}
onMounted(() => {
    if (!socket.value) {
        socket.value = new VueSocketIO({
            debug: true,
            connection: SocketIO(main.url),
        })
    }
    registerSockets(sockets_methods, socket.value, proxy);
    console.log(socket.value)
    socket.value.io.emit('viewGameRecords', { 'userid': userid })
});
// function goBackHome() {
//     removeSockets(sockets_methods, socket.value, proxy)
//     socket.value.io.disconnect()
//     socket.value = null
//     router.push('/')
// }
onUnmounted(() => {
    try {
        removeSockets(sockets_methods, socket.value, proxy);
        socket.value.io.disconnect()
        socket.value = null
        console.log("Record Remove Socket Success!")
    }
    catch (err) {
        console.log("Record Remove Socket Failed!")
        console.log(err)
    }

});
const Get = ref(() => {
    // console.log(value.value)
    my_camp.value = getCamp(value.value)
    // console.log(value.value['recordId'])
    socket.value.io.emit('viewMoveRecords', { 'record_id': value.value})
})

const Move = (data) => {
    console.log(data)
}

const Next = () => {
    if (step.value >= moves.value.length) {
        ElMessage.info('已经到最后一步')
        return
    }
    let data = moves.value[step.value]
    data.pos1 = data.startPos.split(',')
    data.pos2 = data.endPos.split(',')
    data.x1 = parseInt(data.pos1[0])
    data.y1 = parseInt(data.pos1[1])
    data.z1 = parseInt(data.pos1[2])
    data.x2 = parseInt(data.pos2[0])
    data.y2 = parseInt(data.pos2[1])
    data.z2 = parseInt(data.pos2[2])
    console.log(data)
    step.value += 1
    board.value.moveSuccess(data)
}


const vis = ref(false)
const to_report_id = ref(0)
const handleReportEnd = () => {
    vis.value = false
}
const handleReport = (userid) => {
    to_report_id.value = userid
    vis.value = true
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
const copy = async (anything) => {
  try {
    await toClipboard(anything)
    console.log('Copied to clipboard')
  } catch (e) {
    console.error(e)
  }
}
const share = () => {
    if(value.value){
        copy(main.self_url+'/publicShare?recordId='+value.value)
        ElMessage.success('链接已复制到剪贴板')
    }

}
</script>
<template>
    <Report :toreportid="to_report_id" :myuserid="userid" :dialogFormVisible=vis @reportEnd="handleReportEnd" />
    <div class="background-image-Record"></div>
    
    <!-- <button class="button-home" @click="goBackHome()">
            <el-icon style="vertical-align: middle" size="30px">
                <HomeFilled />
            </el-icon>
        </button> -->
    <button class="button-share" @click="share">
        <el-icon style="vertical-align: middle" size="30px">
                <Share />
            </el-icon>
    </button>
    <div v-if="start">
        <button @click="EndGo" class="button">结束回放</button>   
        <div class="brd2">     
        <div class="brd1">
            <div class="chessboard-overlay"></div>
            <div class="chessboard-container">
            <Board :my_camp="my_camp" ref="board" @requireMove="Move" />
            </div>
            <button @click="Next" class="next_button">下一步</button>
            <div class="avatar">
            <!---------0号位---------->
            <div :class="camp_0_style">
            <Avatar :my_userid="userid" :userid="userids[0]" @reportUser="handleReport">
                <template #name>
                    <p>{{ name[0] }}</p>
                </template>
                <template #avatar>
                    {{ name[0] }}
                </template>
            </Avatar>
            </div>
            <!---------1号位---------->
            <div :class="camp_1_style">
            <Avatar :my_userid="userid" :userid="userids[1]" @reportUser="handleReport">
                <template #name>
                    <p>{{ name[1] }}</p>
                </template>
                <template #avatar>
                    {{ name[1] }}
                </template>
            </Avatar>
            </div>
            <!---------2号位---------->
            <div :class="camp_2_style">
            <Avatar :my_userid="userid" :userid="userids[2]"  @reportUser="handleReport">
                <template #name>
                    <p>{{ name[2] }}</p>
                </template>
                <template #avatar>
                    {{ name[2] }}
                </template>
            </Avatar>
            </div>
            </div>
        </div>
        </div>
    </div>
    <div v-else>
        <div>
            <button @click="Get" class="button">开始回放</button>
        </div>
        <div class="select_btn">
            <el-select v-model="value" filterable placeholder="请输入对局" :loading="loading" popper-class="select_down"
                style="width: 240px">
                <el-option v-for="item in options" :label="item.startTime" :key="item.recordId" :value="item.recordId">
                </el-option>
            </el-select>
        </div>
    </div>
</template>

<style scoped>

.background-image-Record {
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

/* .end_button {
    display: block;
    padding: 10px 10px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    position: absolute;
    left: 50%;
    z-index: 9999;
} */

.next_button {
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    position: relative;
    margin-right: 30px;
    top: 388px;
}

.select_btn {
   position: relative;
}


.button-home:hover {
    background-color: #e0a61b;
}

.brd2{
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
}

.brd1 {
    position: relative;
    z-index: -1;
    width: 1100px;
}

.chessboard-container {
    position: relative;
}


.el-select {
    .el-select__wrapper {
        background-color: bisque !important;
    }
}

.select_down {
    background-color: bisque !important;

    .el-select-dropdown__item:hover {
        background-color: beige;
    }
}
.button-share{
    position: absolute;
    top: 80px;
    right: 20px;
    background-color: #ecb920;
    border: none;
    padding: 10px 20px;
    border-radius: 40px;
    font-size: 18px;
    cursor: pointer;
    z-index: 9999;
}

.button-share:hover{
    background-color: #e0a61b;
}

</style>
