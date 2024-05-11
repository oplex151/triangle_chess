<script setup>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import Cookies from 'js-cookie';
import { useRouter } from 'vue-router';

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
    }
    ).then(res => {
        if (res.status == 200) {
        Cookies.remove('userid');
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
            router.push('/');
        }
        else {
        ElMessage({
            message: '请求错误',
            grouping: true,
            type: 'error',
            showClose: true
        })
        router.push('/');
        }
    });
})
</script>