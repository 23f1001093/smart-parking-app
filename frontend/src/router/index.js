import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import UserDashboard from '../components/UserDashboard.vue'
import ParkingLots from '../components/ParkingLots.vue'
import MyReservations from '../components/MyReservations.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import AdminLots from '../components/AdminLots.vue'
import AdminUsers from '../components/AdminUsers.vue'
import LotStatus from '../components/LotStatus.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/register', component: Register },
  { path: '/user', component: UserDashboard },
  { path: '/lots', component: ParkingLots },
  { path: '/reservations', component: MyReservations },
  { path: '/admin', component: AdminDashboard },
  { path: '/admin/lots', component: AdminLots },
  { path: '/admin/users', component: AdminUsers },
  { path: '/admin/status', component: LotStatus }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
