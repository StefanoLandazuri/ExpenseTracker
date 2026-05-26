<template>
  <div class="h-64 md:h-80">
    <canvas ref="canvas" />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { Chart, LineElement, PointElement, CategoryScale, LinearScale, Tooltip, LineController, Filler } from 'chart.js'

Chart.register(LineElement, PointElement, CategoryScale, LinearScale, Tooltip, LineController, Filler)

const props = defineProps<{
  data: { date: string; total: number }[]
}>()

const canvas = ref<HTMLCanvasElement | null>(null)
let chart: Chart | null = null

function buildChart() {
  if (!canvas.value) return
  if (chart) chart.destroy()

  // Mostrar solo cada 5 días en móvil
  const labels = props.data.map((d, i) => {
    const day = parseInt(d.date.slice(-2))
    return i % 5 === 0 ? String(day) : ''
  })

  chart = new Chart(canvas.value, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        data: props.data.map(d => d.total),
        borderColor: '#3b82f6',
        backgroundColor: 'rgba(59,130,246,0.1)',
        fill: true,
        tension: 0.4,
        pointRadius: 3,
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