<script setup>
import { defineProps, ref } from 'vue';
import { ElInput, ElButton } from 'element-plus';
import {Promotion } from '@element-plus/icons-vue'
const props = defineProps({
    o_message: Array,
});
const emits = defineEmits(['sendMessage']);
const i_message = defineModel('i_message');
const sendMessage = () => {
    if (i_message.value) {
        emits('sendMessage', i_message.value);
        i_message.value = '';
    }
}

</script>

<style>
/* 必须设置下面的属性：
--text-width:190px;
--text-padding-right:10px;
--message-height:500px;
--message-width:10px;
--message-margin-bottom: 10px; */
.custominput {
    max-width: var(--text-width) !important;
    padding-right: var(--text-padding-right) !important;
}

.custominput .el-input__inner {
    /* 背景色 */
    border-color: #dcdfe6;

    /* 边框色 */
    color: #606266;
    /* 文本颜色 */

}

.message .el-button {
    color: white;
    background-color: #ecb920;
    border-radius: 1px;
    border: orange;
    border-width: 1px;
}

.message .el-button:hover {
    background-color: #ffe7b0;
}

.custominput .el-input__inner:focus {
    border-color: #569eee;
    /* 聚焦时边框色 */
}

.custominput .el-input__wrapper {
    width: 20px;
    background-color: beige;
}

.custominput .el-input__count-inner {
    background-color: beige !important;
}

.in-room {
    display: flex;
}

.message {
    margin-left: 20px;
    margin-right: 5px;
    width: 60%;

}

.messageshow {
    border-style:solid;
    border-width: 5px;
    border-color: #ecb920;;
    overflow-y: scroll;
    padding: 10px;
    margin-top: 0px ;
    background-color: rgb(255, 246, 235) !important;
    margin-bottom: 10px;
    margin-bottom: var(--message-margin-bottom) !important;
    overflow-y: auto;
    border-radius: 10px;
    height: 500px;
    height: var(--message-height);
    text-align: left;
}

.messageshow li {
    margin: 0px;
    font-size: 10px !important;
    color: rgb(71, 65, 64);
    color: var(--message-color);
}
</style>

<template>
    
    <div class="message">

        <div class="messageshow">
            <div v-for="(item, index) in props.o_message">
                &nbsp;&nbsp;{{ item.user }}:{{ item.message }}
            </div>
        </div>
        <el-input class="custominput" v-model="i_message" maxlength=40 show-word-limit
            @keyup.enter.native="sendMessage" placeholder="Please input" />
        <el-button @click="sendMessage" style="width: 10px" type="primary">
            <el-icon>
                <Promotion />
            </el-icon>
        </el-button>
    </div>
</template>