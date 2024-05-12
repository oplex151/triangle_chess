<script setup>
import { ElMessage } from 'element-plus';
import { ref, onMounted, onUnmounted } from 'vue'
const props = defineProps(['camp'])
const emit = defineEmits(['let_go'])
const p = ref(1)
const createRoom = () => {
    emit('let_go','jump','gogogo')
}
function go_to(){
    p.value = p.value + 1
    ElMessage.success('go_to'+p.value)
}
defineExpose({
    p,
    go_to
})
</script>

<template>
    <el-button type="primary" @click="createRoom">往父组件传递消息</el-button>
</template>