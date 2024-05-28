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

onMounted(() => {
    if (!socket.value) {
        socket.value = new VueSocketIO({
            debug: true,
            connection: SocketIO(main.url),
        })
    }
    registerSockets(sockets_methods, socket.value, proxy);
    console.log(socket.value)
    my_camp.value = -1
    console.log(route.query.recordId)
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
        console.log("Record Remove Socket Failed!")
        console.log(err)
    }

});


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
        console.log('Copied to clipboard')
    } catch (e) {
        console.error(e)
    }
}
const share = () => {
    copy(main.self_url+'/publicShare?recordId='+route.query.recordId)
    ElMessage.success('链接已复制到剪贴板')
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
                <Avatar :my_userid="userid" :userid="userids[2]"  @reportUser="handleReport" >
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
    width: 1000px;
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
    padding: 10px 10px;
    top: 400px;
    left: 100px;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    position: absolute;
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
