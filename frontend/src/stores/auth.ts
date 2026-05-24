import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api, { setAccessToken } from '../api/client'
import type { User } from '../types/api'

const ACCESS_TOKEN_KEY = 'expense-tracker.access-token'

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const accessToken = ref<string | null>(null)
    const isHydrated = ref(false)
    let initPromise: Promise<void> | null = null

    const isAuthenticated = computed(() => accessToken.value !== null)

    function syncAccessToken(token: string | null) {
        accessToken.value = token
        setAccessToken(token)

        if (typeof window !== 'undefined') {
            if (token) {
                window.localStorage.setItem(ACCESS_TOKEN_KEY, token)
            } else {
                window.localStorage.removeItem(ACCESS_TOKEN_KEY)
            }
        }
    }

    function setSession(token: string, currentUser: User) {
        syncAccessToken(token)
        user.value = currentUser
    }

    async function login(email: string, password: string) {
        const res = await api.post('/auth/login', { email, password })
        setSession(res.data.access_token as string, res.data.user as User)
    }

    async function register(email: string, password: string) {
        const res = await api.post('/auth/register', { email, password })
        setSession(res.data.access_token as string, res.data.user as User)
    }

    async function refresh() {
        const res = await api.post('/auth/refresh')
        syncAccessToken(res.data.access_token as string)

        // Traer datos del usuario con el nuevo token
        const meRes = await api.get('/auth/me')
        user.value = meRes.data as User
    }

    async function init() {
        if (isHydrated.value) {
            return
        }

        if (!initPromise) {
            initPromise = (async () => {
                if (typeof window !== 'undefined') {
                    const storedToken = window.localStorage.getItem(ACCESS_TOKEN_KEY)
                    if (storedToken) {
                        syncAccessToken(storedToken)
                    }
                }

                try {
                    if (accessToken.value) {
                        const meRes = await api.get('/auth/me')
                        user.value = meRes.data as User
                    } else {
                        await refresh()
                    }
                } catch {
                    logout()
                } finally {
                    isHydrated.value = true
                    initPromise = null
                }
            })()
        }

        await initPromise
    }

    function logout() {
        user.value = null
        syncAccessToken(null)
    }

    return { user, accessToken, isAuthenticated, isHydrated, init, login, register, refresh, logout }
})