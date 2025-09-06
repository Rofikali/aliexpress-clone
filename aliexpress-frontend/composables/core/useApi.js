// composables/core/useApi.js
import { useAuthStore } from "~/stores/modules/authStore";
import { useFetch } from "#app";

const breakers = new Map(); // per-endpoint circuit breakers
let refreshingPromise = null; // single refresh queue

export function useApi(url, options = {}) {
    const config = useRuntimeConfig();
    const authStore = useAuthStore();

    // Normalize URL: always starts with /api/v1/
    const apiUrl = url.startsWith("http")
        ? url
        : `/api/v1${url.startsWith("/") ? url : `/${url}`}`;

    // --- Circuit breaker setup ---
    if (!breakers.has(apiUrl)) {
        breakers.set(apiUrl, {
            failures: 0,
            state: "CLOSED", // CLOSED | OPEN | HALF_OPEN
            openUntil: null,
            threshold: 5,
            cooldown: 10000,
        });
    }
    const breaker = breakers.get(apiUrl);

    const defaultOptions = {
        baseURL: config.public.apiBase || "http://localhost:8000/api/v1",
        headers: { "Content-Type": "application/json" },
        method: "GET",
        timeout: 10000, // default timeout 10s
        ...options,
    };

    if (authStore.tokens?.access) {
        defaultOptions.headers.Authorization = `Bearer ${authStore.tokens.access}`;
    }

    // --- Circuit Breaker Guard ---
    function checkBreaker() {
        const now = Date.now();
        if (breaker.state === "OPEN") {
            if (now >= breaker.openUntil) breaker.state = "HALF_OPEN";
            else throw new Error("Service temporarily unavailable (circuit breaker open)");
        }
    }

    function recordSuccess() {
        breaker.failures = 0;
        breaker.state = "CLOSED";
        breaker.openUntil = null;
    }

    function recordFailure() {
        breaker.failures += 1;
        if (breaker.failures >= breaker.threshold) {
            breaker.state = "OPEN";
            breaker.openUntil = Date.now() + breaker.cooldown;
            console.warn(`[useApi] Circuit breaker OPEN for ${apiUrl} until`, new Date(breaker.openUntil));
        }
    }

    // --- Refresh token helper ---
    async function handleRefresh() {
        if (!refreshingPromise) {
            refreshingPromise = (async () => {
                const refreshResp = await useFetch("/refresh/", {
                    baseURL: config.public.apiBase || "http://localhost:8000/api/v1",
                    method: "POST",
                    body: { refresh: authStore.tokens.refresh },
                    headers: { "Content-Type": "application/json" },
                });
                if (!refreshResp.data.value?.access) throw new Error("Refresh failed");
                authStore.setAccessToken(refreshResp.data.value.access);
                refreshingPromise = null;
                return refreshResp.data.value.access;
            })();
        }
        return refreshingPromise;
    }

    // --- Core fetch with retries, timeout, and abort support ---
    async function fetchWithAuth() {
        checkBreaker();
        const controller = new AbortController();
        defaultOptions.signal = controller.signal;

        let attempt = 0;
        const maxRetries = options.retries ?? 3;

        while (attempt <= maxRetries) {
            try {
                const timeoutPromise = new Promise((_, reject) =>
                    setTimeout(() => reject(new Error("Request timed out")), defaultOptions.timeout)
                );

                const fetchPromise = useFetch(apiUrl, defaultOptions);
                const { data, error, status } = await Promise.race([fetchPromise, timeoutPromise]);

                if (error.value) throw error.value;

                // 401 → try refresh
                if (status.value === 401 && authStore.tokens?.refresh) {
                    try {
                        const newAccess = await handleRefresh();
                        defaultOptions.headers.Authorization = `Bearer ${newAccess}`;

                        const retryResp = await useFetch(apiUrl, defaultOptions);
                        if (retryResp.error.value) throw retryResp.error.value;

                        recordSuccess();
                        return { data: retryResp.data.value, status: retryResp.status.value, error: null };
                    } catch (refreshErr) {
                        console.warn("[useApi] Silent refresh failed → logging out", refreshErr);
                        await authStore.logoutUser();
                        recordFailure();
                        throw refreshErr;
                    }
                }

                // Retry only network errors or 5xx
                if (status.value >= 500 || !status.value) throw error.value || new Error("Network/Server error");

                // ✅ Success
                recordSuccess();
                return { data: data.value, status: status.value, error: null };

            } catch (err) {
                attempt++;
                if (attempt > maxRetries) {
                    recordFailure();
                    throw err;
                }
                // exponential backoff
                const backoff = Math.min(1000 * 2 ** attempt, 8000);
                await new Promise(res => setTimeout(res, backoff));
            }
        }
    }

    return fetchWithAuth();
}
