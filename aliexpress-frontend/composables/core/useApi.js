// // // // composables/core/useApi.js
// // // import { useAuthStore } from "~/stores/modules/authStore";
// // // import { useFetch } from "#app";

// // // const breakers = new Map(); // per-endpoint circuit breakers
// // // let refreshingPromise = null; // single refresh queue

// // // export function useApi(url, options = {}) {
// // //     const config = useRuntimeConfig();
// // //     const authStore = useAuthStore();

// // //     // Normalize URL: always starts with /api/v1/
// // //     const apiUrl = config.public.apiBase
// // //     // const apiUrl = url.startsWith("http")
// // //     // ? url
// // //     // : `/api/v1${url.startsWith("/") ? url : `/${url}`}`;

// // //     // --- Circuit breaker setup ---
// // //     if (!breakers.has(apiUrl)) {
// // //         breakers.set(apiUrl, {
// // //             failures: 0,
// // //             state: "CLOSED", // CLOSED | OPEN | HALF_OPEN
// // //             openUntil: null,
// // //             threshold: 5,
// // //             cooldown: 350,
// // //         });
// // //     }
// // //     const breaker = breakers.get(apiUrl);

// // //     const defaultOptions = {
// // //         baseURL: apiUrl || "http://localhost:8000/api/v1",
// // //         headers: { "Content-Type": "application/json" },
// // //         method: "GET",
// // //         timeout: 10000, // default timeout 10s
// // //         ...options,
// // //     };

// // //     if (authStore.tokens?.access) {
// // //         defaultOptions.headers.Authorization = `Bearer ${authStore.tokens.access}`;
// // //     }

// // //     // --- Circuit Breaker Guard ---
// // //     function checkBreaker() {
// // //         const now = Date.now();
// // //         if (breaker.state === "OPEN") {
// // //             if (now >= breaker.openUntil) breaker.state = "HALF_OPEN";
// // //             else throw new Error("Service temporarily unavailable (circuit breaker open)");
// // //         }
// // //     }

// // //     function recordSuccess() {
// // //         breaker.failures = 0;
// // //         breaker.state = "CLOSED";
// // //         breaker.openUntil = null;
// // //     }

// // //     function recordFailure() {
// // //         breaker.failures += 1;
// // //         if (breaker.failures >= breaker.threshold) {
// // //             breaker.state = "OPEN";
// // //             breaker.openUntil = Date.now() + breaker.cooldown;
// // //             console.warn(`[useApi] Circuit breaker OPEN for ${apiUrl} until`, new Date(breaker.openUntil));
// // //         }
// // //     }

// // //     // --- Refresh token helper ---
// // //     async function handleRefresh() {
// // //         if (!refreshingPromise) {
// // //             refreshingPromise = (async () => {
// // //                 const refreshResp = await useFetch("/refresh/", {
// // //                     baseURL: config.public.apiBase || "http://localhost:8000/api/v1",
// // //                     method: "POST",
// // //                     body: { refresh: authStore.tokens.refresh },
// // //                     headers: { "Content-Type": "application/json" },
// // //                 });
// // //                 if (!refreshResp.data.value?.access) throw new Error("Refresh failed");
// // //                 authStore.setAccessToken(refreshResp.data.value.access);
// // //                 refreshingPromise = null;
// // //                 return refreshResp.data.value.access;
// // //             })();
// // //         }
// // //         return refreshingPromise;
// // //     }

// // //     // --- Core fetch with retries, timeout, and abort support ---
// // //     async function fetchWithAuth() {
// // //         checkBreaker();
// // //         const controller = new AbortController();
// // //         defaultOptions.signal = controller.signal;

// // //         let attempt = 0;
// // //         const maxRetries = options.retries ?? 3;

// // //         while (attempt <= maxRetries) {
// // //             try {
// // //                 const timeoutPromise = new Promise((_, reject) =>
// // //                     setTimeout(() => reject(new Error("Request timed out")), defaultOptions.timeout)
// // //                 );

// // //                 const fetchPromise = useFetch(apiUrl, defaultOptions);
// // //                 const { data, error, status } = await Promise.race([fetchPromise, timeoutPromise]);

// // //                 if (error.value) throw error.value;

