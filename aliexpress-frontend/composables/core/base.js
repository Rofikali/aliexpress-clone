
// // ~/composables/core/useApi.js
// import { useAuthStore } from "~/stores/modules/authStore";

// const breakers = new Map();
// let refreshingPromise = null;

// /** Utility: breaker key by endpoint */
// function getBreakerKey(url) {
//     const u = new URL(url, "http://dummy");
//     return u.pathname.split("?")[0];
// }

// /** Utility: jitter backoff */
// function getBackoffDelay(attempt) {
//     const base = Math.min(1000 * 2 ** attempt, 8000);
//     const jitter = Math.random() * 300;
//     return base + jitter;
// }

// /** Utility: normalize final response envelope */
// function makeResponse({ raw, error, status = 200 }) {
//     if (error) {
//         const message =
//             error?.data?.message || error?.message || "An unexpected error occurred";
//         const code = error?.status || status || 500;

//         return {
//             status: "error",
//             success: false,
//             code,
//             message,
//             request: error?.data?.request ?? null,
//             meta: error?.data?.meta ?? null,
//             errors: error?.data?.errors ?? [{ message, code }],
//             data: null,
//         };
//     }

//     const payload = raw?.data ?? null;
//     const meta = raw?.meta ?? {};
//     const errors = raw?.errors ?? null;

//     return {
//         status: raw?.status ?? "success",
//         success: raw?.success ?? true,
//         code: raw?.code ?? status ?? 200,
//         message: raw?.message ?? "",
//         request: raw?.request ?? null,
//         meta,
//         errors,
//         data: payload,
//     };
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

//     // --- Breaker helpers ---
//     function checkBreaker() {
//         const now = Date.now();
//         if (breaker.state === "OPEN") {
//             if (now >= breaker.openUntil) breaker.state = "HALF_OPEN";
//             else return makeResponse({
//                 error: { message: "Service unavailable (circuit breaker open)", status: 503 },
//                 status: 503,
//             });
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
//             console.warn(`[useApi] Breaker OPEN for ${breakerKey} until`, new Date(breaker.openUntil));
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
//         const breakerCheck = checkBreaker();
//         if (breakerCheck) return breakerCheck;

//         let attempt = 0;
//         const maxRetries = options.retries ?? 3;

//         while (attempt <= maxRetries) {
//             try {
//                 const controller = new AbortController();
//                 defaultOptions.signal = controller.signal;
//                 const timeoutId = setTimeout(() => controller.abort(), defaultOptions.timeout);

//                 const raw = await $fetch(apiUrl, defaultOptions);
//                 clearTimeout(timeoutId);

//                 recordSuccess();
//                 return makeResponse({ raw, status: 200 });
//             } catch (err) {
//                 clearTimeout(defaultOptions.timeout);

//                 // 401 → refresh
//                 if (err?.status === 401 && authStore.tokens?.refresh) {
//                     try {
//                         const newAccess = await handleRefresh();
//                         defaultOptions.headers.Authorization = `Bearer ${newAccess}`;
//                         const retryRaw = await $fetch(apiUrl, defaultOptions);
//                         recordSuccess();
//                         return makeResponse({ raw: retryRaw, status: 200 });
//                     } catch (refreshErr) {
//                         await authStore.logoutUser();
//                         recordFailure();
//                         return makeResponse({
//                             error: refreshErr,
//                             status: 401,
//                         });
//                     }
//                 }

//                 attempt++;
//                 if (attempt > maxRetries) {
//                     recordFailure();
//                     return makeResponse({ error: err, status: err?.status || 500 });
//                 }

//                 // exponential backoff + jitter
//                 const delay = getBackoffDelay(attempt);
//                 await new Promise((res) => setTimeout(res, delay));
//             }
//         }
//     }

//     return fetchWithAuth();
// }

// // ~/composables/core/base.js
// export function normalizeResponse(response) {
//   return {
//     success: response.success,
//     code: response.code,
//     message: response.message,
//     request: response.request || null,
//     meta: response.meta || null,
//       errors: response.errors || null,
//       data: response.data || null,
//   }
// }

// export function handleError(error) {
//   if (error.response?.data) return normalizeResponse(error.response.data)

//   return {
//     success: false,
//     code: error.response?.status || 500,
//     message: error.message || "Unknown error occurred",
//     request: null,
//     meta: null,
//     errors: null,
//     data: null,
//   }
// }

// ~/composables/core/base.js
export function normalizeResponse(payload) {
  return {
    success: payload.success ?? false,
    code: payload.code ?? null,
    message: payload.message ?? null,
    request: payload.request ?? null,
    meta: payload.meta ?? null,
    errors: payload.errors ?? null,
    data: payload.data ?? null,
  }
}

export function handleError(error) {
  if (error.response?.data) {
    return normalizeResponse(error.response.data)
  }

  return {
    success: false,
    code: error.response?.status || 500,
    message: error.message || "Unknown error occurred",
    request: null,
    meta: null,
    errors: null,
    data: null,
  }
}
