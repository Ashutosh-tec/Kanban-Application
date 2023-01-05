import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName:"about" */ '../views/LogIn.vue')
  },
  {
    path: '/edit_list/:id',
    name: 'edit_list',
    component: () => import('../views/EditList.vue')
  },
  {
    path: '/add_list',
    name: 'add_list',
    component: () => import('../views/AddList.vue')
  },
  {
    path: '/add_task/:id',
    name: 'add_task',
    component: () => import('../views/AddTask.vue')
  },
  {
    path: '/list/:id1/edit_task/:id2',
    name: 'edit_task',
    component: () => import('../views/EditTask.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router