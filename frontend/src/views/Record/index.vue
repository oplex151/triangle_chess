<script setup>
import { onMounted, ref, onUnmounted, computed, getCurrentInstance, onBeforeUnmount, watch, nextTick } from 'vue';
import { ElMessage } from "element-plus";
import { useRouter } from 'vue-router';
import Cookies from 'js-cookie'
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
import axios from 'axios';
import main from '@/main';
import { Share,Star ,StarFilled} from '@element-plus/icons-vue'
import { registerSockets, socket, removeSockets } from '@/sockets'
import Board from '@/views/Game/board.vue'
import game_info from '@/assets/jsons/game_info.json'
import Report from '@/components/views/Report.vue'
import Avatar from '@/components/views/Avatar.vue'
import * as CONST from '@/lib/const.js'

const start = ref(false)
const options = ref([])
const record_id = ref(-1)
const loading = ref(true)
const { proxy } = getCurrentInstance()
const router = useRouter()
const userid = Cookies.get('userid')
const moves = ref([])
const my_camp = ref(-1)
const step = ref(0)
const board = ref(null)
const map_state = ref(game_info)
import useClipboard from 'vue-clipboard3';

const { toClipboard } = useClipboard()

let status1 = ''

const record_content = computed(() => {
  for (let item=0 ; item < options.value.length; item++){
    if(options.value[item]['recordId']==record_id.value){
      return options.value[item]
    }
  }
  return ''
})

const userids = computed(()=>{
  let names = [-1,-1,-1]
  names[0] = record_content.value['p1']
  names[1] = record_content.value['p2']
  names[2] = record_content.value['p3']
  return names
})

