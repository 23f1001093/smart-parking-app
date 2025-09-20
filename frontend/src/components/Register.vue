<template>
  <div class="container py-5">
    <div class="row justify-content-center">
      <div class="col-md-4">
        <div class="card p-4 shadow">
          <h3 class="card-title mb-3">Register</h3>
          <form @submit.prevent="register">
            <div class="mb-3">
              <input v-model="username" type="text" class="form-control" placeholder="Username" required />
            </div>
            <div class="mb-3">
              <input v-model="email" type="email" class="form-control" placeholder="Email" required />
            </div>
            <div class="mb-3">
              <input v-model="password" type="password" class="form-control" placeholder="Password" required />
            </div>
            <button class="btn btn-success w-100" :disabled="loading">Register</button>
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
const username = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const router = useRouter()

async function register() {
  loading.value = true
  error.value = ''
  const res = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: username.value, email: email.value, password: password.value })
  })
  const data = await res.json()
  if (res.ok) {
    router.push('/')
  } else {
    error.value = data.message || 'Registration failed'
  }
  loading.value = false
}
</script>
