<template>
  <div class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
      <input
        v-model="form.amount"
        type="text"
        inputmode="decimal"
        autocomplete="off"
        placeholder="0.00"
        class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
      <div class="grid grid-cols-4 gap-2">
        <button
          v-for="(meta, key) in CATEGORY_META"
          :key="key"
          @click="form.category = key"
          :class="[
            'flex flex-col items-center py-2 px-1 rounded-xl border text-xs font-medium transition-colors',
            form.category === key
              ? 'border-blue-500 bg-blue-50 text-blue-700'
              : 'border-gray-200 text-gray-600'
          ]"
        >
          <span class="text-lg mb-1">{{ meta.emoji }}</span>
          {{ meta.label }}
        </button>
      </div>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
      <input
        v-model="form.date"
        type="date"
        class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Description <span class="text-gray-400">(optional)</span></label>
      <textarea
        v-model="form.description"
        maxlength="200"
        rows="2"
        placeholder="What was it for?"
        class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
      />
    </div>

    <div v-if="errorMsg" class="bg-red-50 text-red-600 text-sm rounded-lg px-4 py-3">
      {{ errorMsg }}
    </div>

    <div class="flex gap-3 pt-2">
      <button
        @click="$emit('cancel')"
        class="flex-1 border border-gray-200 text-gray-700 py-3 rounded-xl font-medium text-sm"
      >
        Cancel
      </button>
      <button
        @click="handleSubmit"
        :disabled="loading"
        class="flex-1 bg-blue-600 text-white py-3 rounded-xl font-medium text-sm disabled:opacity-50"
      >
        {{ loading ? 'Saving...' : 'Save' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useExpensesStore } from '../stores/expenses'
import { CATEGORY_META } from '../utils/categories'
import type { Category } from '../types/api'

const emit = defineEmits<{
  cancel: []
  saved: []
}>()

const store = useExpensesStore()

const today = new Date().toISOString().slice(0, 10)

const form = ref({
  amount: '',
  category: 'food' as Category,
  date: today,
  description: '',
})

const loading = ref(false)
const errorMsg = ref('')

function normalizeAmount(value: string) {
  return value.trim().replace(',', '.')
}

async function handleSubmit() {
  errorMsg.value = ''

  const normalizedAmount = normalizeAmount(form.value.amount)

  if (!normalizedAmount || Number(normalizedAmount) <= 0) {
    errorMsg.value = 'Please enter a valid amount.'
    return
  }

  loading.value = true
  try {
    await store.createExpense({
      amount: normalizedAmount,
      category: form.value.category,
      date: form.value.date,
      description: form.value.description || undefined,
    })
    emit('saved')
  } catch {
    errorMsg.value = 'Failed to save expense.'
  } finally {
    loading.value = false
  }
}
</script>