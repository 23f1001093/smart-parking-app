<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card p-4 shadow">
          <h3 class="card-title mb-3">Login</h3>
          <form @submit.prevent="login">
            <div class="mb-3">
              <input v-model="email" type="email" class="form-control" placeholder="Email" required />
            </div>
            <div class="mb-3">
              <input v-model="password" type="password" class="form-control" placeholder="Password" required />
            </div>
            <button class="btn btn-primary w-100" :disabled="loading">Login</button>
          </form>
          <div v-if="error" class="alert alert-danger mt-2">{{ error }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function login() {
  loading.value = true
  error.value = ''
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({ email: email.value, password: password.value })
  })
  const data = await res.json()
  if (res.ok && data.role) {
    localStorage.setItem('role', data.role)
    router.push(data.role === 'admin' ? '/admin' : '/user')
  } else {
    error.value = data.message || 'Login failed'
  }
  loading.value = false
}
</script>
