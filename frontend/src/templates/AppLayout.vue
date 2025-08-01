<template>
  <div class="app-layout">
    <Navbar />
    <div class="main-container" :class="{ 'sidebar-collapsed': isCollapsed }">
      <Header />
      <main class="content">
        <router-view />
      </main>
      <Footer />
    </div>
  </div>
</template>

<script setup>
import Navbar from './Navbar.vue'
import Header from './Header.vue'
import Footer from './Footer.vue'
</script>

<style scoped>
@import '../assets/styles/applayout-style.css';
</style>


