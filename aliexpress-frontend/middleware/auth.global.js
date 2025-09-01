import { useAuthStore } from "~/stores/modules/authStore";

export default defineNuxtRouteMiddleware(async (to, from) => {
    const authStore = useAuthStore();

    // Hydrate store state (in case of SSR or hard refresh)
    if (!authStore.isHydrated) {
        await authStore.checkAuth(); // verify token from cookie/localStorage
    }

    // Public routes that don't need login
    const publicRoutes = ["/login", "/register", "/"];

    if (!authStore.isAuthenticated && !publicRoutes.includes(to.path)) {
        return navigateTo("/login");
    }
});