// // //                 // 401 → try refresh
// // //                 if (status.value === 401 && authStore.tokens?.refresh) {
// // //                     try {
// // //                         const newAccess = await handleRefresh();
// // //                         defaultOptions.headers.Authorization = `Bearer ${newAccess}`;

// // //                         const retryResp = await useFetch(apiUrl, defaultOptions);
// // //                         if (retryResp.error.value) throw retryResp.error.value;

// // //                         recordSuccess();
// // //                         return { data: retryResp.data.value, status: retryResp.status.value, error: null };
// // //                     } catch (refreshErr) {
// // //                         console.warn("[useApi] Silent refresh failed → logging out", refreshErr);
// // //                         await authStore.logoutUser();
// // //                         recordFailure();
// // //                         throw refreshErr;
// // //                     }
// // //                 }

// // //                 // Retry only network errors or 5xx
// // //                 if (status.value >= 500 || !status.value) throw error.value || new Error("Network/Server error");

// // //                 // ✅ Success
// // //                 recordSuccess();
// // //                 return { data: data.value, status: status.value, error: null };

// // //             } catch (err) {
// // //                 attempt++;
// // //                 if (attempt > maxRetries) {
// // //                     recordFailure();
// // //                     throw err;
// // //                 }
// // //                 // exponential backoff
// // //                 const backoff = Math.min(1000 * 2 ** attempt, 8000);
// // //                 await new Promise(res => setTimeout(res, backoff));
// // //             }
// // //         }
// // //     }

// // //     return fetchWithAuth();
// // // }

// // // 10-09-2025

// // // composables/core/useApi.js
// // import { useAuthStore } from "~/stores/modules/authStore";

// // const breakers = new Map();
// // let refreshingPromise = null;

// // export function useApi(url, options = {}) {
// //     const config = useRuntimeConfig();
// //     const authStore = useAuthStore();

// //     if (!url || typeof url !== "string") {
// //         throw new Error(`[useApi] Invalid URL: ${url}`);
// //     }

// //     // Normalize URL
// //     const base = config.public.apiBase || "http://localhost:8000/api/v1";
// //     const apiUrl = url.startsWith("http")
// //         ? url
// //         : `${base}${url.startsWith("/") ? url : `/${url}`}`;

// //     // --- Circuit breaker setup ---
// //     if (!breakers.has(apiUrl)) {
// //         breakers.set(apiUrl, {
// //             failures: 0,
// //             state: "CLOSED",
// //             openUntil: null,
// //             threshold: 5,
// //             cooldown: 10000,
// //         });
// //     }
// //     const breaker = breakers.get(apiUrl);

// //     const defaultOptions = {
// //         method: "GET",
// //         headers: { "Content-Type": "application/json" },
// //         timeout: 10000,
// //         ...options,
// //     };

// //     if (authStore.tokens?.access) {
// //         defaultOptions.headers.Authorization = `Bearer ${authStore.tokens.access}`;
// //     }

// //     // --- Circuit Breaker Guards ---
// //     function checkBreaker() {
// //         const now = Date.now();
// //         if (breaker.state === "OPEN") {
// //             if (now >= breaker.openUntil) breaker.state = "HALF_OPEN";
// //             else throw new Error("Service temporarily unavailable (circuit breaker open)");
// //         }
// //     }

// //     function recordSuccess() {
// //         breaker.failures = 0;
// //         breaker.state = "CLOSED";
// //         breaker.openUntil = null;
// //     }

// //     function recordFailure() {
// //         breaker.failures++;
// //         if (breaker.failures >= breaker.threshold) {
// //             breaker.state = "OPEN";
// //             breaker.openUntil = Date.now() + breaker.cooldown;
// //             console.warn(`[useApi] Circuit breaker OPEN for ${apiUrl} until`, new Date(breaker.openUntil));
// //         }
// //     }

// //     // --- Refresh token helper ---
// //     async function handleRefresh() {
// //         if (!refreshingPromise) {
// //             refreshingPromise = (async () => {
// //                 const refreshResp = await $fetch("/refresh/", {
// //                     baseURL: base,
// //                     method: "POST",
// //                     body: { refresh: authStore.tokens.refresh },
// //                     headers: { "Content-Type": "application/json" },
// //                 });
// //                 if (!refreshResp?.access) throw new Error("Refresh failed");
// //                 authStore.setAccessToken(refreshResp.access);
// //                 refreshingPromise = null;
// //                 return refreshResp.access;
// //             })();
// //         }
// //         return refreshingPromise;
// //     }

