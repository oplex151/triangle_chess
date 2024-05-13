import { createRouter, createWebHistory } from 'vue-router'
import Cookies from 'js-cookie';

import Login from '@/views/Login/index.vue'
import Layout from '@/views/Layout/index.vue'
import Home from '@/views/Home/index.vue'
import Category from '@/views/Category/index.vue'
import Game from '@/views/Game/index.vue'
import Register from '@/views/Register/index.vue'
import Logout from '@/views/Logout/index.vue'
import Room from '@/views/Room/index.vue'
import { socket } from '@/sockets';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    //   主页
    {
      path: '/',
      component: Layout,
      meta: {isAuth: true,connection: false},
      // 这两个没用到
      children:[
        //   主页-默认页
        {
          path: '/home',
          component: Home,
          meta: {isAuth: true,connection: false},
        },
        //   主页-目录页
        {
          path: '/category',
          component: Category,
          meta: {isAuth: true,connection: false},
        },
      ]
    },
    //   登录页
    {
      path: '/login',
      component: Login,
      meta: {isAuth: false,connection: false},
    },
    //   登出页
    {
      path: '/logout',
      component: Logout,
      meta: {isAuth: true,connection: false},
    },
    //   主页-游戏页
    {
      path:'/game',
      component:Game,
      meta: {isAuth: true,connection: true},
    },
    //   房间
    {
      path:'/room',
      component: Room,
      meta: {isAuth: true,connection: true},
    },
    {
      path:'/register',
      component: Register,
      meta: {isAuth: false,connection: false},
    }
  ]
})

router.beforeEach((to, from, next) => {
  //在不需要连接的页面，断开连接
  if (!to.meta.connection) {
    socket.value = ""
    Cookies.remove('room_id')
    Cookies.remove('room_info')
  }
  if (to.meta.isAuth) {
    if (Cookies.get('userid')) {
      next()
    } else {
      next('/login')
    }
  } else {
    next()
  }
})

export default router
