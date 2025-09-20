<template>
  <Navbar />
  <main>
    <router-view />
  </main>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
</script>

<style>
body {
  background-color: #f8f9fa;
}
main {
  min-height: 90vh;
}
</style>
