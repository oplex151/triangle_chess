<script setup>
import { ref } from 'vue';

const uname = ref('');
const password = ref('');
const errorMessage = ref('');

const register = async() =>{
    try{

        const params = new URLSearchParams();
        params.append('uname', uname.value);
        params.append('password', password.value);
        const paramsString = 'http://localhost:9002/user/register?' + params.toString();
        const response = await fetch(paramsString, {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        uname: uname.value,
        password: password.value
        })
    });
    if (!response.ok) {
    throw new Error('注册失败');
    }
}
catch (error) {
    errorMessage.value = '网络异常，请稍后再试';
}
}
</script>

<template>
    
</template>