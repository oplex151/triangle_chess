<script setup>
import { ref, reactive ,defineEmits,defineProps} from 'vue'

const emits = defineEmits(['reportUser'])
const props = defineProps(['userid','my_userid'])
// {/* <el-button class="login-button"  size="mini">
//             加好友
// </el-button> */}
const reportUser = () => {
    emits('reportUser',props.userid);
}
</script>

<template>
<el-popover :width="300" class = "avatar-popover">
    <template #reference>
    <el-avatar>
        <template v-slot>
        <slot name="avatar"></slot>
        </template>
    </el-avatar>
    </template>

    <template #default>
    <div class="rich-conent">
    <el-avatar>
        <template v-slot>
        <slot name="avatar"></slot>
        </template>
    </el-avatar>

    <div>
        <p class="name" style="margin: 0; font-weight: 500">
            <slot name="name">User</slot>
        </p>
        </div>
        <p>
        <el-button v-if="props.userid!= props.my_userid" class="login-button" style="background-color: bisque;" size="small" @click="reportUser">
            举报
        </el-button>

        </p>
    </div>
    </template>
    </el-popover>

</template>
<style>
.login-button {
    justify-content: center;
    background-color: #f6bb4e;
    color: #fff;
    border: none;
    border-radius: 15px;
    padding: 15px 0; /* 增加垂直内边距 */
    margin: auto;
    cursor: pointer;
    font-size: 15px;
}
.el-popover {
    background-color: #f6bb4e5d!important;
    text-align: center;
}
.el-avatar {

    border:2px solid #895e0f;
}
</style>