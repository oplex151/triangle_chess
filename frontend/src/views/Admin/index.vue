<script setup lang="ts">
import { onMounted, ref } from 'vue'
import axios from 'axios';
import main from '@/main'
import { useRouter,useRoute } from 'vue-router';
import Cookies from 'js-cookie'
import { ElMessage } from 'element-plus';
import router from '@/router';
import * as CONST from '@/lib/const.js';

const user_data = ref([])
const apeal_table = ref([])
const visable = ref(false)
const appeal_text = ref('')
const appeal_id = ref(-1)
const toid = ref(-1)
const ruleForm = ref({
    feedback: ''
})

onMounted(() => {
    axios.post(main.url+'/api/checkAdmin',
    {
        'token': Cookies.get('admin_token')
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(res => {
        if(res.status == 200){
            ElMessage.success('验证成功')
            getUserData()
            getAppeals()
        }
        else{
            ElMessage.error('验证失败')
            router.push('admin/login')
        }
    }).catch(err => {
        ElMessage.error('验证失败')
        router.push('admin/login')
    })
})



function getUserData() {
    axios.post(main.url+'/api/getUserData',
    {
        'token': Cookies.get('admin_token')
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(res => {
        if(res.status == 200){
            user_data.value = res.data
        }
        else{
            ElMessage.error('获取用户数据失败')
        }
    }).catch(err => {
        //console.log(err)
        ElMessage.error('获取用户数据失败')
    })
}

function getAppeals() {
    axios.post(main.url+'/api/getAppeals',
    {
        'token': Cookies.get('admin_token')
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(res => {
        if(res.status == 200){
            apeal_table.value = res.data
        }
        else{
            ElMessage.error('获取申诉数据失败')
        }
    }).catch(err => {
        //console.log(err)
        if (err.response.status == CONST.NO_APPEALS) {
            ElMessage.info('暂无申诉数据')
        }
        else
            ElMessage.error('获取申诉数据失败')
    })
}

function handleBan(user) {
    //console.log(user)
    axios.post(main.url+'/api/banUser',
    {
        'token': Cookies.get('admin_token'),
        'userid': user.userid
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(res => {
        if(res.status == 200){
            ElMessage.success('封禁成功')
            getUserData()
        }
        else{
            ElMessage.error('封禁失败')
        }
    }).catch(err => {
        //console.log(err)
        ElMessage.error('封禁失败')
    })
}

function handleRelease(user) {
    //console.log(user)
    axios.post(main.url+'/api/releaseUser',
    {
        'token': Cookies.get('admin_token'),
        'userid': user.userid
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(res => {
        if(res.status == 200){
            ElMessage.success('解封成功')
            getUserData()
        }
        else{
            ElMessage.error('解封失败')
        }
    }).catch(err => {
        //console.log(err)
        ElMessage.error('解封失败')
    })
}   

const filterHandler = (value,row) => {
  //console.log(row, value)
  return row.banned == value
}

const filterDealed = (value,row) => {
  //console.log(row, value)
  return row.dealed == value
}

function viewDetail(row) {
    //console.log(row)
    visable.value = true
    appeal_text.value = row.content
    appeal_id.value = row.appealid
    if (row.userid != row.fromid) 
        toid.value = row.userid
}

function handleClose() {
    visable.value = false
    appeal_text.value = ''
    appeal_id.value = -1
    ruleForm.value.feedback = ''
    toid.value = -1
}

function handleSubmit() {
    //console.log(appeal_id.value, ruleForm.value.feedback)
    axios.post(main.url+'/api/handleAppeal',
    {
        'token': Cookies.get('admin_token'),
        'appeal_id': appeal_id.value,
        'feedback': ruleForm.value.feedback
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(res => {
        if(res.status == 200){
            ElMessage.success('处理成功')
            getAppeals()
        }
        else{
            ElMessage.error('处理失败')
        }
    }).catch(err => {
        //console.log(err)
        ElMessage.error('处理失败')
    })
    handleClose()
}

const formatDate = (timestamp) => {
    //console.log(timestamp)
    // 将日期字符串转换为Date对象
    const date = new Date(timestamp);

    // 获取各个部分
    const year = date.getFullYear();
    const month = date.getMonth() + 1; // 月份从0开始，需要加1
    const day = date.getDate();
    const hour = date.getHours();
    const minute = date.getMinutes();
    const second = date.getSeconds();

    // 中文星期数组
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const dayOfWeek = days[date.getDay()];

    // 格式化为中文日期字符串
    const chineseDate = `${year}-${month}-${day} ${dayOfWeek} ${hour}:${minute}:${second}`;

    return chineseDate;
}

</script>

<template>
    <div class="admin-lable">用户信息表</div>
    <el-table :data="user_data">
        <el-table-column prop="userid" label="用户id"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="email" label="邮箱"></el-table-column>
        <el-table-column prop="phone_num" label="手机号"></el-table-column>
        <el-table-column prop="rank" label="段位"></el-table-column>
        <el-table-column prop="score" label="积分"></el-table-column>
        <el-table-column 
        label="账号状态"
        prop="banned"
        :filters="[
            { text: '正常', value: 0 },
            { text: '封禁', value: 1 },
        ]"
        :filter-method="filterHandler"
        >
            <template #default="scope">
                
                <span>{{scope.row.banned ==0 ? '正常' : '封禁'}}</span>
                
            </template>
        </el-table-column  >
        <el-table-column fixed="right" label="Operations" width="120">
        <template #default="scope">
            <el-button v-if="scope.row.banned == 0"
            type="danger" size="small" @click="handleBan(scope.row)">
                封禁
            </el-button>
            <el-button v-if="scope.row.banned == 1"
            type="primary" size="small" @click="handleRelease(scope.row)">
                解封
            </el-button>
            <!-- <el-button link type="primary" size="small">Edit</el-button> -->
        </template>
        </el-table-column>
    </el-table>
    <div class="admin-lable2">消息处理表</div>
    <el-table  :data="apeal_table">
        <el-table-column prop="appealid" label="id"></el-table-column>
        <el-table-column prop="fromid" label="用户id"></el-table-column>
        <el-table-column prop="username" label="用户名"></el-table-column>
        <el-table-column prop="timestamp" label="时间" sortable>
            <template #default="scope">
                {{formatDate(scope.row.timestamp)}}
            </template>
        </el-table-column>
        <el-table-column prop="type" label="申诉类型">
            <template #default="scope">
                <el-tag
                :type="scope.row.type ? 'success' :'danger'">
                     {{scope.row.type ? '申诉' : '举报'}}
                </el-tag>
            </template>
        </el-table-column>
        <el-table-column 
        label="处理状态"
        prop="dealed"
        :filters="[
            { text: '未处理', value: 0 },
            { text: '已处理', value: 1 },
        ]"
        :filter-method="filterDealed"
        >
            <template #default="scope">
                
                <span>{{scope.row.dealed == 0 ? '未处理' : '已处理'}}</span>
                
            </template>
        </el-table-column >
        <el-table-column prop="content" label="申诉内容"
        fixed="right" width="150">
            <template #default="scope">
                <div>
                {{scope.row.content.split(':')[0]}}
                </div>
                <el-button type="text" @click="viewDetail(scope.row)">
                    查看详情
                </el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-dialog 
    v-model="visable" 
    :title="'详情'+ (toid!=-1?': 对uid为$的用户的举报'.replace('$',toid):'')"
    width="500"
    class="report-dialog" 
    :before-close="handleClose">
        <div class="report-content">
            {{appeal_text.split(':')[0]}}:
            {{appeal_text.split(':')[1]}}
        </div>
        <el-input v-model="ruleForm.feedback" 
        placeholder="请输入回复" />
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="handleClose()">取消</el-button>
                <el-button type="primary" @click="handleSubmit()">
                    提交
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<style scoped>
.admin-lable {
    margin-top: 10px;
    background-color: #f6bb4e;
    border-radius: 5px;
    height: 100%;
    width: 100%;
    font-size: 30px;
    display: flex;
    justify-content: center;
    align-items: center;    
}
.admin-lable2 {
    margin-top: 50px;
    background-color: #f6bb4e;
    border-radius: 5px;
    height: 100%;
    width: 100%;
    font-size: 30px;
    display: flex;
    justify-content: center;
    align-items: center;    
}

.report-content {
    margin-top: 20px;
    font-size: 18px;
    line-height: 1.5;
    margin-bottom: 30px;
    border-radius: 10px;
    border-width: 2px;
    padding: 10px;
    border-style: solid;
    border-color: black;
}
</style>