// ~/middleware/guest.global.js
import { useAuthStore } from "~/stores/modules/authStore"

export default defineNuxtRouteMiddleware((to) => {
    const auth = useAuthStore()

    // if logged in, block access to login/register
    // if (auth.tokens?.access) {
    //     if (to.path === "/auth/login/" || to.path === "/auth/register/") {
    //         return navigateTo("/auth/profile/")
    //     }
    // }
})
