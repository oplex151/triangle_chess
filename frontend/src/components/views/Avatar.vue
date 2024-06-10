<script setup>
import { ref, reactive, onMounted } from 'vue'

import axios from 'axios';
import main from '@/main';
import * as CONST from '@/lib/const.js'

import { ElMessage } from 'element-plus';
import { getRankLevel } from '@/config/rank';

const emits = defineEmits(['reportUser','deleteFriend'])
const props = defineProps(['userid', 'my_userid', 'is_friend'])

const reportUser = () => {
    emits('reportUser', props.userid);
}
const isfriend = ref(false)
const user_info = ref({})

//////////////////////////////code for bug////////////////////////
/**
 * 复现方法：找三个人，加到一个房间，然后退一个再加退一个再加，就能看到终端里面一片一片的531报错
 * 
 * 原因：Avatar组件有许多个，有多个人会执行Avatar，会导致getFriends被反复执行
 * 然而代码中游标只有一个
 * 因为axios是异步的，而python也是异步的，所以getFriends的顺序并不是固定的
 * 这会导致单个游标反复执行不同的cursor.exc，进而
 * - 如果游标执行队列过长，会导致游标认为数据库断联而关闭（......），进而后面所有的执行都无法完成，看上去就像后端崩溃一样
 * - 尝试采纳的解决：每次执行的时候重ping一次数据库
 * - 如果游标的执行顺序和数据库的完成顺序不一致，会导致游标取回结果的顺序和执行查询的顺序不一致，出现Packet sequence number wrong
 * - 建议的解决：加锁，保证队列一致。或者把数据库连接放到代码里面
 * p.s.这个并不是最终版本的好友功能，最后可能会用一个新的isFriends api 来代替现在的getFriends.
*/
onMounted (() => {
    ////console.log('mounted')
    if (props.is_friend) {
        isfriend.value = true
    }
    else axios.post(main.url + '/api/getFriends', 
        {
            'userid': props.my_userid
        },
        {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
    ).then(res => {
        if (res.status == 200) {
            ////console.log(res.data)
            for (const id in res.data.friends) {
                let friend = res.data.friends[id]
                if (friend.userid == props.userid) {
                    isfriend.value = true
                    break
                }
            }
        }      
    }).catch(err => {})
    axios.post(main.url + '/api/getRankInfo', {
        'userid': props.userid
    },
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(res => {
        if (res.status == 200) {
            user_info.value = res.data
        }
    }).catch(err => {})
})
//////////////////////////////////end////////////////////
const addFriend = () => {

    ////console.log('add friend')
    if (props.userid == props.my_userid) {
        ElMessage.error('不能添加自己为好友')
        return
    }
    axios.post(main.url + '/api/addFriend', {
        'userid': props.my_userid,
        'friend_id': props.userid
    },
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    ).then(res => {
        if (res.status == 200) {
            ////console.log(res.data)
            ElMessage.success('好友信息已发送')
        } else {
            ////console.log('error')
            ElMessage.error('添加好友失败')
        }
    }).catch(err => {
        if (err.response.status == CONST.ALREADY_FRIEND) {
            ElMessage.error('已经是好友了')
            isfriend.value = true
            return
        }
        ////console.log(err)
        ElMessage.error('添加好友失败')
    })
}
const deleteFriend = () => {
    //console.log('delete friend')
    axios.post(main.url + '/api/deleteFriend', {
        'userid': props.my_userid,
        'friend_id': props.userid
    },
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    ).then(res => {
        if (res.status == 200) {
            ////console.log(res.data)
            ElMessage.success('删除好友成功')
            isfriend.value = false
        
        } else {
            ////console.log('error')
            ElMessage.error('删除好友失败')
        }
    }).catch(err => {
        //console.log(err)
        if (err.response.status == CONST.NOT_FRIEND) {
            ElMessage.error('已经不是好友了')
            isfriend.value = false
        }
        else
            ElMessage.error('删除好友失败')
    })
    emits('deleteFriend', props.userid)
}   
</script>

<template>
    <el-popover :width="200" class="avatar-popover">
        <template #reference>
            <el-avatar :size="50">
                <template v-slot>
                    <slot name="avatar"></slot>
                </template>
            </el-avatar>
        </template>
        <template #default>
            <div class="rich-conent">
                <el-avatar :size="50">
                    <template v-slot class='user-name'>
                        <slot name="avatar"></slot>
                    </template>
                </el-avatar>
                <p class="name" style="margin: 0; font-weight: 500">
                    <slot name="name">User</slot>
                </p>
                <div v-if="user_info" class="user-info-table">
                    <div class="'user-info'">
                        段位:{{getRankLevel(user_info.rank)}}
                    </div>
                    <div class="'user-info'">
                        积分:{{user_info.score}}
                    </div>
                </div>
                <p>
                    <el-button v-if="props.userid != props.my_userid" class="login-button"
                        style="background-color: bisque;" size="" @click="reportUser">
                        举报
                    </el-button>
                    <div>
                        <div v-if="!isfriend">
                            <el-button v-if="props.userid != props.my_userid" class="login-button" style="background-color: bisque;" size="mini" @click="addFriend">
                                加好友
                            </el-button>
                        </div>
                        <div v-else>
                            <el-button class="login-button" style="background-color: bisque;" size="mini" @click="deleteFriend">
                                删除好友
                            </el-button>
                        </div>
                    </div>
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
    /* 增加垂直内边距 */
    margin: auto;
    cursor: pointer;
    font-size: 15px;
    margin: 5px;
    width: 70px;
}

.el-popover {
    background-color: #f6bb4ed1 !important;
    text-align: center;
}

.el-avatar {
    border: 2px solid #895e0f;
}

.user-name{
    font-size: 18px;
    color: #895e0f;
    font-weight: 500;
}

.name{
    position: relative;
    left:50px;
    bottom: 30px;
}

.user-info-table {
    display: inline-flex;
    flex-direction: column;
}

.user-info {
    display: inline-block;
    font-size: 14px;
}


</style>