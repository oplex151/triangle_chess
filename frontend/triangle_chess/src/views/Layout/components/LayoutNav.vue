<script setup>
import {ref} from "vue";

// 定义一个响应式变量 categoryList，存储页面导航栏的数据
const categoryList = ref([
  {
    id:1,
    name:"个人中心/登录",
    url:"/login",
    picture:""
  },
  {
    id:2,
    name:"开始比赛",
    url:"/game",
    picture:""
  },
  {
    id:3,
    name:"战绩查看",
    url:"/",
    picture:""
  },
  {
    id:4,
    name:"帮助中心",
    url:"/",
    picture:""
  },
  {
    id:5,
    name:"关于我们",
    url:"/",
    picture:""
  },
])
</script>
<template>
  <!-- 页面模板 -->
  <div class="background-image"></div>
  <div class="centered-buttons">
    <!-- 使用v-for指令循环渲染页面导航按钮 -->
    <RouterLink v-for="item in categoryList" :key="item.id" :to="item.url" class="centered-button">{{ item.name }}</RouterLink>
  </div>
</template>

<style lang="scss" scoped>
/* 样式定义部分 */
.centered-buttons {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
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
  //位置居中
  position: relative;
  left: 50%;
  transform: translateX(-0%, -0%);
  //字体宋体
  font-family: "SimSun", "宋体";
  font-size: 14px;
  font-weight: bold;
  //鼠标悬停时背景颜色变化
  cursor: pointer;
  //美化边界
  box-shadow: 0 5cqh 5px rgba(0, 0, 0, 0.3);
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
  /* 使用背景图片填充页面背景 */
  background-image: url('@/assets/images/login/图1.jpg');
  background-size: cover;
  z-index: -1;
}
</style>