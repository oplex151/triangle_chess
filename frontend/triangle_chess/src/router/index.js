import { createRouter, createWebHistory } from 'vue-router'
import Cookies from 'js-cookie';

import Login from '@/views/Login/index.vue'
import Layout from '@/views/Layout/index.vue'
import Home from '@/views/Home/index.vue'
import Category from '@/views/Category/index.vue'
import Game from '@/views/Game/index.vue'
import Register from '@/views/Register/index.vue'
import Logout from '@/views/Logout/index.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/test',
      name: 'test',
      component: () => import('@/views/Test_socket/index.vue')
    },
    //   主页
    {
      path: '/',
      component: Layout,
      children:[
        //   主页-默认页
        {
          path: '/',
          component: Home,
        },
        //   主页-目录页
        {
          path: '/category',
          component: Category,
          meta: {isAuth: true},
        },

      ]
    },
    //   登录页
    {
      path: '/login',
      component: Login,
    },
    //   登出页
    {
      path: '/logout',
      component: Logout,
    },
    //   主页-游戏页
    {
      path:'/game',
      component:Game,
      meta: {isAuth: true},
    },
    {
      path:'/register',
      component: Register,

    }
  ]
})

router.beforeEach((to, from, next) => {
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
