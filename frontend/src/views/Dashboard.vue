<template>
  <div class="p-8">
    <h1 class="text-2xl font-bold mb-4">Dashboard</h1>
    <p class="text-gray-600 mb-6">Logged in as: {{ auth.user?.email }}</p>
    <button
      @click="handleLogout"
      class="bg-red-500 text-white px-4 py-2 rounded-lg"
    >
      Logout
    </button>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function handleLogout() {
  auth.logout()
  await router.push('/login')
}
</script>