<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container">
      <a class="navbar-brand" href="#">Smart Parking</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li v-if="!isLoggedIn" class="nav-item">
            <router-link class="nav-link" to="/">Login</router-link>
          </li>
          <li v-if="!isLoggedIn" class="nav-item">
            <router-link class="nav-link" to="/register">Register</router-link>
          </li>
          <li v-if="isLoggedIn && isAdmin" class="nav-item">
            <router-link class="nav-link" to="/admin">Admin Dashboard</router-link>
          </li>
          <li v-if="isLoggedIn && !isAdmin" class="nav-item">
            <router-link class="nav-link" to="/user">User Dashboard</router-link>
          </li>
          <li v-if="isLoggedIn" class="nav-item">
            <a class="nav-link" href="#" @click="handleLogout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = ref(false)
const isAdmin = ref(false)

// Dummy logic; connect this to your actual auth/session logic!
function checkAuth() {
  const role = localStorage.getItem('role')
  isLoggedIn.value = !!role
  isAdmin.value = role === 'admin'
}
function handleLogout() {
  localStorage.removeItem('role')
  isLoggedIn.value = false
  isAdmin.value = false
  router.push('/')
}
checkAuth()
</script>
