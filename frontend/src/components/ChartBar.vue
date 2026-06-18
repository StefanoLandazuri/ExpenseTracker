<template>
  <div class="h-64 md:h-80">
    <canvas ref="canvas" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, BarElement, CategoryScale, LinearScale, Tooltip, BarController } from 'chart.js'
import type { Category } from '../types/api'
import { CATEGORY_META } from '../utils/categories'

Chart.register(BarElement, CategoryScale, LinearScale, Tooltip, BarController)

const props = defineProps<{
  data: Partial<Record<Category, number>>
}>()

const canvas = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

function buildChart() {
  if (!canvas.value) return

  const categories = Object.keys(props.data) as Category[]
  const filtered = categories.filter(c => (props.data[c] ?? 0) > 0)

  if (chart) chart.destroy()

  chart = new Chart(canvas.value, {
    type: 'bar',
    data: {
      labels: filtered.map(c => CATEGORY_META[c].label),
      datasets: [{
        data: filtered.map(c => props.data[c] ?? 0),
        backgroundColor: filtered.map(c => CATEGORY_META[c].chartColor),
        borderColor: filtered.map(c => CATEGORY_META[c].chartColor),
        borderWidth: 1,
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        x: { ticks: { font: { size: 11 } } },
        y: { beginAtZero: true },
      },
    },
  })
}

onMounted(buildChart)
watch(() => props.data, buildChart, { deep: true })
</script>