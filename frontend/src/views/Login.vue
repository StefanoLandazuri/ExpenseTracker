<template>
  <div class="min-h-screen bg-gray-50 flex items-center justify-center px-4">
    <div class="w-full max-w-sm">
      <h1 class="text-2xl font-bold text-center mb-8 text-gray-900">
        Expense Tracker
      </h1>

      <form @submit.prevent="handleLogin" class="bg-white rounded-2xl shadow-sm p-6 space-y-4">
        <h2 class="text-lg font-semibold text-gray-800">Sign in</h2>

        <div v-if="errorMsg" class="bg-red-50 text-red-600 text-sm rounded-lg px-4 py-3">
          {{ errorMsg }}
        </div>

        <div class="space-y-3">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-blue-600 text-white py-3 rounded-xl font-medium text-sm disabled:opacity-50"
        >
          {{ loading ? 'Signing in...' : 'Sign in' }}
        </button>

        <p class="text-center text-sm text-gray-500">
          No account?
          <router-link to="/register" class="text-blue-600 font-medium">Register</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

const ERROR_MESSAGES: Record<string, string> = {
  INVALID_CREDENTIALS: 'Invalid email or password.',
  EMAIL_ALREADY_EXISTS: 'This email is already registered.',
}

async function handleLogin() {
  errorMsg.value = ''

  if (!email.value || !password.value) {
    errorMsg.value = 'Please fill in all fields.'
    return
  }
  if (password.value.length < 8) {
    errorMsg.value = 'Password must be at least 8 characters.'
    return
  }

  loading.value = true
  try {
    await auth.login(email.value, password.value)
    await router.push('/dashboard')
  } catch (err: unknown) {
    const code = (err as { response?: { data?: { error?: { code?: string } } } })
      ?.response?.data?.error?.code
    errorMsg.value = (code && ERROR_MESSAGES[code]) ?? 'Something went wrong.'
  } finally {
    loading.value = false
  }
}
</script>