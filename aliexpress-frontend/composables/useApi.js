// composables/useApi.js
import { useAuthStore } from "~/stores/modules/authStore";
import { useFetch } from "#app";

export function useApi(url, options = {}) {
    const authStore = useAuthStore();

    // Normalize URL: always starts with /api/v1/
    const apiUrl = url.startsWith("http")
        ? url
        : `/api/v1${url.startsWith("/") ? url : `/${url}`}`;

    // Default fetch options
    const defaultOptions = {
        baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
        credentials: "include", // send cookies (for refresh token HttpOnly cookie)
        headers: {
            "Content-Type": "application/json",
        },
        ...options,
    };

    // Add Authorization header if we have an access token
    if (authStore.tokens?.access) {
        defaultOptions.headers = {
            ...defaultOptions.headers,
            Authorization: `Bearer ${authStore.tokens.access}`,
        };
    }

    // Wrapper around useFetch
    async function fetchWithAuth() {
        const { data, error, status } = await useFetch(apiUrl, defaultOptions);

        // If 401 → try refresh
        if (status.value === 401 && authStore.tokens?.refresh) {
            try {
                const refreshResp = await useFetch("/api/v1/auth/refresh/", {
                    baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1",
                    method: "POST",
                    credentials: "include",
                    body: { refresh: authStore.tokens.refresh },
                });

                if (refreshResp.data.value?.access) {
                    // Update access token in store
                    authStore.setAccessToken(refreshResp.data.value.access);

                    // Retry original request with new token
                    defaultOptions.headers.Authorization = `Bearer ${refreshResp.data.value.access}`;
                    const retryResp = await useFetch(apiUrl, defaultOptions);

                    return {
                        data: retryResp.data.value,
                        error: retryResp.error.value,
                        status: retryResp.status.value,
                    };
                }
            } catch (refreshErr) {
                console.warn("Silent refresh failed → logging out", refreshErr);
                await authStore.logoutUser();
            }
        }

        return { data: data.value, error: error.value, status: status.value };
    }

    return fetchWithAuth();
}
