<script lang="ts" setup>
import VueSocketIO from 'vue-socket.io'
import SocketIO from 'socket.io-client'
//import main from '@/main'
import { onMounted, ref, getCurrentInstance ,computed} from 'vue'
//import { registerSockets, socket, registerSocketsForce, removeSockets } from '@/sockets'
import axios from 'axios'
import Cookies from 'js-cookie'
import { useRouter } from 'vue-router';
import { ElDivider, ElInput, ElMessage } from 'element-plus'
//import * as CONST from '@/lib/const.js'
import { User, HomeFilled } from '@element-plus/icons-vue'

import { Menu as IconMenu, Message, Setting } from '@element-plus/icons-vue'
import PersonalProfile from 'components/PersonalProfile.vue'


const router = useRouter()
const item = {
  date: '2016-05-02',
  name: 'Tom',
  address: 'No. 189, Grove St, Los Angeles',
}
const tableData = ref(Array.from({ length: 20 }).fill(item))



function goBackHome(){

    router.push('/')
}



</script>



<template>
    <div class="background-image"></div>
    <button class="button-home" @click="goBackHome()">
      <el-icon style="vertical-align: middle" size="30px">
        <HomeFilled />
      </el-icon>
    </button>
    <el-container class="layout-container-demo" style="height: 800px">
        <el-header style="text-align: right; font-size: 12px">
          <div class="toolbar">
            <!-- <el-dropdown>
              <el-icon style="margin-right: 8px; margin-top: 1px">
                <setting />
              </el-icon>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>View</el-dropdown-item>
                  <el-dropdown-item>Add</el-dropdown-item>
                  <el-dropdown-item>Delete</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown> -->
            <span>Tom</span>
          </div>
        </el-header>


  
      <el-container>
        <el-aside width="200px">
        <el-scrollbar>
          <el-menu 
          :default-openeds="['1', '3']"
          @select="handleMenuSelect"
          >
            <el-sub-menu index="1">
              <template #title>
                <el-icon><user /></el-icon>个人信息
              </template>
                <el-menu-item index="1-1">Option 1</el-menu-item>
                <el-menu-item index="1-2">Option 2</el-menu-item>
                <el-menu-item index="1-3">Option 3</el-menu-item>

            </el-sub-menu>
            <el-sub-menu index="2">
              <template #title>
                <el-icon><icon-menu /></el-icon>对局历史
              </template>
                <el-menu-item index="2-1">Option 1</el-menu-item>
                <el-menu-item index="2-2">Option 2</el-menu-item>
                <el-menu-item index="2-3">Option 3</el-menu-item>

            </el-sub-menu>
            <el-sub-menu index="3">
              <template #title>
                <el-icon><setting /></el-icon>设置
              </template>
                <el-menu-item index="3-1">Option 1</el-menu-item>
                <el-menu-item index="3-2">Option 2</el-menu-item>
                <el-menu-item index="3-3">Option 3</el-menu-item>
            </el-sub-menu>
          </el-menu>
        </el-scrollbar>
      </el-aside>

  
        <el-main>
          <component :is="currentComponent"></component>
        </el-main>
      </el-container>
    </el-container>
  </template>


<style scoped>
.button-home {
  position: absolute;
  top: 20px;
  left: 20px;
  background-color: #ecb920;
  border: 5px solid #d79e03;
  padding: 10px 20px;
  border-radius: 40px;
  font-size: 18px;
  cursor: pointer;
}
.layout-container-demo .el-header {
  position: relative;
  background-color: #ecb920;
  color: var(--el-text-color-primary);
}
.layout-container-demo .el-aside {
  color: var(--el-text-color-primary);
  background: #ffe7b0;
  opacity: 0.9;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}
.layout-container-demo .el-menu {
  border-right: none;
  background: #ecb920;
}
.layout-container-demo .el-main {
    
  padding: 0;
}
.layout-container-demo .toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
.layout-container-demo .el-menu-item{
    background-color: #ffe7b0;
}
</style>