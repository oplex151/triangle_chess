<script setup>
import { ref, onMounted } from 'vue'
import main from '@/main.js'
import Cookies from 'js-cookie'
import axios from 'axios'



const user_apeals = ref([])
const visable = ref(false)
const text = ref('')

onMounted(() => {
    getUserAppeal()
})

function getUserAppeal() {
    axios.post(main.url + '/api/getUserAppeal', 
    {
        'userid': Cookies.get('userid')
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }).then(response => {
        if (response.status ==200) {
            console.log(response.data)
            user_apeals.value = response.data
        }
        else{
            ElMessage.error('Error getting user appeals')
        }
    }).catch(error => {
        console.log(error)
        ElMessage.error('Error getting user appeals')
    })
}
const formatDate = (timestamp) => {
    console.log(timestamp)
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

const formatReport = (row) => {
    if (row.userid!= row.fromid )
        return row.userid
    else 
        return '无'
}

function viewDetail(content) {
    visable.value = true
    text.value = content
}

function closeDetail() {
    visable.value = false
    text.value = ''
}

</script>

<template>
    <el-table :data="user_apeals" style="width: 100%">
        <el-table-column prop="timestamp" label="时间" sortable>
            <template #default="scope"> 
                {{ formatDate(scope.row.timestamp) }}
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
        <el-table-column prop="title" label="举报对象">
            <template #default="scope"> 
                {{ formatReport(scope.row)}}
            </template>
        </el-table-column>
        <el-table-column prop="feedback" label="回复">
            <template #default="scope">
                <el-button 
                v-if="scope.row.dealed"
                type="text" @click="viewDetail(scope.row.feedback)">
                    查看详情
                </el-button>
            </template>
        </el-table-column>
        <el-table-column prop="content" label="举报内容">
            <template #default="scope">
                <div>
                {{scope.row.content.split(':')[0]}}
                </div>
                <el-button type="text" @click="viewDetail(scope.row.content)">
                    查看详情
                </el-button>
            </template>
        </el-table-column>

    </el-table>
    <el-dialog 
    v-model="visable" 
    title='详情'
    width="500"
    class="report-dialog" >
        <div class="report-content">
            {{text}}
        </div>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="closeDetail()">ok</el-button>
            </div>
        </template>
    </el-dialog>
</template>

<style>
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