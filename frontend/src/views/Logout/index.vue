<script setup>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';
import * as CONST from '@/lib/const'; 

import main from '@/main';
import { onBeforeMount } from 'vue'
const router = useRouter();

onBeforeMount(() =>{
    console.log(Cookies.get('userid'));
    axios.post(main.url+ '/api/logout', {
    'userid': Cookies.get('userid'),
    },
    {
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
        timeout:4000,
    }
    ).then(res => {
        if (res.status == 200) {
            Cookies.remove('userid');
            Cookies.remove('room_id');
            Cookies.remove('room_info');
            Cookies.remove('username');
            router.push('/');
        }         
    }).catch(err => {
        if (err.response.status == 507) {
            ElMessage({
                message: '用户未登录或登录超时',
                grouping: true,
                type: 'error',
                showClose: true
            })
            Cookies.remove('userid');
            Cookies.remove('room_id');
            Cookies.remove('room_info');
            Cookies.remove('username');
            router.push('/');
        }
        else if (err.response.status == CONST.SESSION_EXPIRED){
            ElMessage({
                message: '会话过期，请重新登录',
                grouping: true,
                type: 'error',
                showClose: true
            })
            Cookies.remove('userid');
            Cookies.remove('room_id');
            Cookies.remove('room_info');
            Cookies.remove('username');
            router.push('/');
        }
        else {
            ElMessage({
                message: '请求错误',
                grouping: true,
                type: 'error',
                showClose: true
            })
            Cookies.remove('userid');
            Cookies.remove('room_id');
            Cookies.remove('room_info');
            Cookies.remove('username');
            router.push('/');
        }
    });

})
</script>