// //     // --- Core fetch ---
// //     async function fetchWithAuth() {
// //         checkBreaker();

// //         let attempt = 0;
// //         const maxRetries = options.retries ?? 3;

// //         while (attempt <= maxRetries) {
// //             try {
// //                 const controller = new AbortController();
// //                 defaultOptions.signal = controller.signal;

// //                 const timeout = setTimeout(() => controller.abort(), defaultOptions.timeout);

// //                 const res = await $fetch(apiUrl, defaultOptions);
// //                 clearTimeout(timeout);

// //                 recordSuccess();
// //                 return { data: res, status: 200, error: null };

// //             } catch (err) {
// //                 clearTimeout(defaultOptions.timeout);

// //                 // 401 → try refresh
// //                 if (err?.status === 401 && authStore.tokens?.refresh) {
// //                     try {
// //                         const newAccess = await handleRefresh();
// //                         defaultOptions.headers.Authorization = `Bearer ${newAccess}`;
// //                         const retryRes = await $fetch(apiUrl, defaultOptions);
// //                         recordSuccess();
// //                         return { data: retryRes, status: 200, error: null };
// //                     } catch (refreshErr) {
// //                         await authStore.logoutUser();
// //                         recordFailure();
// //                         throw refreshErr;
// //                     }
// //                 }

// //                 attempt++;
// //                 if (attempt > maxRetries) {
// //                     recordFailure();
// //                     throw err;
// //                 }

// //                 // exponential backoff
// //                 const backoff = Math.min(1000 * 2 ** attempt, 8000);
// //                 await new Promise(res => setTimeout(res, backoff));
// //             }
// //         }
// //     }

// //     return fetchWithAuth();
// // }

// // ~/composables/core/useApi.js
// import { useAuthStore } from "~/stores/modules/authStore";

// const breakers = new Map();
// let refreshingPromise = null;

// /**
//  * Extract a breaker key from URL (endpoint-level granularity).
//  * Example: "/products?page=2" -> "/products"
//  */
// function getBreakerKey(url) {
//     const u = new URL(url, "http://dummy"); // fallback base for relative URLs
//     return u.pathname.split("?")[0]; // ignore query params
// }

// /**
//  * Standardize error object
//  */
// function formatError(err, defaultMsg = "Request failed") {
//     if (err?.status) {
//         return {
//             message: err?.data?.detail || err.message || defaultMsg,
//             code: err.status,
//             retriable: err.status >= 500, // 5xx = safe to retry
//         };
//     }
//     return {
//         message: err?.message || defaultMsg,
//         code: "NETWORK_ERROR",
//         retriable: true,
//     };
// }

// /**
//  * Apply jitter to exponential backoff
//  */
// function getBackoffDelay(attempt) {
//     const base = Math.min(1000 * 2 ** attempt, 8000);
//     const jitter = Math.random() * 300; // ±300ms
//     return base + jitter;
// }

// export function useApi(url, options = {}) {
//     const config = useRuntimeConfig();
//     const authStore = useAuthStore();

//     if (!url || typeof url !== "string") {
//         throw new Error(`[useApi] Invalid URL: ${url}`);
//     }

//     // Normalize URL
//     const base = config.public.apiBase || "http://localhost:8000/api/v1";
//     const apiUrl = url.startsWith("http")
//         ? url
//         : `${base}${url.startsWith("/") ? url : `/${url}`}`;

//     const breakerKey = getBreakerKey(apiUrl);

//     // --- Circuit breaker setup ---
//     if (!breakers.has(breakerKey)) {
//         breakers.set(breakerKey, {
//             failures: 0,
//             state: "CLOSED",
//             openUntil: null,
//             threshold: 5,
//             cooldown: 10000,
//         });
//     }
//     const breaker = breakers.get(breakerKey);

//     const defaultOptions = {
//         method: "GET",
//         headers: { "Content-Type": "application/json" },
//         timeout: 10000,
//         ...options,
//     };

//     if (authStore.tokens?.access) {
//         defaultOptions.headers.Authorization = `Bearer ${authStore.tokens.access}`;
//     }

