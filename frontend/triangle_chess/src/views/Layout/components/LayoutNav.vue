<script setup>
import {ref} from "vue";

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
  <div class="centered-buttons">
    <RouterLink v-for="item in categoryList" :key="item.id" :to="item.url" class="centered-button">{{ item.name }}</RouterLink>
  </div>
</template>

<style lang="scss" scoped>
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
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.centered-button:hover {
  background-color: #0056b3;
}
</style>
