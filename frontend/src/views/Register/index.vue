<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import axios from 'axios';
import main from '@/main';
import { reactive, ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'

const formRef = ref<FormInstance>()
const disableForm = ref(false)
const router = useRouter();
const errorMessage = ref('')
const RegisterForm = reactive({
    username: '',
    email: '',
    phone_num: '',
    password: '',
    repassword: '',
    gender: ''
})

const checkUsername = (rule: any, value: any, callback: any) => {
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
    else if (value.length < 8 || value.length > 50) {
        callback(new Error('密码长度为8-50位'))
    }
    else if (!/^[ -~]+$/.test(value)) {
        callback(new Error('密码只能由字符和数字构成'))
    }
    else if (!/^[^\s]+$/.test(value)) {
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
            {
                trigger: ['blur', 'change'],
                validator: checkUsername
            }
        ],
        password: [
            {
                trigger: ['blur', 'change'],
                validator: checkPassword
            }
        ],
        repassword: [
            {
                trigger: ['blur', 'change'],
                validator: checkRepassword
            }
        ]
    }
)

const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid) => {
        if (valid) {
            console.log('submit!')
            disableForm.value = true
            axios.post(main.url + '/api/register', {
                'username': RegisterForm.username,
                'password': RegisterForm.password,
                'email': RegisterForm.email,
                'phone_num': RegisterForm.phone_num,
                'gender': RegisterForm.gender
                /* Hash! */
            },
                {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
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

watch(errorMessage, (oldValue, newValue) => {
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
            <el-form ref="formRef" style="max-width: 315px ;width: 350px; position: relative;" :model="RegisterForm"
                label-width="auto" :rules="Validator" class="form-container" status-icon :disabled=disableForm
                hide-required-asterisk>
                <el-form-item prop="username" class="form-group">
                    <div class="form-label">用户名:&nbsp </div>
                    <el-input class="form-input" v-model="RegisterForm.username" type="text" autocomplete="on" />
                </el-form-item>
                <el-form-item prop="email" class="form-group" :rules="[
                    // {
                    //     required: true,
                    //     message: '请输入邮箱',
                    //     trigger: 'blur',
                    // },
                    {
                        type: 'email',
                        message: '请输入正确的邮箱地址',
                        trigger: ['blur', 'change'],
                    },
                ]">
                    <div class="form-label">邮&nbsp箱:&nbsp </div>
                    <el-input class="form-input" v-model="RegisterForm.email" type="text" autocomplete="on" />
                </el-form-item>
                <el-form-item prop="phone" class="form-group" :rules="[
                    // { required: true, message: '请输入手机号' },
                    { type: 'number', message: '请输入正确的手机号' },
                ]">
                    <div class="form-label">手机号:&nbsp </div>
                    <el-input class="form-input" v-model="RegisterForm.phone_num" type="text" autocomplete="on" />
                </el-form-item>
                <el-form-item prop="gender" class="form-group">
                    <div class="form-label">性&nbsp别:&nbsp</div>
                    <el-radio-group v-model="RegisterForm.gender" class="form-input">
                        <el-radio value="male" size="large">男</el-radio>
                        <el-radio value="female" size="large">女</el-radio>
                        <el-radio value="" size="large">不愿透露</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item prop="password" class="form-group">
                    <div class="form-label">密&nbsp码:&nbsp</div>
                    <el-input class="form-input" v-model="RegisterForm.password" type="password" autocomplete="off"
                        show-password />
                </el-form-item>
                <el-form-item prop="repassword" class="form-group">
                    <div class="form-label">重复密码: </div>
                    <el-input class="form-input" v-model="RegisterForm.repassword" type="password" autocomplete="off"
                        show-password />
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" class="login-button" @click="submitForm(formRef)">注册</el-button>
                </el-form-item>
                <el-form-item>
                    <el-button class="clear-button" @click="resetForm(formRef)">清空</el-button>
                </el-form-item>
            </el-form>
            <router-link to="/login" class="gobutton">返回</router-link>
        </div> <!-- end of login-container -->

    </div> <!-- end of outer-container -->
</template>

<style scoped>
.gobutton {
    display: text-indent;
    color: #00b88d;
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
    width: 560px;
    height: 660px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 20px;
    position: relative;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    background-color: rgba(248, 234, 171, 0.8);
    /* 设置一个半透明的背景色 */
}

.login-button {
    justify-content: center;
    background-color: #f6bb4e;
    color: #fff;
    border: none;
    border-radius: 15px;
    padding: 15px 0;
    /* 增加垂直内边距 */
    margin: auto;
    cursor: pointer;
    font-size: 15px;
    height: 50px;
    width: 280px;
    margin-top: 20px;
}

.clear-button {
    justify-content: center;
    background-color: #605f5f;
    color: #fff;
    border: none;
    border-radius: 15px;
    padding: 15px 0;
    /* 增加垂直内边距 */
    margin: auto;
    cursor: pointer;
    font-size: 15px;
    height: 50px;
    width: 280px;
    margin-top: -5px;
}

.login-title {
    text-align: center;
    font-size: 30px;
    margin-top: 20px;
    margin-bottom: 30px;
    font-family: "SimSun";
    font-weight: bold;
}


.form-container {
    margin: auto;
    border: initial;
    transform: translate(-0%, -0%);
    background-color: rgba(255, 255, 255, 0);
    /* 设置一个半透明的背景色 */
}

.login-form {
    display: flex;
    flex-direction: column;
}

.form-group {
    margin-bottom: 26px;
    align-items: flex-start;
    /* 让 form-label 和 form-input 上下对齐 */
    display: flex;
    flex-direction: row;
}

.form-label {
    width: 70px;
    font-weight: bold;
    font-size: 15px;
    /* 增加字体大小 */
    font-family: "SimSun";
}

.el-input {
    width: 240px;
    height: 55px;
}

.form-input {

    align-items: flex-start;
    height: 30px;
    width: 220px;
    font-size: 18px;
    /* 增加输入框字体大小 */

}

.form-button {
    display: flex;
    justify-content: center;
}
</style>
