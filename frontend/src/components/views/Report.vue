<template>
    <el-dialog 
    v-model="props.dialogFormVisible" 
    title="举报" 
    width="500" 
    class="report-dialog" 
    :before-close="handleClose"
    >
        <el-form 
        :model="ruleForm" 
        :rules="rules" 
        ref="ruleFormRef"
        :size="formSize"
        >
            <el-form-item label="举报理由" prop="reason">
                <el-radio-group v-model="ruleForm.reason">
                    <el-radio value="Bad_content">违规发言</el-radio>
                    <el-radio value="Bad_behaviour">恶意行为</el-radio>
                    <el-radio value="Bad_selfie">违规头像或信息</el-radio>
                    <el-radio value="Other">其他</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="详细原因" prop="detail">
                    <el-input v-model="ruleForm.detail" />
            </el-form-item>
        </el-form>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="handleClose">Cancel</el-button>
                <el-button type="primary" @click="handleSubmit(ruleFormRef)">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<script lang="ts" setup>
// props:toreportid，需要举办的名字
// 
import { defineProps, defineEmits, ref ,reactive, computed } from 'vue'
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import axios from 'axios';
import main from '@/main';
const formSize = ref<ComponentSize>('default')

const props = defineProps({
    toreportid: Number,
    dialogFormVisible: Boolean,
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
    ElMessage.success(props.toreportid + ' 已被您('+props.myuserid+')举报，原因：' + ruleForm.reason + ' ' + ruleForm.detail)
    axios.post(main.url+ '/api/report', {
        userid:props.toreportid,
        reason:ruleForm.reason,
        detail:ruleForm.detail,
        reporter:props.myuserid
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
    }
    ).then(res => {
    if (res.status == 200) {
        ElMessage.success(props.toreportid + ' 已被您举报，原因：' + ruleForm.reason + ' ' + ruleForm.detail)

    } 
    else {
        ElMessage.success('举报出错,反正是发过去了')
        console.log(res)
        
    }
    })
    .catch(error => {
        ElMessage.success('举报出错')
        console.log(error)
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
    emit('reportStop')
}
</script>