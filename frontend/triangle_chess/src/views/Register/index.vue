<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import axios from 'axios';
import main from '@/main';
import { reactive, ref ,watch} from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()
const disableForm = ref(false)
const router = useRouter();
const errorMessage = ref('')
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
        axios.post(main.url+ '/register', {
        'username':    RegisterForm.username,
        'password': RegisterForm.password
        /* Hash! */
    },
        {
            headers: {'Content-Type':'application/x-www-form-urlencoded'},
        }
        ).then(res => {
            if (res.status === 200) {
                ElMessage.success("注册成功！")
                disableForm.value = true
                router.push('/login');
            } 
            else if (res.status === 503) {
                errorMessage.value = '用户名已存在！'
                disableForm.value = false                
            }
            else {
                disableForm.value = false
                errorMessage.value = '未知错误'
            }
        }).catch(err => {
            console.log(err);
            errorMessage.value = err;
            disableForm.value = false
        });
        disableForm.value = false
    } else {
        console.log('error submit!');
        errorMessage.value = '注册表单出错!'
        disableForm.value = false
        return false
    }
    })
}
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}

watch(errorMessage, (oldValue ,newValue) => {
    if (newValue !== oldValue && errorMessage.value !== '') {
        ElMessage({
        message: errorMessage.value,
        grouping: true,
        type: 'error',
        showClose: true
    })
        errorMessage.value = '';
    }
});
</script>

<template>
    <div class="outer-container">
        
        <div class="background-image"></div>
        <div class="login-container">
        <h1 class="login-title">注册</h1>

        <div class="form-container">                
            <el-form
                ref="formRef"
                style="max-width: 300px ;width: 300px;"
                :model="RegisterForm"
                label-width="auto"
                :rules="Validator"
                class="demo-ruleForm"
                status-icon
                :disabled=disableForm
                hide-required-asterisk	
                >
                <el-form-item
                    label="用户名: "
                    prop="username"
                >
                    <el-input
                    v-model="RegisterForm.username"
                    type="text"
                    autocomplete="on"
                    />
                </el-form-item>
                <el-form-item
                    label="密&nbsp&nbsp&nbsp码: "
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
                    label="重复密码: "
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
        </div> <!-- end of form-container -->
        <router-link to="/login" class="returnbutton">返回</router-link>
        </div>  <!-- end of login-container -->
    </div>   <!-- end of outer-container -->
</template>

<style scoped>
.returnbutton{
    color:rgb(8, 165, 110);
    font-size:larger;
    font-weight: bold;
}
.outer-container {
    display: center;
    justify-content: center;
    align-items: center;
    height: 100vh;
    }

.background-image {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('@/assets/images/login/图1.jpg');
    background-size: cover;
    z-index: -1;
}

.login-container {
    margin-top: 100px;

    height: flex;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 20px;

    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: rgba(255, 255, 255, 0.8); /* 设置一个半透明的背景色 */
}

.login-title {
    text-align: center;
    font-size: 30px;
    margin-bottom: 80px;
}

.form-container {
    display: flex;
    justify-content: center;
    min-width: 500px;
}

.login-form {
    display: flex;
    flex-direction: column;
}

.form-group {
    margin-bottom: 70px;
    align-items: flex-start; /* 让 form-label 和 form-input 上下对齐 */
}

.form-label {
    font-weight: bold;
    font-size: 25px; /* 增加字体大小 */
}

.form-input {
    padding: 15px;
    border: 2px solid #ccc; /* 增加边框宽度 */
    border-radius: 5px;
    font-size: 18px; /* 增加输入框字体大小 */
}

.form-button{
    display: flex;
    justify-content: center;
}

.login-button {
    justify-content: center;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 15px;
    padding: 15px 0; /* 增加垂直内边距 */
    cursor: pointer;
    font-size: 25px;
    height: 70px;
    width: 250px;
}
</style>


