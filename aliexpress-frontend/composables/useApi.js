// // composables/useApi.js
// import { useAuthStore } from "~/stores/modules/authStore";
// import { useFetch } from "#app";

// export function useApi(url, options = {}) {
//     const authStore = useAuthStore();

//     // Normalize URL: always starts with /api/v1/
//     const apiUrl = url.startsWith("http")
//         ? url
//         : `/api/v1${url.startsWith("/") ? url : `/${url}`}`;

//     // Default fetch options
//     const defaultOptions = {
//         baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
//         credentials: "include", // send cookies (for refresh token HttpOnly cookie)
//         headers: {
//             "Content-Type": "application/json",
//         },
//         ...options,
//     };

//     // Add Authorization header if we have an access token
//     if (authStore.tokens?.access) {
//         defaultOptions.headers = {
//             ...defaultOptions.headers,
//             Authorization: `Bearer ${authStore.tokens.access}`,
//         };
//     }

//     // Wrapper around useFetch
//     async function fetchWithAuth() {
//         const { data, error, status } = await useFetch(apiUrl, defaultOptions);

//         // If 401 → try refresh
//         if (status.value === 401 && authStore.tokens?.refresh) {
//             try {
//                 const refreshResp = await useFetch("/api/v1/auth/refresh/", {
//                     baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1",
//                     method: "POST",
//                     credentials: "include",
//                     body: { refresh: authStore.tokens.refresh },
//                 });

//                 if (refreshResp.data.value?.access) {
//                     // Update access token in store
//                     authStore.setAccessToken(refreshResp.data.value.access);

//                     // Retry original request with new token
//                     defaultOptions.headers.Authorization = `Bearer ${refreshResp.data.value.access}`;
//                     const retryResp = await useFetch(apiUrl, defaultOptions);

//                     return {
//                         data: retryResp.data.value,
//                         error: retryResp.error.value,
//                         status: retryResp.status.value,
//                     };
//                 }
//             } catch (refreshErr) {
//                 console.warn("Silent refresh failed → logging out", refreshErr);
//                 await authStore.logoutUser();
//             }
//         }

//         return { data: data.value, error: error.value, status: status.value };
//     }

//     return fetchWithAuth();
// }


// composables/useApi.js
import { useAuthStore } from "~/stores/modules/authStore";
import { useFetch } from "#app";

// --- Circuit Breaker State (scoped to backend API) ---
const circuitBreaker = {
    failures: 0,
    state: "CLOSED", // CLOSED | OPEN | HALF_OPEN
    openUntil: null,
    threshold: 5,       // failures before opening
    cooldown: 10000,    // ms to stay open before trying half-open
};

export function useApi(url, options = {}) {
    const authStore = useAuthStore();

    // Normalize URL: always starts with /api/v1/
    const apiUrl = url.startsWith("http")
        ? url
        : `/api/v1${url.startsWith("/") ? url : `/${url}`}`;

    const defaultOptions = {
        baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000",
        credentials: "include", // include cookies
        headers: {
            "Content-Type": "application/json",
        },
        ...options,
    };

    // Add auth header if token exists
    if (authStore.tokens?.access) {
        defaultOptions.headers = {
            ...defaultOptions.headers,
            Authorization: `Bearer ${authStore.tokens.access}`,
        };
    }

    // --- Circuit Breaker Guard ---
    function checkBreaker() {
        const now = Date.now();

        if (circuitBreaker.state === "OPEN") {
            if (now >= circuitBreaker.openUntil) {
                // Cooldown passed → allow test request
                circuitBreaker.state = "HALF_OPEN";
            } else {
                throw new Error("Service temporarily unavailable (circuit breaker open)");
            }
        }
    }

    function recordSuccess() {
        circuitBreaker.failures = 0;
        circuitBreaker.state = "CLOSED";
        circuitBreaker.openUntil = null;
    }

    function recordFailure() {
        circuitBreaker.failures += 1;
        if (circuitBreaker.failures >= circuitBreaker.threshold) {
            circuitBreaker.state = "OPEN";
            circuitBreaker.openUntil = Date.now() + circuitBreaker.cooldown;
            console.warn("[useApi] Circuit breaker OPEN until", new Date(circuitBreaker.openUntil));
        }
    }

    // --- Core fetch with retries ---
    async function fetchWithAuth() {
        checkBreaker();

        let attempt = 0;
        const maxRetries = options.retries ?? 3;

        while (attempt <= maxRetries) {
            try {
                const { data, error, status } = await useFetch(apiUrl, defaultOptions);

                if (error.value) throw error.value;

                // 401 → try refresh
                if (status.value === 401 && authStore.tokens?.refresh) {
                    try {
                        const refreshResp = await useFetch("/api/v1/auth/refresh/", {
                            baseURL: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1",
                            method: "POST",
                            credentials: "include",
                            body: { refresh: authStore.tokens.refresh },
                        });

                        if (refreshResp.data.value?.access) {
                            authStore.setAccessToken(refreshResp.data.value.access);

                            defaultOptions.headers.Authorization = `Bearer ${refreshResp.data.value.access}`;
                            const retryResp = await useFetch(apiUrl, defaultOptions);

                            if (retryResp.error.value) throw retryResp.error.value;

                            recordSuccess();
                            return {
                                data: retryResp.data.value,
                                error: null,
                                status: retryResp.status.value,
                            };
                        }
                    } catch (refreshErr) {
                        console.warn("[useApi] Silent refresh failed → logging out", refreshErr);
                        await authStore.logoutUser();
                        recordFailure();
                        throw refreshErr;
                    }
                }

                // ✅ Success
                recordSuccess();
                return { data: data.value, error: null, status: status.value };

            } catch (err) {
                attempt++;

                if (attempt > maxRetries) {
                    recordFailure();
                    throw err;
                }

                // Exponential backoff
                const backoff = Math.min(1000 * 2 ** attempt, 8000);
                await new Promise(res => setTimeout(res, backoff));
            }
        }
    }

    return fetchWithAuth();
}
