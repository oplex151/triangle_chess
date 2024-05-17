<script setup>
import { onMounted, ref, onUnmounted, computed, getCurrentInstance, onBeforeUnmount, watch ,nextTick } from 'vue';
import { ElMessage } from "element-plus";
import { useRouter } from 'vue-router';
import Cookies from 'js-cookie'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'
import { User, HomeFilled } from '@element-plus/icons-vue'
import { registerSockets, socket, removeSockets } from '@/sockets'
import Board from '@/views/Game/board.vue'
import game_info from '@/assets/jsons/game_info.json'
const start = ref(false)
const options = ref([])
const value = ref('')
const loading = ref(true)
const {proxy} = getCurrentInstance()
const router = useRouter()
const userid = Cookies.get('userid')
const moves = ref([])
const my_camp = ref(0)
const step = ref(0)
const board = ref(null)
const map_state = ref(game_info)
let status1 = ''


const EndGo = ()=>{
    start.value = false
    moves.value = []
    step.value = 0
}
const sockets_methods = {
    gameRecord(data){
        options.value = data.record[0]
        console.log(options.value)
        loading.value = false
    },
    gameMoveRecord(data){
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
    processWrong(data){
        status1 = data.status
        ElMessage.error("Error due to "+status1)
    },
}
const getCamp = (game_head) => {
    if (game_head.p1 == userid){
        return 0
    }
    else if(game_head.p2 == userid){
        return 1
    }
    else if(game_head.p3 == userid){
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
    socket.value.io.emit('viewGameRecords',{'userid':userid})
});
function goBackHome(){
    removeSockets(sockets_methods, socket.value, proxy)
    Cookies.remove('room_id')
    Cookies.remove('room_info')
    socket.value.io.disconnect()
    socket.value = null
    router.push('/')
}
onUnmounted(() => {
    try{
        removeSockets(sockets_methods, socket.value, proxy);
        socket.value.io.disconnect()
    }
    catch(err){
        console.log("Record Remove Socket Failed!")
        console.log(err)
    }

});
const Get = ref(()=>{
    console.log(value.value)
    my_camp.value = getCamp(options.value[my_camp.value])
    socket.value.io.emit('viewMoveRecords',{'record_id':value.value})
})

const Move = (data)=>{
    console.log(data)
}

const Next = ()=>{
    if (step.value >= moves.value.length){
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
</script>
<template>
    <div class="background-image"></div>
    <button class="button-home" @click="goBackHome()">
            <el-icon style="vertical-align: middle" size="30px">
                <HomeFilled />
            </el-icon>
        </button>
    <div v-if="start">
        <button @click="EndGo" class="end_button">结束回放</button>
        <div class="brd">
            <Board :my_camp="my_camp" ref="board"  @requireMove="Move" />
            <button @click="Next" class="next_button">下一步</button>
        </div>
    </div>
    <div v-else>
        <div class = "select_btn">
        <el-select
        v-model="value"
        filterable
        placeholder="请输入对局"
        :loading="loading"
        popper-class="select_down"
        style="width: 240px"
        >
            <el-option
                v-for="item in options"
                :label="item.startTime"
                :key="item.recordId"
                :value="item.recordId"
            >
            </el-option>
            </el-select>
        </div>
        <div>
            <button @click="Get" class="button">开始回放</button>
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
.end_button{
    position: sticky;
    padding: 10px 10px;
    top: 0%;
    left: 0%;
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
}
.next_button{
    font-size: 18px;
    font-weight: bold;
    padding: 10px 10px;
    top: 400px;
    left: 540px;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    border: none;
    position:relative;
}
.select_btn{
    position: relative;
    justify-content: center;
    align-items: center;
    position: absolute;
    left: 50%;
    margin-top:10%;

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

.brd{
    position: relative;
    top: 30%;
    left:20%;
}
.el-select{
    .el-select__wrapper{
        background-color:bisque !important;
    }
}
.select_down{
    background-color: bisque!important;
    .el-select-dropdown__item:hover{
        background-color: beige;
    }
}

</style>
