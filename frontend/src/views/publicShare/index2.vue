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
import * as CONST from "@/lib/const.js";

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
const EndGo = () => {
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
const Get = ref(() => {
    console.log(value.value)
    my_camp.value = getCamp(value.value)
    console.log(value.value['recordId'])
    socket.value.io.emit('viewMoveRecords', { 'record_id': value.value['recordId'] })
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
</script>
<template>
            <div v-for="(item,index) in camp_c" :key="index">
                <div :class="item">
                    <Avatar :my_userid="userid" :userid="userids[index]" @reportUser="handleReport">
                        <template #name>
                            <p>{{ name[index] }}</p>
                        </template>
                        <template #avatar>
                            <img :src="main.url+avatars[userids[index]]" alt="头像" />
                        </template>
                    </Avatar>
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

.next_button {
    font-size: 18px;
    font-weight: bold;
    padding: 10px 10px;
    top: 400px;
    left: 540px;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    position: relative;
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

.brd {
    position: absolute;
    top: 5%;
    left: 0%;
    width: 1080px;
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

</style>
