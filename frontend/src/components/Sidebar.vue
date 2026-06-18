<template>
  <aside class="hidden md:flex flex-col w-64 bg-white border-r border-gray-100 min-h-screen px-4 py-6">
    <h1 class="text-lg font-bold text-gray-900 mb-6 px-2">Expense Tracker</h1>

    <button
      @click="emit('add')"
      class="flex items-center justify-center gap-2 bg-blue-600 text-white rounded-xl py-2.5 mb-6 text-sm font-medium hover:bg-blue-700 transition-colors"
    >
      <Plus :size="18" />
      Add Expense
    </button>

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
        <component :is="item.icon" :size="18" />
        {{ item.label }}
      </router-link>
    </nav>

    <button
      @click="handleLogout"
      class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium text-red-500 hover:bg-red-50 transition-colors"
    >
      <LogOut :size="18" />
      Logout
    </button>
  </aside>
</template>

<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { LayoutDashboard, Wallet, Plus, LogOut } from '@lucide/vue'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const emit = defineEmits<{ add: [] }>()

const items = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/expenses',  label: 'Expenses',  icon: Wallet },
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