<script setup>
import { ref } from 'vue'
import Avatar from './Avatar.vue';
import Cookies from 'js-cookie';
import * as CONST from '@/lib/const.js'

import axios from 'axios'
import main from '@/main'
import { ElMessage } from 'element-plus';
import Report from './Report.vue';
const innerDrawer = ref(false)
const outerDrawer = ref(false)
const userid = Cookies.get('userid')

const Friendlist = ref([])
const UnconfirmedFriendlist = ref([])
const AvatarList = ref([])
const handlevis = ref(false)
const to_report_id = ref(0)
const  getFriendList = () => {
    getConfirmedFriendList()
    getUnconfirmedFriendList()

}
const getConfirmedFriendList = () => {
    
    axios.post(main.url+'/api/getFriends', {
        userid: userid
    },{
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(res => {
        Friendlist.value = res.data.friends
    }).catch(err => {
        console.log(err)
        ElMessage.error('获取好友列表失败')
        // if(err.response.status == CONST.SESSION_EXPIRED){ //Session expired
        // Cookies.remove('room_id')
        // Cookies.remove('userid')
        // Cookies.remove('room_info')
        // Cookies.remove('username')
        // Cookies.remove('camp')
        // ElMessage({
        //     message: '会话过期，请重新登录',
        //     grouping: true,
        //     type: 'error',
        //     showClose: true
        // })
        //     router.replace('/login')
        // }
    })
}
const getUnconfirmedFriendList = () => {
    axios.post(main.url+'/api/getFriends', {
        'userid': userid,
        'confirm': 0
    },{
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(res => {
        UnconfirmedFriendlist.value = res.data.friends
    }).catch(err => {
        console.log(err)
        ElMessage.error('获取列表失败')
        // if(err.response.status == CONST.SESSION_EXPIRED){ //Session expired
        // Cookies.remove('room_id')
        // Cookies.remove('userid')
        // Cookies.remove('room_info')
        // Cookies.remove('username')
        // Cookies.remove('camp')
        // ElMessage({
        //     message: '会话过期，请重新登录',
        //     grouping: true,
        //     type: 'error',
        //     showClose: true
        // })
        //     router.replace('/login')
        // }
    })
}
const getAvatars = () =>{
    console.log(UnconfirmedFriendlist.value)
    let confuserids = Friendlist.value.map(user => {
        return user.userid;
    }) 
    let unuserids = UnconfirmedFriendlist.value.map(user => {
        return user.userid;
    })
    let joinuserids = confuserids.concat(unuserids)
    joinuserids.push(userid)
    axios.post(main.url+'/api/getAvatars', {
        'userids': joinuserids.join(',')
    },{
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(res => {
        console.log(res.data)
        AvatarList.value = res.data
    }).catch(err => {
        console.log(err)
        ElMessage.error('获取头像列表失败')
    })
}
const confirmFriend = (friendid, confirm) => {
    console.log(confirm)
    console.log(friendid)
    axios.post(main.url+'/api/confirmFriend', {
        'userid': userid,
        'friend_id': friendid,
        'confirm': confirm
    },{
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(res => {
        if (res.status == 200) {
            // getFriendList()
            ElMessage.success('操作成功')
            if (confirm == 1) {
                Friendlist.value.push(UnconfirmedFriendlist.value.filter(friend => friend.userid == friendid)[0])
            }
            UnconfirmedFriendlist.value = UnconfirmedFriendlist.value.filter(friend => friend.userid != friendid)
            
        } else {
            ElMessage.error('操作失败')
        }
    }).catch(err => {
        console.log(err)
        ElMessage.error('操作失败')
    })
}

const deleteFriend = (friendid) => {
    console.log('delete friend')
    axios.post(main.url + '/api/deleteFriend', {
        'userid': userid,
        'friend_id': friendid
    },
    {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }
    ).then(res => {
        if (res.status == 200) {
            ElMessage.success('删除好友成功')
            isfriend.value = false
            Friendlist.value = Friendlist.value.filter(friend => friend.userid != friendid)
        } else {
            ElMessage.error('删除好友失败')
        }
    }).catch(err => {
        console.log(err)
        if (err.response.status == CONST.NOT_FRIEND) {
            ElMessage.error('已经不是好友了')
            Friendlist.value = Friendlist.value.filter(friend => friend.userid != friendid)
        }
        else
            ElMessage.error('删除好友失败')
    })
}  
const removeFriend = (friendid) => {
    Friendlist.value = Friendlist.value.filter(friend => friend.userid != friendid)
}

const handleReportEnd = () => {
    handlevis.value = false;
}
const handleReport = (id) => {
    to_report_id.value = id;
    handlevis.value = true;
}
</script>


<template>
<Report :toreportid=to_report_id :myuserid="Cookies.get('userid')" :dialogFormVisible=handlevis @reportEnd="handleReportEnd" />

<button @click="outerDrawer = true" class="friend-drawer-start-btn">好友</button>
<el-drawer class ="friend-drawer-body" v-model="outerDrawer" title="好友列表" :append-to-body="true" @open="getFriendList" @opened="getAvatars" size="18%">
    <div class="friend-drawer-header"><button class="friend-drawer-btn" @click="innerDrawer = true">好友确认消息</button></div>
    
    <el-drawer class="friend-drawer-body" v-model="innerDrawer" append-to-body="true" title="好友确认消息" @open="getUnconfirmedFriendList" @close="getConfirmedFriendList" size = "18%">
        <div v-for="(friend, index) in UnconfirmedFriendlist" :key="friend.userid" :index="index" class="friend-item">
            <!-- <el-avatar :size="40" :src="friend.avatar">
                <img :src="main.url+AvatarList[friend.userid]" alt="头像" />
            </el-avatar> -->
            <Avatar>
            <template #name>
                <p>{{friend.username}}</p>
                </template>
                <template #avatar>
                    <img :src="main.url+AvatarList[friend.userid]" alt="头像" />
                </template>
        </Avatar>
            <span class="friend-item-name">{{friend.username}}</span>
            <button class ="friend-item-btn" @click="confirmFriend(friend.userid, 1)">确认</button>
            <button class ="friend-item-btn" @click="confirmFriend(friend.userid, 0)">拒绝</button>
        </div>
    </el-drawer>


    <div v-for="(friend, index) in Friendlist" :key="friend.userid" :index="index" class="friend-item">
        <!-- <el-avatar :size="40" :src="friend.avatar">
            <img :src="main.url+AvatarList[friend.userid]" alt="头像" />
        </el-avatar> -->
        <Avatar :my_userid="userid" :userid=friend.userid 
            @reportUser="handleReport" @deleteFriend="removeFriend" 
            class="avas">
            <template #name>
            <p>{{friend.username}}</p>
            </template>
            <template #avatar>
                <img :src="main.url+AvatarList[friend.userid]" alt="头像" />
            </template>
        </Avatar>
        <span class="friend-item-name">{{friend.username}}</span>
        <button class="friend-item-btn" style="right:-15%" @click="deleteFriend(friend.userid)">删除好友</button>
    </div>
</el-drawer>
</template>


<style>
.friend-drawer-start-btn{
    background-color: #dda641;
    color: white;
    border: none;
    border-radius: 5px;
    width: 80px;
    padding: 10px;

    font-size: 16px;

}
.friend-item {
    display: flex;
    align-items: center;
    margin: 10px;
}
.friend-item-name{
    margin-left: 10px;
    min-width: 30px;
    font-size: 14px;
    margin-right: 20px;
}
.friend-drawer-body{
    background-color: #0000007d !important;
    min-width: 300px;

    .el-drawer__body{
        background-color: rgba(253, 185, 37, 0.777) ;
    }
    .el-drawer__header {
        background-color: rgba(253, 185, 37, 0.777) ;
        margin-bottom: 0px!important;
    }
}
.friend-drawer-header{
    width: 100%;
    height: 50px;
    display: flex;
    justify-content: center;
    align-items: center;
}
.friend-drawer-btn{
    background-color: #dda641;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    width: auto;
    margin-right: 10px;
    font-size: 16px;
    position: relative;
}
.friend-item-btn{
    background-color: #acef39;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    width: auto;
    margin-right: 10px;
    font-size: 16px;
    position: relative;    
}
</style>