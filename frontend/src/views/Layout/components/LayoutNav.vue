<script setup>
import Cookies from "js-cookie";
import {ref} from "vue";
import FriendDrawer from "@/components/views/FriendDrawer.vue";
// 定义一个响应式变量 categoryList，存储页面导航栏的数据
const categoryList = ref([
  {
    id:2,
    name:"房间模式",
    url:"/room",
    picture:""
  },
  {
    id:7,
    name:"匹配模式",
    url:"/match",
    picture:""
  },
  {
    id:10,
    name:"排位模式",
    url:"/rank",
    picture:""
  },
  {
    id:11,
    name:"观战模式",
    url:"/witness",
    picture:""
  },
  {
    id:3,
    name:"个人中心",
    url:'/profile',
    picture:""
  },
  {
    id:6,
    name:"棋局广场",
    url:"/ground",
    picture:""
  },
  {
    id:7,
    name:"登出",
    url:"/logout",
    picture:""
  },
])
const NoLoggedList = ref([
  {
    id:1,
    name:"登录",
    url:"/login",
    picture:""
  },
  {
    id:5,
    name:"关于我们",
    url:"/",
    picture:""
  },
])
const logged = ref(Cookies.get("userid"))
</script>
<template>
  <div class="background-image"></div>
  <div class="centered-buttons">
    <!-- 使用v-for指令循环渲染页面导航按钮 -->
    <div v-if=logged>
    <RouterLink v-for="item in categoryList" :key="item.id" :to="item.url" class="centered-button">{{ item.name }}</RouterLink>
    </div>
    <div v-else>
    <RouterLink v-for="item in NoLoggedList" :key="item.id" :to="item.url" class="centered-button">{{ item.name }}</RouterLink>
    </div>
  </div>
  <div class="friend-drawer">
    <FriendDrawer />
  </div>
</template>

<style lang="scss" scoped>
/* 样式定义部分 */
.centered-buttons {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.centered-button {
  display: block;
  padding: 10px 20px;
  margin-bottom: 10px;
  background-color: #f6bb4e;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
  //美化边界
  box-shadow: 0 5px 5px rgba(0, 0, 0, 0.3);
  //宽度一致
  width: 200px;
  //字体居中
  text-align: center;
  //位置居中
  position: relative;
  left: 0%;
  transform: translateX(-0%, -0%);
  font-size: 18px;
  font-weight: bold;
  //鼠标悬停时背景颜色变化
  cursor: pointer;
  //美化边界
  box-shadow: 0 5px 5px rgba(0, 0, 0, 0.3);
  //宽度一致
  width: 200px;
  //字体居中
  text-align: center;
}

.centered-button:hover {
  background-color: #b38c00e9;
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

.friend-drawer{
  position: fixed;
  right: 0%;
}
</style>
