<template>
  <div class="px-4 py-6 max-w-2xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-xl font-bold text-gray-900">Expenses</h1>
      <input
        v-model="store.currentMonth"
        type="month"
        class="border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        @change="store.fetchExpenses(store.currentMonth)"
      />
    </div>

    <!-- Loading -->
    <div v-if="store.loading" class="space-y-3">
      <div v-for="i in 3" :key="i" class="bg-white rounded-2xl p-4 animate-pulse">
        <div class="h-4 bg-gray-200 rounded w-1/3 mb-2" />
        <div class="h-3 bg-gray-100 rounded w-1/2" />
      </div>
    </div>

    <!-- Empty state -->
    <div v-else-if="store.expenses.length === 0" class="text-center py-20">
      <p class="text-4xl mb-3">💸</p>
      <p class="text-gray-500 font-medium">No expenses yet</p>
      <p class="text-gray-400 text-sm">Tap + to add one</p>
    </div>

    <!-- List -->
    <div v-else class="space-y-3">
      <div
        v-for="expense in store.expenses"
        :key="expense.id"
        class="bg-white rounded-2xl p-4 flex items-center gap-3 shadow-sm"
      >
        <span
          :class="['text-2xl w-10 h-10 flex items-center justify-center rounded-xl', CATEGORY_META[expense.category].color]"
        >
          {{ CATEGORY_META[expense.category].emoji }}
        </span>

        <div class="flex-1 min-w-0">
          <p class="font-medium text-gray-900 text-sm">
            {{ CATEGORY_META[expense.category].label }}
          </p>
          <p class="text-gray-400 text-xs truncate">
            {{ expense.description ?? expense.date }}
          </p>
        </div>

        <div class="text-right">
          <p class="font-semibold text-gray-900">${{ expense.amount }}</p>
          <button
            @click="confirmDelete(expense)"
            class="text-red-400 text-xs mt-1"
          >
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Delete modal -->
    <div
      v-if="expenseToDelete"
      class="fixed inset-0 bg-black/40 z-20 flex items-center justify-center px-4"
      @click.self="expenseToDelete = null"
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-sm">
        <h3 class="font-semibold text-gray-900 mb-2">Delete expense?</h3>
        <p class="text-gray-500 text-sm mb-6">This action cannot be undone.</p>
        <div class="flex gap-3">
          <button
            @click="expenseToDelete = null"
            class="flex-1 border border-gray-200 py-2.5 rounded-xl text-sm font-medium"
          >
            Cancel
          </button>
          <button
            @click="handleDelete"
            class="flex-1 bg-red-500 text-white py-2.5 rounded-xl text-sm font-medium"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useExpensesStore } from '../stores/expenses'
import { CATEGORY_META } from '../utils/categories'
import type { Expense } from '../types/api'

const store = useExpensesStore()
const expenseToDelete = ref<Expense | null>(null)

onMounted(() => store.fetchExpenses())

function confirmDelete(expense: Expense) {
  expenseToDelete.value = expense
}

async function handleDelete() {
  if (!expenseToDelete.value) return
  await store.deleteExpense(expenseToDelete.value.id, expenseToDelete.value.date)
  expenseToDelete.value = null
}
</script>