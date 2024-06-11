<script setup>
import { onMounted, ref, onUnmounted, computed, getCurrentInstance, watch, nextTick } from 'vue';
import { ElMessage } from "element-plus";
import { useRouter,useRoute} from 'vue-router';
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
import useClipboard from 'vue-clipboard3';
import * as CONST from "@/lib/const.js";

const { toClipboard } = useClipboard()
const start = ref(false)
const options = ref([])
const value = ref('')
const loading = ref(true)
const { proxy } = getCurrentInstance()
const router = useRouter()
const route = useRoute()
const userid = Cookies.get('userid')
const moves = ref([])
const my_camp = ref(-1)
const step = ref(0)
const board = ref(null)
const map_state = ref(game_info)

let status1 = ''
const userids = computed(() => {
    let names = []
    for (let i = 0; i < 3; i++) {
        names.push(value.value['p' + (i + 1)])
    }
    return names
})
const name = computed(()=>{
    return userids.value
})
const sockets_methods = {
    gameRecord(data) {
        options.value = data.record[0]
        //console.log(options.value)
        loading.value = false
    },
    gameMoveRecord(data) {
        //console.log(data)
        moves.value = data.record[0]
        loading.value = false
        start.value = true
        //console.log(game_info)
        map_state.value = game_info
        // 使用nextTick等board初始化完成
        nextTick(() => {
            board.value.initMap(map_state.value)
        });

    },
    processWrong(data) {
        status1 = data.status
        ElMessage.error("Error due to " + status1)
        if(status1 == CONST.SESSION_EXPIRED){ //Session expired
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
    },
}

onMounted(() => {
    if (!socket.value) {
        socket.value = new VueSocketIO({
            debug: true,
            connection: SocketIO(main.url),
        })
    }
    registerSockets(sockets_methods, socket.value, proxy);
    //console.log(socket.value)
    my_camp.value = -1
    //console.log(route.query.recordId)
    socket.value.io.emit('viewMoveRecords', { 'record_id': route.query.recordId })
});
function goBackHome() {
    removeSockets(sockets_methods, socket.value, proxy)
    Cookies.remove('room_id')
    Cookies.remove('room_info')
    socket.value.io.disconnect()
    socket.value = null
    router.push('/')
}
onUnmounted(() => {
    try {
        removeSockets(sockets_methods, socket.value, proxy);
        socket.value.io.disconnect()
    }
    catch (err) {
        //console.log("Record Remove Socket Failed!")
        //console.log(err)
    }

});


const Move = (data) => {
    //console.log(data)
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
    //console.log(data)
    step.value += 1
    board.value.moveSuccess(data)
}


const handleReport = (userid) => {
    ElMessage.error('分享模式下，暂不支持举报')
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
        //console.log('Copied to clipboard')
    } catch (e) {
        //console.error(e)
    }
}
const share = () => {
    copy(main.self_url+'/publicShare?recordId='+route.query.recordId)
    ElMessage.success('链接已复制到剪贴板')
}
const camp_c = computed(() => {
    return [camp_0_style.value, camp_1_style.value, camp_2_style.value]
})
const Previous = () =>{
    step.value -= 1
    if(step.value < 0){
        ElMessage.info('已经到第一步')
        step.value = 0
        return
    }
    board.value.WithDraw()
}
</script>
<template>
    <div class="background-image-publicShare"></div>

    <button class="button-home" @click="goBackHome()">
            <el-icon style="vertical-align: middle" size="30px">
                <HomeFilled />
            </el-icon>
        </button>
    <button class="button-share" @click="share">
        <el-icon style="vertical-align: middle" size="30px">
                <Share />
            </el-icon>
    </button>
    <div v-if="start">
            
        <div class="brd">
            <div class="chessboard-overlay"></div>
            <Board :my_camp="my_camp" ref="board" @requireMove="Move" />
            <button @click="Previous" class="next_button">上一步</button>
            <button @click="Next" class="next_button">下一步</button>
            <div class="avatar">
            <!---------0号位---------->
                <div v-for="(item,index) in camp_c" :key="index">
                    <div :class="item">
                        <Avatar :my_userid="userid" :userid="userids[index]" @reportUser="handleReport">
                            <template #name>
                                <p>noname{{index}}</p>
                            </template>
                            <template #avatar>
                                <img :src="main.url+'/static/noname.png'" alt="头像" />
                            </template>
                        </Avatar>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.button {
    display: block;
    margin: 0 auto;
    padding: 10px 10px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    cursor: pointer;
}

.end_button {
    display: block;
    margin: 0 auto;
    padding: 10px 10px;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    cursor: pointer;
}
.chessboard-overlay {
    position: absolute;
    top: 35px;
    left: -42px;
    width: 1080px;
    height: 800px;
    background-image: url('@/assets/images/game/chessBoard.jpg');
    background-size: cover;
    opacity: 1.0; /* Adjust opacity as needed */
    z-index: -1;
}
.board{
    position: absolute;
    top: 700px;
    left: 950px;
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
.background-image-publicShare {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('@/assets/images/login/图1.jpg');
    background-size: cover;
    z-index: -1;
}
.next_button {
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    position: relative;
    margin-right: 30px;
    height: 40px;
    top: 360px;
    left:120px

}

.select_btn {
    position: relative;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: 50%;
    margin-top: 10%;

    transform: translate(-50%, -50%);

}

.button-home {
    position: absolute;
    top: 20px;
    left: 20px;
    background-color: #ecb920;
    border: none;
    padding: 10px 20px;
    border-radius: 40px;
    font-size: 18px;
    cursor: pointer;


    z-index: 9999;
}

.button-home:hover {
    background-color: #e0a61b;
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
    top: 20px;
    right: 20px;
    background-color: #ecb920;
    border: none;
    padding: 10px 20px;
    border-radius: 40px;
    font-size: 18px;
    cursor: pointer;
    z-index: 9999;
}
.brd{
    position: relative;
    top:100px;
    left:100px;

}
</style>
