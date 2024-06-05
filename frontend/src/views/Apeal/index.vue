<template>
    <div class="apeal-body">
    <el-form 
    :model="ruleForm" 
    :rules="rules" 
    ref="ruleFormRef"
    :size="formSize"
    >
        <el-form-item label="申诉理由" prop="reason">
            <el-radio-group v-model="ruleForm.reason">
                <el-radio value="Apeal_bad_report">恶意举报</el-radio>
                <el-radio value="Bad_bug">遭遇bug</el-radio>
                <el-radio value="Ask_help">请求帮助</el-radio>
                <el-radio value="Other">其他</el-radio>
            </el-radio-group>
        </el-form-item>
        <el-form-item label="详细原因" prop="detail">
                <el-input v-model="ruleForm.detail" />
        </el-form-item>
    </el-form>
    <div class="dialog-footer">
        <el-button @click="handleClose">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit(ruleFormRef)">
            Confirm
        </el-button>
    </div>
    </div>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits, ref ,reactive, computed } from 'vue'
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import axios from 'axios';
import main from '@/main';
import Cookies from "js-cookie";
import router from '@/router';
const formSize = ref<ComponentSize>('default')

const props = defineProps({
    myuserid: Number
})
const emit = defineEmits(['reportEnd','reportStop'])

interface RuleForm {
    reason: string
    detail: string
}
const ruleFormRef = ref < FormInstance >()
const ruleForm = reactive < RuleForm > ({
    reason: '',
    detail: '',
})

const rules = reactive < FormRules < RuleForm >> ({
    reason: [
        { required: true, message: '请选择原因', trigger: 'blur' },
    ],
    detail: [
        { required: true, message: '请输入详细描述', trigger: 'blur'}
    ]
})

const Confirm = () => {
    axios.post(main.url+ '/api/addAppeals', {
        'userid':props.myuserid,
        'type': 1,  //apeal
        'content':ruleForm.reason +':'+ruleForm.detail,
        'fromid':props.myuserid
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }
    ).then(res => {
    if (res.status == 200) {
        ElMessage.success("发送成功")
    } 
    else {
        ElMessage.success('发送出错,反正是发过去了')
        //console.log(res)
    }
    })
    .catch(error => {
        ElMessage.error('发送出错')
        //console.log(error.response.status)
        if(error.response.status == 550){ //Session expired
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
    resetForm(ruleFormRef.value)  
    emit('reportEnd')
}
const handleSubmit = (ruleFormRef : FormInstance |undefined) => {
    if (!ruleFormRef) return
    ruleFormRef.validate((valid,fields) => {
        if (valid) {
            Confirm()
        } else {
            return false
        }
    })
}
const resetForm = (ruleFormRef : FormInstance |undefined) => {
    if (!ruleFormRef) return
    ruleFormRef.resetFields()
}
const handleClose = (done: () => void) => {
    resetForm(ruleFormRef.value)  
    emit('reportEnd')
}
</script>

<style scoped>
.apeal-body {
    padding: 20px;
    min-height: 300px;
}
.dialog-footer {
    margin-top: 20px;
    position: absolute;
    left: 50%;
    bottom: 70px;
}
</style>