const avatars = ref({})
const name = computed(()=>{
    return userids.value
})
const EndGo = () => {
    //console.log('EndGo')
    start.value = false
    moves.value = []
    step.value = 0
    my_camp.value = -1
    record_id.value = -1
}
const sockets_methods = {
    gameRecord(data) {
        // options.value = data.record[0]
        // //console.log(options.value)
        // loading.value = false
        options.value = data.record.map(record => ({
          ...record,
          liked: false // 初始化 liked 属性为 false
        }))
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
        axios.post(main.url + '/api/getAvatars', {'userids': userids.value.join(',')},
        {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        }
        )
        .then(res => {
            //console.log(res.data)
            avatars.value = res.data
        })
        .catch(err => {
            //console.error(err)
            if(err.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
        })

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
    //console.log(socket.value)
    socket.value.io.emit('viewGameRecords', { 'userid': userid })
});
// function goBackHome() {
//     removeSockets(sockets_methods, socket.value, proxy)
//     socket.value.io.disconnect()
//     socket.value = null
//     router.push('/')
// }
onUnmounted(() => {
    try {
        removeSockets(sockets_methods, socket.value, proxy);
        socket.value.io.disconnect()
        socket.value = null
        //console.log("Record Remove Socket Success!")
    }
    catch (err) {
        //console.log("Record Remove Socket Failed!")
        //console.log(err)
    }

});
const Get = ref(() => {
    if (record_id.value == -1)
        return
    // //console.log(record_id.value)
    my_camp.value = getCamp(record_id.value)
    // //console.log(record_id.value['recordId'])
    socket.value.io.emit('viewMoveRecords', { 'record_id': record_id.value})
})

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
const Previous = () =>{
  step.value -= 1
  if(step.value < 0){
    ElMessage.info('已经到第一步')
    step.value = 0
    return
  }
  board.value.WithDraw()
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
const copy = async (anything) => {
  try {
    await toClipboard(anything)
    //console.log('Copied to clipboard')
  } catch (e) {
    //console.error(e)
  }
}
const share = () => {
    if(record_id.value){
        copy(main.self_url+'/publicShare?recordId='+record_id.value)
        ElMessage.success('链接已复制到剪贴板')
    }

}
const camp_c = computed(() => {
    return [camp_0_style.value, camp_1_style.value, camp_2_style.value]
})

const view_comments_record_id = ref(-1)
const comment_content = ref({name:""})
const comments = ref([])
const comments_dialog = ref(false)

// 点赞
function likeGameRecord(row) {
  row.liked = true;
  //console.log("当前的记录id为：" + row.recordId);
  axios.post(main.url+'/api/likeGameRecord',
      { 'recordid': row.recordId },
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(response => {
    ElMessage.success('点赞成功');
    row.likeNum += 1; // 更新点赞数
  }).catch(error => {
    ElMessage.error('点赞失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}

function unlikeGameRecord(row) {
  row.liked = false;
  //console.log("当前的记录id为：" + row.recordId);
  axios.post(main.url+'/api/unlikeGameRecord',
      { 'recordid': row.recordId },
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(response => {
    ElMessage.success('取消点赞');
    row.likeNum -= 1; // 更新点赞数
  }).catch(error => {
    ElMessage.error('取消点赞失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}

function likeComment(row){
  row.comment_liked = true;
  //console.log("当前的记录id为：" + row.commentId);
  axios.post(main.url+'/api/likeComment',
      { 'commentid': row.commentId },
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(response => {
    ElMessage.success('点赞成功');
    row.likeNum += 1; // 更新点赞数
  }).catch(error => {
    ElMessage.error('点赞失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}

function unlikeComment(row){
  row.comment_liked = false;
  //console.log("当前的记录id为：" + row.commentId);
  axios.post(main.url+'/api/unlikeComment',
      { 'commentid': row.commentId },
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(response => {
    ElMessage.success('取消点赞');
    row.likeNum -= 1; // 更新点赞数
  }).catch(error => {
    ElMessage.error('取消点赞失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}


function addComments(content) {
  axios.post(main.url+'/api/addComment',
      { 'recordid': view_comments_record_id.value,"userid": userid,"content":content},
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(response => {
    if (response.status === 200) {
      ElMessage.success('评论成功');
      options.value.find(item => item.recordId === view_comments_record_id.value).commentNum += 1; // 更新评论数
      comment_content.value.name = '';
      viewComments(view_comments_record_id.value);
    }
    else
      ElMessage.error('评论失败');
  }).catch(error => {
    ElMessage.error('评论失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}



function viewComments(record_id){
  axios.post(main.url+'/api/viewRecordComments',
      { 'recordid': record_id},
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(res => {
    //console.log(res.data)
    view_comments_record_id.value = record_id
    comments_dialog.value = true
    comments.value = res.data.map(comment => ({
      ...comment,
      comment_liked: false // 初始化 liked 属性为 false
    }))
  }).catch(error => {
    ElMessage.error('查看失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}

const handleRowClick = (row) => {
  if (record_id.value == row.recordId) {
    record_id.value = -1;
  } else {
    record_id.value = row.recordId;
  }
};

function rowStyle ({row, rowIndex}) {
  if (record_id.value == row.recordId) {
    // 此处返回选中行的样式对象，按需设置
    return {
      'background-color': 'rgb(94, 180, 251)',
      'color': 'rgb(0, 0, 0)'
    }
  }
}

function formatDate(date1) {
  let date = new Date(date1);
  let year = date.getFullYear();
  let month = date.getMonth() + 1;
  let day = date.getDate();
  let hour = date.getHours();
  let minute = date.getMinutes();
  let second = date.getSeconds();
  return year + '-' + month + '-' + day +'  ' + hour + ':' + minute + ':' + second;
}

function changeVisible(record_id, visible) {
  axios.post(main.url+'/api/changeVisible',
      { 'record_id': record_id, 'visible': visible },
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
  ).then(response => {
    if (response.status == 200) {
      options.value.find(item => item.recordId === record_id).visible = visible; // 更新评论数
    }
    else
      ElMessage.error('修改失败');
  }).catch(error => {
    ElMessage.error('修改失败');
    //console.error(error);
    if(error.response.status == CONST.SESSION_EXPIRED){ //Session expired
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
  });
}

</script>
<template>
    <Report :toreportid="to_report_id" :myuserid="userid" :dialogFormVisible=vis @reportEnd="handleReportEnd" />
    <div class="container">
        <div class="background-image-Record"></div>
        <div v-if="start" class="record-container">
            <button class="button-share" @click="share">
                <el-icon style="vertical-align: middle" size="30px">
                        <Share />
                    </el-icon>
            </button>
            <button @click="EndGo" class="end-button">结束回放</button>   
            <div class="brd2">     
              <div class="brd1">
                  <div class="chessboard-overlay"></div>
                  <div class="chessboard-container">
                  <Board :my_camp="my_camp" ref="board" :game_status="CONST.STATUS_ONING" @requireMove="Move" />
                  </div>
                  <button @click="Previous" class="next_button">上一步</button>
                  <button @click="Next" class="next_button">下一步</button>
                  <div class="avatar">
                  <!---------0号位---------->
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
                  </div>
              </div>
            </div>
        </div>
        <div v-else>
          <el-dialog v-model="comments_dialog" title="评论" width="800">
            <el-table :data="comments" max-height="400" >
              <el-table-column property="userId" label="用户ID" width="150" />
              <el-table-column property="content" label="评论内容" width="200" />
              <el-table-column prop="likeNum" label="点赞" >
                <!-- Like button within the table column -->
                <!-- 在表格列中添加点赞按钮 -->
                <template #default="secondscope">
                  <el-button v-if="secondscope.row.comment_liked == false" type="text" @click="likeComment(secondscope.row)">
                    <el-icon size="40px" color="black">
                      <Star style="font-size: 25px; color: black;" />
                    </el-icon>
                  </el-button>
                  <el-button v-if="secondscope.row.comment_liked == true" type="text" @click="unlikeComment(secondscope.row)">
                    <el-icon size="40px" color="black">
                      <StarFilled style="font-size: 25px; color: black;" />
                    </el-icon>
                  </el-button>
                  <div style="padding-left: 30px">{{ secondscope.row.likeNum }}</div>
                </template>
              </el-table-column>
              <el-table-column property="commentTime" label="评论时间" width="200" sortable>
                <template #default="secondscope">{{formatDate(secondscope.row.commentTime)}}</template>
              </el-table-column>
            </el-table>
            <el-form :model="comment_content">
              <el-form-item label="发表评论" label-width=140px>
                <el-input v-model="comment_content.name" autocomplete="off" />
              </el-form-item>
            </el-form>
            <template #footer>
              <div class="dialog-footer">
                <el-button @click="comments_dialog = false">关闭</el-button>
                <el-button type="primary" @click="addComments(comment_content.name)">
                  添加评论
                </el-button>
              </div>
            </template>
          </el-dialog>
          <div>
              <button @click="Get" class="start-button">开始回放</button>
          </div>
            <div class="record-table">
              <el-table :data="options" style="width: 100%; border-radius: 7px; padding: 10px; top: -50px; height: 550px;">
                <el-table-column prop="startTime" label="开始时间"  sortable>
                  <template #default="scope">{{formatDate(scope.row.startTime)}}</template>
                </el-table-column>
                <el-table-column prop="endTime" label="结束时间" >
                  <template #default="scope">{{formatDate(scope.row.endTime)}}</template>
                </el-table-column>
                <el-table-column prop="likeNum" label="点赞" >
                  <!-- Like button within the table column -->
                  <!-- 在表格列中添加点赞按钮 -->
                  <template #default="scope">
                    <el-button v-if="scope.row.liked == false" type="text" @click="likeGameRecord(scope.row)">
                      <el-icon size="40px" color="black">
                        <Star style="font-size: 25px; color: black;" />
                      </el-icon>
                    </el-button>
                    <el-button v-if="scope.row.liked == true" type="text" @click="unlikeGameRecord(scope.row)">
                      <el-icon size="40px" color="black">
                        <StarFilled style="font-size: 25px; color: black;" />
                      </el-icon>
                    </el-button>
                    <div style="padding-left: 30px">{{ scope.row.likeNum }}</div>
                  </template>
                </el-table-column>
                <el-table-column prop="comment" label="评论" >
                  <template #default="firstscope">
                    <el-button type="text">
                      {{ firstscope.row.commentNum }}
                    </el-button>
<!--                    这里加入展示评论的窗口-->
                    <el-button type="text" @click="viewComments(firstscope.row.recordId)" >
                      查看评论
                    </el-button>

                  </template>
                </el-table-column >
                <el-table-column prop="visible" label="对其他人可见">
                  <template #default="scope">
                    <el-button type="text" @click="changeVisible(scope.row.recordId, scope.row.visible==1?0:1)">
                      {{ scope.row.visible==1?'公开':'私密' }}
                    </el-button>
                  </template>
                </el-table-column>
                <el-table-column prop="record_id" label="选择"
                fixed="right">
                  <template #default="scope">
                    <el-button 
                    :type= "record_id==scope.row.recordId ? 'success' : 'primary'"
                    @click="handleRowClick(scope.row)">
                      {{record_id!=scope.row.recordId ?'选择':'取消'}}
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
        </div>
    </div>
</template>

<style scoped>

/* .background-image-Record {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('@/assets/images/login/图1.jpg');
    background-size: cover;
    z-index: -1;
} */

.container{
    width : 100%;
}


.start-button {
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    position: absolute;
    border: none;
    padding: 10px;
    display: inline-block;
    top: 90px;
    left:50%;
}

.start-button:hover {
    background-color: #d29a19;
}


.record-container{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.7);
    z-index: 1888;
}

.chessboard-overlay {
    position: absolute;
    top: 35px;
    left: -42px;
    width: 1280 * 1.01px;
    height: 800 * 1.01px;
    background-image: url('@/assets/images/game/chessBoard.jpg');
    background-size: cover;
    opacity: 1.0; /* Adjust opacity as needed */
    z-index: -1;
}

.end-button {
    font-size: 18px;
    font-weight: bold;
    color: #fff;
    background-color: #ecb920;
    border-radius: 10px;
    position: relative;
    border: none;
    padding: 10px;
    right: 30%;
    top: 5%;
    z-index: 9999;
}

.end-button:hover {
    background-color: #d29a19;
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
    top: 360px;
}

.next_button:hover {
    background-color: #e0a61b;
}

.select_btn {
   position: relative;
}


.button-home:hover {
    background-color: #e0a61b;
}

.brd2{
    top: 50px;
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
}

.brd1 {
    position: relative;
    z-index: -1;
    width: 1100px;
}

.chessboard-container {
    position: relative;
}

.button-share{
    position: relative;
    top:5%;
    left: 50%;
    background-color: #ecb920;
    border: none;
    padding: 10px 20px;
    border-radius: 40px;
    font-size: 18px;
    cursor: pointer;
    z-index: 9999;
}

.button-share:hover{
    background-color: #e0a61b;
}

.end-record-button{
  position: relative; /* 确保按钮处于正常的层级 */
  z-index: 1000; /* 提高按钮的层级 */
}

.record-table {
  margin-top: 20px;
}

.selected-row {
  background-color: rgb(94, 180, 251) !important;
  color: rgb(0, 0, 0) !important;
}

</style>
