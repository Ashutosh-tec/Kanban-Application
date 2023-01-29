import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'



Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    
    component: () => import(/* webpackChunkName:"about" */ '../views/LogIn.vue')
  },
  {
    path: '/create_account',
    name: 'create_account',
    component: () => import(/**/'../views/CreateAccount.vue')
  },
  {
    path: '/edit_list/:id',
    name: 'edit_list',
    component: () => import(/**/'../views/EditList.vue')
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
  {
    path: '/Summary_page',
    name: 'summay_page',
    component: () => import(/**/'../views/summary.vue')
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


export default router
