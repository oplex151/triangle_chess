<script setup>
import { ref, reactive } from 'vue'
import Report from '@/components/views/Report.vue'
import Avatar from '@/components/views/Avatar.vue'


const vis = ref(false)
const name = ref('name')
const handleReportEnd = () => {
    vis.value = false
}
const handleReport = (userid) => {
    name.value = userid
    vis.value = true
}
</script>
<template>
    <Report :name=name :dialogFormVisible=vis @reportEnd="handleReportEnd"/>
    <Avatar :my_camp="my_camp" :userid=1 @reportUser="handleReport">
        <template #name>
            <p>{{name}}</p>    
        </template>
        <template #avatar>
            {{name}}
        </template>
    </Avatar>
</template>