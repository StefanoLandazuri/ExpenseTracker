<template>
  <nav class="fixed bottom-0 inset-x-0 md:hidden bg-white border-t border-gray-100 flex">
    <router-link
      v-for="item in navItems"
      :key="item.path"
      :to="item.path"
      class="flex-1 flex flex-col items-center justify-center py-3 text-xs font-medium"
      :class="route.path === item.path ? 'text-blue-600' : 'text-gray-400'"
    >
      <component :is="item.icon" :size="22" class="mb-1" />
      {{ item.label }}
    </router-link>

    <button
      type="button"
      aria-label="Add expense"
      @click="emit('add')"
      class="absolute z-10 left-1/2 top-0 -translate-x-1/2 -translate-y-1/2 w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg flex items-center justify-center"
    >
      <Plus :size="26" />
    </button>
  </nav>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { LayoutDashboard, Wallet, Plus } from '@lucide/vue'

const route = useRoute()

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/expenses', label: 'Expenses', icon: Wallet },
]

const emit = defineEmits<{ add: [] }>()
</script>