//     // --- Circuit Breaker Guards ---
//     function checkBreaker() {
//         const now = Date.now();
//         if (breaker.state === "OPEN") {
//             if (now >= breaker.openUntil) breaker.state = "HALF_OPEN";
//             else throw formatError(null, "Service temporarily unavailable (circuit breaker open)");
//         }
//     }

//     function recordSuccess() {
//         breaker.failures = 0;
//         breaker.state = "CLOSED";
//         breaker.openUntil = null;
//     }

//     function recordFailure() {
//         breaker.failures++;
//         if (breaker.failures >= breaker.threshold) {
//             breaker.state = "OPEN";
//             breaker.openUntil = Date.now() + breaker.cooldown;
//             console.warn(`[useApi] Circuit breaker OPEN for ${breakerKey} until`, new Date(breaker.openUntil));
//         }
//     }

//     // --- Refresh token helper ---
//     async function handleRefresh() {
//         if (!refreshingPromise) {
//             refreshingPromise = (async () => {
//                 try {
//                     const refreshResp = await $fetch("/refresh/", {
//                         baseURL: base,
//                         method: "POST",
//                         body: { refresh: authStore.tokens.refresh },
//                         headers: { "Content-Type": "application/json" },
//                     });
//                     if (!refreshResp?.access) throw new Error("Refresh failed");
//                     authStore.setAccessToken(refreshResp.access);
//                     return refreshResp.access;
//                 } finally {
//                     refreshingPromise = null;
//                 }
//             })();
//         }
//         return refreshingPromise;
//     }

//     // --- Core fetch ---
//     async function fetchWithAuth() {
//         checkBreaker();

//         let attempt = 0;
//         const maxRetries = options.retries ?? 3;

//         while (attempt <= maxRetries) {
//             try {
//                 const controller = new AbortController();
//                 defaultOptions.signal = controller.signal;
//                 const timeoutId = setTimeout(() => controller.abort(), defaultOptions.timeout);

//                 const res = await $fetch(apiUrl, defaultOptions);
//                 clearTimeout(timeoutId);

//                 recordSuccess();

//                 return { data: res, status: 200, error: null };
//             } catch (err) {
//                 const formattedError = formatError(err);

//                 // 401 → try refresh
//                 if (err?.status === 401 && authStore.tokens?.refresh) {
//                     try {
//                         const newAccess = await handleRefresh();
//                         defaultOptions.headers.Authorization = `Bearer ${newAccess}`;
//                         const retryRes = await $fetch(apiUrl, defaultOptions);
//                         recordSuccess();
//                         return { data: retryRes, status: 200, error: null };
//                     } catch (refreshErr) {
//                         await authStore.logoutUser();
//                         recordFailure();
//                         return { data: null, status: 401, error: formatError(refreshErr, "Auth refresh failed") };
//                     }
//                 }

//                 attempt++;
//                 if (attempt > maxRetries) {
//                     recordFailure();
//                     return { data: null, status: formattedError.code, error: formattedError };
//                 }

//                 // exponential backoff w/ jitter
//                 const delay = getBackoffDelay(attempt);
//                 await new Promise((res) => setTimeout(res, delay));
//             }
//         }
//     }

//     return fetchWithAuth();
// }



// ~/composables/core/useApi.js
import { useAuthStore } from "~/stores/modules/authStore";

const breakers = new Map();
let refreshingPromise = null;

/** Utility: breaker key by endpoint */
function getBreakerKey(url) {
    const u = new URL(url, "http://dummy");
    return u.pathname.split("?")[0];
}

/** Utility: jitter backoff */
function getBackoffDelay(attempt) {
    const base = Math.min(1000 * 2 ** attempt, 8000);
    const jitter = Math.random() * 300;
    return base + jitter;
}

/** Utility: normalize final response envelope */
function makeResponse({ raw, error, status = 200 }) {
    if (error) {
        const message =
            error?.data?.message || error?.message || "An unexpected error occurred";
        const code = error?.status || status || 500;

        return {
            status: "error",
            success: false,
            code,
            message,
            request: error?.data?.request ?? null,
            meta: error?.data?.meta ?? null,
            errors: error?.data?.errors ?? [{ message, code }],
            data: null,
        };
    }

    const payload = raw?.data ?? null;
    const meta = raw?.meta ?? {};
    const errors = raw?.errors ?? null;

    return {
        status: raw?.status ?? "success",
        success: raw?.success ?? true,
        code: raw?.code ?? status ?? 200,
        message: raw?.message ?? "",
        request: raw?.request ?? null,
        meta,
        errors,
        data: payload,
    };
}

