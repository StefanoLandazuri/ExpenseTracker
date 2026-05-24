import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import ExpenseList from '../views/ExpenseList.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', redirect: '/dashboard' },
        { path: '/login', component: Login },
        { path: '/register', component: Register },
        {
            path: '/dashboard',
            component: Dashboard,
            meta: { requiresAuth: true },
        },
        {
            path: '/expenses',
            component: ExpenseList,
            meta: { requiresAuth: true },
        },
        { path: '/:pathMatch(.*)*', redirect: '/dashboard' },
    ],
})

router.beforeEach(async (to) => {
    const auth = useAuthStore()

    if (!auth.isHydrated) {
        await auth.init()
    }

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
        return '/login'
    }

    if ((to.path === '/login' || to.path === '/register') && auth.isAuthenticated) {
        return '/dashboard'
    }
})

export default router