<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import Cookies from 'js-cookie'
import Report from '@/components/views/Report.vue'
import Avatar from '@/components/views/Avatar.vue'


const vis = ref(false)
const name = ref('name')
const name1 = ref('name')
const handleReportEnd = () => {
    vis.value = false
}
const handleReport = (userid) => {
    name1.value = userid
    vis.value = true
}
</script>
<template>
    <Report :toreportid=name1 :myuserid=0 :dialogFormVisible=vis @reportEnd="handleReportEnd" />
    <Avatar :my_camp="my_camp" :userid=1 @reportUser="handleReport">
        <template #name>
            <p>{{name}}</p>    
        </template>
        <template #avatar>
            {{name}}
        </template>
    </Avatar>
</template>
