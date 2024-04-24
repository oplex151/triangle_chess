import { createRouter, createWebHistory } from 'vue-router'
import Login from '@/views/Login/index.vue'
import Layout from '@/views/Layout/index.vue'
import Home from '@/views/Home/index.vue'
import Category from '@/views/Category/index.vue'
import Game from '@/views/Game/index.vue'
import Register from '@/views/Register/index.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    //   主页
    {
      path: '/',
      component: Layout,
      children:[
        //   主页-默认页
        {
          path: '/',
          component: Home
        },
        //   主页-目录页
        {
          path: '/category',
          component: Category
        },

      ]
    },
    //   登录页
    {
      path: '/login',
      component: Login,
    },
    //   主页-游戏页
    {
      path:'/game',
      component:Game
    },
    {
      path:'/register',
      component: Register
    }
  ]
})

export default router
