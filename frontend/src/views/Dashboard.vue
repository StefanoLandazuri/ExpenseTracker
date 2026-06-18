<template>
  <div class="px-4 py-6 max-w-4xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-gray-900">Dashboard</h1>
      <input
        v-model="store.currentMonth"
        type="month"
        class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        @change="loadData"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div class="bg-white rounded-2xl p-6 animate-pulse h-32" />
      <div class="bg-white rounded-2xl p-6 animate-pulse h-64" />
      <div class="bg-white rounded-2xl p-6 animate-pulse h-64" />
    </div>

    <!-- Empty state -->
    <div v-else-if="!store.summary || parseFloat(store.summary.total) === 0" class="text-center py-20">
      <LayoutDashboard :size="40" class="mx-auto mb-3 text-gray-300" />
      <p class="text-gray-500 font-medium">No expenses this month</p>
      <p class="text-gray-400 text-sm">Tap + to add some</p>
    </div>

    <div v-else class="space-y-4">
      <!-- Total -->
      <div class="bg-white rounded-2xl p-6 shadow-sm">
        <p class="text-sm text-gray-500 mb-1">Total this month</p>
        <p class="text-5xl font-bold text-gray-900">${{ store.summary.total }}</p>
        <p v-if="previousTotal !== null" class="text-sm mt-2" :class="changeColor">
          {{ changeLabel }} vs last month
        </p>
      </div>

      <!-- Charts grid -->
      <div class="grid md:grid-cols-2 gap-4">
        <div class="bg-white rounded-2xl p-4 shadow-sm">
          <h2 class="text-sm font-semibold text-gray-700 mb-3">By category</h2>
          <ChartBar :data="categoryData" />
        </div>

        <div class="bg-white rounded-2xl p-4 shadow-sm">
          <h2 class="text-sm font-semibold text-gray-700 mb-3">By day</h2>
          <ChartLine :data="dayData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { LayoutDashboard } from '@lucide/vue'
import { useExpensesStore } from '../stores/expenses'
import { useAuthStore } from '../stores/auth'
import ChartBar from '../components/ChartBar.vue'
import ChartLine from '../components/ChartLine.vue'
import api from '../api/client'
import type { Category } from '../types/api'

const store = useExpensesStore()
const auth = useAuthStore()
const loading = ref(false)
const previousTotal = ref<number | null>(null)

const categoryData = computed(() => {
  if (!store.summary) return {}
  const result: Partial<Record<Category, number>> = {}
  for (const [k, v] of Object.entries(store.summary.by_category)) {
    result[k as Category] = parseFloat(v)
  }
  return result
})

const dayData = computed(() => {
  if (!store.summary) return []
  return store.summary.by_day.map(d => ({
    date: d.date,
    total: parseFloat(d.total),
  }))
})

const changeLabel = computed(() => {
  if (previousTotal.value === null || !store.summary) return ''
  const current = parseFloat(store.summary.total)
  const prev = previousTotal.value
  if (prev === 0) return ''
  const pct = (((current - prev) / prev) * 100).toFixed(0)
  return parseFloat(pct) >= 0 ? `+${pct}%` : `${pct}%`
})

const changeColor = computed(() => {
  if (!changeLabel.value) return 'text-gray-400'
  return changeLabel.value.startsWith('+') ? 'text-red-500' : 'text-green-500'
})

async function loadData() {
  loading.value = true
  try {
    await store.fetchSummary(store.currentMonth)

    // Mes anterior
    const [year, month] = store.currentMonth.split('-').map(Number)
    const prevDate = new Date(year, (month ?? 1) - 2, 1)
    const prevMonth = prevDate.toISOString().slice(0, 7)
    const res = await api.get(`/expenses/summary?month=${prevMonth}`)
    previousTotal.value = parseFloat(res.data.total)
  } catch {
    // silencioso
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (auth.isAuthenticated) loadData()
})

watch(
  () => store.dashboardRefreshToken,
  () => {
    if (auth.isAuthenticated) loadData()
  }
)
</script>