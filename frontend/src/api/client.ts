import axios from 'axios'

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
    withCredentials: true,
})

let accessToken: string | null = null

export function setAccessToken(token: string | null) {
    accessToken = token
}

export function getAccessToken(): string | null {
    return accessToken
}

// Request interceptor — agrega el token a cada request
api.interceptors.request.use((config) => {
    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config
})

// Response interceptor — reintenta con refresh ante 401
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const original = error.config

        // Si es 401 y no es el endpoint de refresh y no reintentamos ya
        if (
            error.response?.status === 401 &&
            !original._retry &&
            !original.url?.includes('/auth/refresh')
        ) {
            original._retry = true
            try {
                const res = await api.post('/auth/refresh')
                const newToken = res.data.access_token as string
                setAccessToken(newToken)
                original.headers.Authorization = `Bearer ${newToken}`
                return api(original)
            } catch {
                setAccessToken(null)
                if (!['/login', '/register'].includes(window.location.pathname)) {
                    window.location.href = '/login'
                }
            }
        }

        return Promise.reject(error)
    }
)

export default api