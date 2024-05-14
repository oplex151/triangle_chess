<script setup>
import { onMounted, ref, onUnmounted, computed, getCurrentInstance, onBeforeUnmount, watch } from 'vue';
import { ElMessage } from "element-plus";

import Cookies from 'js-cookie'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import main from '@/main'

import { registerSockets, socket, removeSockets } from '@/sockets'
import Board from '@/views/Game/board.vue'

const start = ref(false)
const options = ref([])
const value = ref('')
const loading = ref(true)
const {proxy} = getCurrentInstance()
const userid = Cookies.get('userid')
let status1 = ''

const StartGo = ()=>{
    start.value = true
    // need get game_record

}
const EndGo = ()=>{
    start.value = false
}
const sockets_methods = {
    gameRecord(data){
        console.log(data.record)
        options.value = data.record[0]
        console.log(options.value)
        loading.value = false
    },
    processWrong(data){
        status1 = data.status
        ElMessage.error("Error due to "+status1)
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
    ElMessage.info(Cookies.get('userid'))
    console.log(socket.value)
    socket.value.io.emit('viewGameRecords',{'userid':userid})
});

onUnmounted(() => {
    removeSockets(sockets_methods, socket.value, proxy);
});
const Get = ref(()=>{
    socket.value.io.emit('viewGameRecords',{'userid':userid})
})
</script>
<template>
    <div class="background-image"></div>
    <div v-if="start">
        <button @click="EndGo">结束回放</button>
        <Board :my_camp="my_camp" ref="board"  @requireMove="Move"/>
    </div>
    <div v-else>
        <el-select
        v-model="value"
        filterable
        placeholder="请输入对局"
        :loading="loading"
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
        <button @click="StartGo">开始回放</button>
        <button @click="Get">Get</button>
        {{value}}
    </div>
</template>
