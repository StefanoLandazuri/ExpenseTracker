import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'
import type { Expense, ExpenseCreate, ExpenseSummary } from '../types/api'

export const useExpensesStore = defineStore('expenses', () => {
  const expenses = ref<Expense[]>([])
  const summary = ref<ExpenseSummary | null>(null)
  const currentMonth = ref(new Date().toISOString().slice(0, 7))
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchExpenses(month?: string) {
    loading.value = true
    error.value = null
    try {
      const m = month ?? currentMonth.value
      const res = await api.get(`/expenses?month=${m}`)
      expenses.value = (res.data.expenses as Expense[]).sort(
        (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
      )
    } catch {
      error.value = 'Failed to load expenses.'
    } finally {
      loading.value = false
    }
  }

  async function createExpense(data: ExpenseCreate) {
    const res = await api.post('/expenses', data)
    expenses.value.unshift(res.data as Expense)
  }

  async function deleteExpense(id: string, date: string) {
    await api.delete(`/expenses/${id}?date=${date}`)
    expenses.value = expenses.value.filter(e => e.id !== id)
  }

  async function fetchSummary(month?: string) {
    const m = month ?? currentMonth.value
    const res = await api.get(`/expenses/summary?month=${m}`)
    summary.value = res.data as ExpenseSummary
  }

  function setMonth(month: string) {
    currentMonth.value = month
  }

  return {
    expenses, summary, currentMonth, loading, error,
    fetchExpenses, createExpense, deleteExpense, fetchSummary, setMonth,
  }
})