export function useApi(url, options = {}) {
    const config = useRuntimeConfig();
    const authStore = useAuthStore();

    if (!url || typeof url !== "string") {
        throw new Error(`[useApi] Invalid URL: ${url}`);
    }

    // Normalize URL
    const base = config.public.apiBase || "http://localhost:8000/api/v1";
    const apiUrl = url.startsWith("http")
        ? url
        : `${base}${url.startsWith("/") ? url : `/${url}`}`;

    const breakerKey = getBreakerKey(apiUrl);

    // --- Circuit breaker setup ---
    if (!breakers.has(breakerKey)) {
        breakers.set(breakerKey, {
            failures: 0,
            state: "CLOSED",
            openUntil: null,
            threshold: 5,
            cooldown: 10000,
        });
    }
    const breaker = breakers.get(breakerKey);

    const defaultOptions = {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        timeout: 10000,
        ...options,
    };

    if (authStore.tokens?.access) {
        defaultOptions.headers.Authorization = `Bearer ${authStore.tokens.access}`;
    }

    // --- Breaker helpers ---
    function checkBreaker() {
        const now = Date.now();
        if (breaker.state === "OPEN") {
            if (now >= breaker.openUntil) breaker.state = "HALF_OPEN";
            else return makeResponse({
                error: { message: "Service unavailable (circuit breaker open)", status: 503 },
                status: 503,
            });
        }
    }

    function recordSuccess() {
        breaker.failures = 0;
        breaker.state = "CLOSED";
        breaker.openUntil = null;
    }

    function recordFailure() {
        breaker.failures++;
        if (breaker.failures >= breaker.threshold) {
            breaker.state = "OPEN";
            breaker.openUntil = Date.now() + breaker.cooldown;
            console.warn(`[useApi] Breaker OPEN for ${breakerKey} until`, new Date(breaker.openUntil));
        }
    }

    // --- Refresh token helper ---
    async function handleRefresh() {
        if (!refreshingPromise) {
            refreshingPromise = (async () => {
                try {
                    const refreshResp = await $fetch("/refresh/", {
                        baseURL: base,
                        method: "POST",
                        body: { refresh: authStore.tokens.refresh },
                        headers: { "Content-Type": "application/json" },
                    });
                    if (!refreshResp?.access) throw new Error("Refresh failed");
                    authStore.setAccessToken(refreshResp.access);
                    return refreshResp.access;
                } finally {
                    refreshingPromise = null;
                }
            })();
        }
        return refreshingPromise;
    }

    // --- Core fetch ---
    async function fetchWithAuth() {
        const breakerCheck = checkBreaker();
        if (breakerCheck) return breakerCheck;

        let attempt = 0;
        const maxRetries = options.retries ?? 3;

        while (attempt <= maxRetries) {
            try {
                const controller = new AbortController();
                defaultOptions.signal = controller.signal;
                const timeoutId = setTimeout(() => controller.abort(), defaultOptions.timeout);

                const raw = await $fetch(apiUrl, defaultOptions);
                clearTimeout(timeoutId);

                recordSuccess();
                return makeResponse({ raw, status: 200 });
            } catch (err) {
                clearTimeout(defaultOptions.timeout);

                // 401 → refresh
                if (err?.status === 401 && authStore.tokens?.refresh) {
                    try {
                        const newAccess = await handleRefresh();
                        defaultOptions.headers.Authorization = `Bearer ${newAccess}`;
                        const retryRaw = await $fetch(apiUrl, defaultOptions);
                        recordSuccess();
                        return makeResponse({ raw: retryRaw, status: 200 });
                    } catch (refreshErr) {
                        await authStore.logoutUser();
                        recordFailure();
                        return makeResponse({
                            error: refreshErr,
                            status: 401,
                        });
                    }
                }

                attempt++;
                if (attempt > maxRetries) {
                    recordFailure();
                    return makeResponse({ error: err, status: err?.status || 500 });
                }

                // exponential backoff + jitter
                const delay = getBackoffDelay(attempt);
                await new Promise((res) => setTimeout(res, delay));
            }
        }
    }

    return fetchWithAuth();
}
