import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue')
  },
  // 旅行社模块 - 简化版，不使用子路由
  {
    path: '/agency',
    component: () => import('../views/agency/Index.vue'),
    meta: { requiresAuth: true, role: 'agency' }
  },
  {
    path: '/agency/routes',
    component: () => import('../views/agency/Routes.vue'),
    meta: { requiresAuth: true, role: 'agency' }
  },
  {
    path: '/agency/tourists',
    component: () => import('../views/agency/Tourists.vue'),
    meta: { requiresAuth: true, role: 'agency' }
  },
  {
    path: '/agency/itineraries',
    component: () => import('../views/agency/Itineraries.vue'),
    meta: { requiresAuth: true, role: 'agency' }
  },
  // 导游模块
  {
    path: '/guide',
    name: 'TourGuide',
    component: () => import('../views/guide/Index.vue'),
    meta: { requiresAuth: true, role: 'guide' }
  },
  // 游客模块
  {
    path: '/tourist',
    name: 'Tourist',
    component: () => import('../views/tourist/Index.vue'),
    meta: { requiresAuth: true, role: 'tourist' }
  },
  // 主管部门模块
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('../views/admin/Index.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  const userRole = localStorage.getItem('userRole')

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.role && to.meta.role !== userRole) {
    next('/login')
  } else {
    next()
  }
})

export default router