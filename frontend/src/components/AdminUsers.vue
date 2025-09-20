<template>
  <div class="container py-3">
    <h3>All Registered Users</h3>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>UserID</th>
          <th>Username</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const users = ref([])
onMounted(async () => {
  const res = await fetch('/api/admin/users', { credentials: 'include' })
  users.value = await res.json()
})
</script>
