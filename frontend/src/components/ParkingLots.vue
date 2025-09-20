<template>
  <div class="container py-3">
    <h4>Available Parking Lots</h4>
    <div class="row">
      <div v-for="lot in lots" :key="lot.id" class="col-md-4 mb-3">
        <div class="card shadow">
          <div class="card-body">
            <h5>{{ lot.prime_location_name }}</h5>
            <p>{{ lot.address }}, {{ lot.pin_code }}</p>
            <span class="badge bg-info text-dark mb-2">₹{{ lot.price }}</span>
            <span class="badge" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
              {{ lot.available_spots > 0 ? `Available: ${lot.available_spots}` : 'Full' }}
            </span>
          </div>
          <div class="card-footer">
            <ReserveForm v-if="lot.available_spots > 0" :lot="lot" @success="fetchLots"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ReserveForm from './ReserveForm.vue'
const lots = ref([])
async function fetchLots() {
  const res = await fetch('/api/parkinglots', { credentials: 'include' })
  lots.value = await res.json()
}
onMounted(fetchLots)
</script>
