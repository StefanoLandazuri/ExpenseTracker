<template>
  <div class="min-h-screen bg-gray-50">
    <div v-if="auth.isAuthenticated" class="flex">
      <Sidebar />
      <main class="flex-1 pb-24 md:pb-0">
        <router-view />
      </main>

      <!-- FAB -->
      <button
        @click="showForm = true"
        class="fixed bottom-20 right-4 md:bottom-8 md:right-8 w-14 h-14 bg-blue-600 text-white rounded-full shadow-lg text-2xl flex items-center justify-center z-10"
      >
        +
      </button>

      <BottomNav />
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
import { useAuthStore } from './stores/auth'
import Sidebar from './components/Sidebar.vue'
import BottomNav from './components/BottomNav.vue'
import ExpenseForm from './components/ExpenseForm.vue'

const auth = useAuthStore()
const showForm = ref(false)
</script>