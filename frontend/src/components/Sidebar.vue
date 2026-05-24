<template>
  <aside class="hidden md:flex flex-col w-64 bg-white border-r border-gray-100 min-h-screen px-4 py-6">
    <h1 class="text-lg font-bold text-gray-900 mb-8 px-2">Expense Tracker</h1>

    <nav class="flex-1 space-y-1">
      <router-link
        v-for="item in items"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors"
        :class="route.path === item.path
          ? 'bg-blue-50 text-blue-700'
          : 'text-gray-600 hover:bg-gray-50'"
      >
        <span class="text-lg">{{ item.icon }}</span>
        {{ item.label }}
      </router-link>
    </nav>

    <button
      @click="handleLogout"
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-red-500 hover:bg-red-50 transition-colors"
    >
      <span class="text-lg">🚪</span>
      Logout
    </button>
  </aside>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const items = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/expenses',  label: 'Expenses',  icon: '💸' },
]

async function handleLogout() {
  const shouldLogout = window.confirm('Do you want to log out?')

  if (!shouldLogout) {
    return
  }

  auth.logout()
  await router.push('/login')
}
</script>