<template>
  <div class="container py-4">
    <h4>My Reservations</h4>
    <table class="table">
      <thead>
        <tr>
          <th>Spot ID</th>
          <th>Vehicle</th>
          <th>In</th>
          <th>Out</th>
          <th>Cost</th>
          <th>Status</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in reservations" :key="r.id">
          <td>{{ r.spot_id }}</td>
          <td>{{ r.vehicle_number }}</td>
          <td>{{ r.parking_timestamp && new Date(r.parking_timestamp).toLocaleString() }}</td>
          <td>{{ r.leaving_timestamp && new Date(r.leaving_timestamp).toLocaleString() }}</td>
          <td>{{ r.parking_cost }}</td>
          <td>
            <span v-if="!r.leaving_timestamp" class="badge bg-warning text-dark">Active</span>
            <span v-else class="badge bg-success">Completed</span>
          </td>
          <td>
            <button 
              v-if="!r.leaving_timestamp" 
              class="btn btn-danger btn-sm"
              @click="release(r.id)">Release</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
const reservations = ref([])
async function fetchReservations() {
  const res = await fetch('/api/my/reservations', { credentials: 'include' })
  reservations.value = await res.json()
}
async function release(reservation_id) {
  if (confirm('Release this spot?')) {
    const res = await fetch('/api/reservations/' + reservation_id + '/release', {
      method: 'POST',
      credentials: 'include'
    })
    if (res.ok) fetchReservations()
    else alert('Release failed.')
  }
}
onMounted(fetchReservations)
</script>
