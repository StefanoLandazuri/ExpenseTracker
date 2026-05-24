<template>
  <nav class="fixed bottom-0 inset-x-0 md:hidden bg-white border-t border-gray-100 flex">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="flex-1 flex flex-col items-center justify-center py-3 text-xs font-medium"
      :class="route.path === item.path ? 'text-blue-600' : 'text-gray-400'"
    >
      <span class="text-xl mb-1">{{ item.icon }}</span>
      {{ item.label }}
    </router-link>

    <button
      type="button"
      @click="handleLogout"
      class="flex-1 flex flex-col items-center justify-center py-3 text-xs font-medium text-red-500"
    >
      <span class="text-xl mb-1">🚪</span>
      Logout
    </button>
  </nav>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/expenses', label: 'Expenses', icon: '💸' },
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