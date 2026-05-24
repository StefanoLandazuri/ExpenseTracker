<template>
  <div v-if="!auth.isHydrated" class="min-h-screen flex items-center justify-center bg-slate-950 text-slate-100">
    <div class="text-center space-y-3">
      <div class="mx-auto h-10 w-10 animate-spin rounded-full border-2 border-slate-500 border-t-slate-100"></div>
      <p class="text-sm text-slate-300">Loading your session...</p>
    </div>
  </div>
  <router-view v-else />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from './stores/auth'

const auth = useAuthStore()

onMounted(() => {
  void auth.init()
})
</script>