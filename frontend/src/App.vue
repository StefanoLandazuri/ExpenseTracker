<template>
  <div class="min-h-screen bg-gray-50">
    <div v-if="auth.isAuthenticated" class="flex">
      <Sidebar @add="showForm = true" />

      <!-- Mobile header -->
      <header class="fixed top-0 inset-x-0 z-10 md:hidden bg-white border-b border-gray-100 flex items-center justify-between px-4 py-3">
        <h1 class="text-lg font-bold text-gray-900">Expense Tracker</h1>
        <button type="button" aria-label="Log out" @click="handleLogout" class="text-red-500">
          <LogOut :size="20" />
        </button>
      </header>

      <main class="flex-1 pt-16 pb-24 md:pt-0 md:pb-0">
        <router-view />
      </main>

      <BottomNav @add="showForm = true" />
    </div>

    <router-view v-else />

    <!-- Modal -->
    <div
      v-if="showForm"
      class="fixed inset-0 bg-black/40 z-20 flex items-end md:items-center justify-center"
      @click.self="showForm = false"
    >
      <div class="bg-white w-full max-w-md rounded-t-2xl md:rounded-2xl p-6">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">Add Expense</h2>
        <ExpenseForm @cancel="showForm = false" @saved="showForm = false" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { LogOut } from '@lucide/vue'
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'
import BottomNav from './components/BottomNav.vue'
import ExpenseForm from './components/ExpenseForm.vue'

const auth = useAuthStore()
const router = useRouter()
const showForm = ref(false)

async function handleLogout() {
  const shouldLogout = window.confirm('Do you want to log out?')

  if (!shouldLogout) {
    return
  }

  auth.logout()
  await router.push('/login')
}
</script>