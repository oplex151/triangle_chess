<template>
    <el-form
    ref="formRef"
    style="max-width: 300px ;width: 300px "
    :model="RegisterForm"
    label-width="auto"
    :rules="Validator"
    class="login-form"
    status-icon
    :disabled=disableForm
    >
    <el-form-item
        label="用户名"
        prop="username"
    >
        <el-input
        v-model="RegisterForm.username"
        type="text"
        autocomplete="on"
        />
    </el-form-item>
    <el-form-item
        label="密&nbsp&nbsp&nbsp码"
        prop="password"
        
    >
        <el-input
        v-model="RegisterForm.password"
        type="password"
        autocomplete="off"
        show-password
        />
    </el-form-item>
    <el-form-item
        label="重复密码"
        prop="repassword"    
    >
        <el-input
        v-model="RegisterForm.repassword"
        type="password"
        autocomplete="off"
        show-password
        />
    </el-form-item>   
    <el-form-item>
        <el-button type="primary" @click="submitForm(formRef)">注册</el-button>
        <el-button @click="resetForm(formRef)">清空</el-button>
    </el-form-item>
    </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { RTL_OFFSET_POS_ASC } from 'element-plus/es/components/virtual-list/src/defaults';

const formRef = ref<FormInstance>()
const disableForm = ref(false)
const RegisterForm = reactive({
    username: '',
    password: '',
    repassword:''
})

const checkUsername   = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('请输入用户名'))
    } else {
        callback()
    }
}
const checkPassword = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('请输入密码'))
    } 
    else if(value.length < 8 || value.length > 50) {
        callback(new Error('密码长度为8-50位'))
    }   
    else if(!/^[ -~]+$/.test(value)) {
        callback(new Error('密码只能由字符和数字构成'))
    }
    else if(!/^[^\s]+$/.test(value)) {
        callback(new Error('密码不能含有空格'))
    } 
    else {
        callback()
    }
}

const checkRepassword = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('请重复密码'))
    } 
    else if (value !== RegisterForm.password) {
        callback(new Error('两次输入密码不一致'))
    }
    else {
        callback()
    }
}

const Validator = reactive<FormRules<typeof RegisterForm>>(
    {
        username: [
            {trigger: 'blur',
            validator:checkUsername
            }
        ],
        password: [
            { trigger: 'blur',
            validator:checkPassword}
        ],
        repassword: [
            {trigger: 'blur' ,
            validator:checkRepassword}
        ]
    }
)

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid) => {
    if (valid) {
        console.log('submit!')
        disableForm.value = true
    } else {
        console.log('error submit!')
        return false
    }
    })
}
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
</script>
