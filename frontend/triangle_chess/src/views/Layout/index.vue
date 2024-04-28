<script setup>
import LayoutNav from "@/views/Layout/components/LayoutNav.vue";
import LayoutHeader from "@/views/Layout/components/LayoutHeader.vue";
import LayoutFooter from "@/views/Layout/components/LayoutFooter.vue";
</script>

<template>
  <!--  展示二级路由内容：二级路由出口-->
  <LayoutNav/>
  <LayoutHeader/>
  <RouterView/>
  <LayoutFooter/>
</template>

<style scoped>

</style>