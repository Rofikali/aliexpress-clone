// ~/middleware/auth.global.js
import { useAuthStore } from "~/stores/modules/authStore"

export default defineNuxtRouteMiddleware((to) => {
    const auth = useAuthStore()

    // if not logged in AND trying to access a protected page
    if (!auth.tokens?.access) {
        // prevent infinite loop: don't redirect if already on login/register
        // if (to.path !== "/auth/login/" && to.path !== "/auth/register/") {
        return navigateTo("/auth/login/")
        // }
    }
})
