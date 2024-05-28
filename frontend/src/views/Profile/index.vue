<script lang="ts" setup>
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
import UserInfo from './UserInfo.vue'


const router = useRouter()
const item = {
  //获取当前时间
  date:  new Date().toLocaleString(),
  name: Cookies.get('username'),
}
const tableData = ref(Array.from({ length: 20 }).fill(item))

function goBackHome(){
    router.push('/')
}

const CurrentView = UserInfo

</script>



<template>
    <div class="background-image"></div>
    <button class="button-home" @click="goBackHome()">
      <el-icon style="vertical-align: middle" size="30px">
        <HomeFilled />
      </el-icon>
    </button>
    <el-container class="layout-container">
      <el-header class="header">
        <div class="toolbar">
          <span>{{Cookies.get('username')}}</span>
        </div>
      </el-header>
      <el-container class="menu-container">
        <el-aside width="150px"  class="aside">
          <el-scrollbar rounded>
            <el-menu class="el-menu" active-text-color="#000">
              <el-menu-item index="1" class="el-menu-item"
              @click="CurrentView = UserInfo">
                  <el-icon><user /></el-icon>个人信息
              </el-menu-item>
              <el-menu-item index="2">
                <template #title>
                  <el-icon><icon-menu /></el-icon>对局历史
                </template>
              </el-menu-item>
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
        <el-main class="main">
          <component class="main-content" :is="CurrentView"></component>
         
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

.layout-container {
  position: relative;
  top : -10px;
}

.header {
  height: 60px;
  line-height: 60px;
  background-color: #d79e03;
  color: #fff;  
  border-radius: 10px;
  margin-left: 70px;
  
}

   
.aside {
  margin-top: 10px;
  border-radius: 5px;
  width: 150px;

}

.el-menu{
  background-color :#ecb920;
  color : #000000;
}

.el-menu-item{
  background-color :#ecb920;
}

.el-menu-item:hover{
  background-color :#d79e03;
  color : #000000 !important;
}

.el-menu-item.is-active{
  background-color :#d79e03;
  color : #000000 !important;
}



.toolbar {
  display: inline-flex;
  align-items: right;
  justify-content: right;
  background-color: #d79e03;
  height: 100%;
  right: 20px;
  width: 100%;
}

.main-content {
  margin-top: 10px;
  margin-left: 10px;
  border-radius: 5px;
  background-color: #fdeec4;
  min-height: 500px;
}

.main {
  text-align: center;
  margin-top: 10px;
  margin-left: 10px;
  border-radius: 5px;
  background-color: #fdeec4;
}

</style>