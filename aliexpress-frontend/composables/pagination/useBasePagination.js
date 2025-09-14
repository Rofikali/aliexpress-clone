
// 14-09-2025 working fine 
// ~/composables/pagination/useBasePagination.js
// import { ref, computed } from "vue"
// import { useNuxtApp } from "#app"

// export function usePagination(url, options = {}) {
//     const { $api } = useNuxtApp()

//     const products = ref([])
//     const nextCursor = ref(null)
//     const hasNext = ref(true)
//     const loading = ref(false)
//     const error = ref(null)

//     const pageSize = options.pageSize || 10
//     const dedupeKey = options.dedupeKey || "id"
//     const retries = options.retries || 0
//     const retryBackoffMs = options.retryBackoffMs || 300
//     const debug = !!options.debug

//     let currentAbort = null
//     let inFlight = false

//     const count = computed(() => products.value.length)

//     // 🔄 Reset state (like store.reset)
//     const reset = () => {
//         products.value = []
//         nextCursor.value = null
//         hasNext.value = true
//         error.value = null
//         try { currentAbort?.abort() } catch { }
//         currentAbort = null
//         console.log("🔄 [usePagination] state reset")
//     }

//     async function _request(params = {}, attempt = 0) {
//         if (currentAbort) {
//             try { currentAbort.abort() } catch { }
//             currentAbort = null
//         }
//         currentAbort = new AbortController()
//         const signal = currentAbort.signal

//         if (debug) console.log("🌐 [usePagination] Request start:", url, params)

//         try {
//             const resp = await $api.get(url, {
//                 params: { ...params, page_size: pageSize },
//                 signal,
//             })
//             if (debug) console.info("✅ [usePagination] Request success:", resp)
//             return resp
//         } catch (err) {
//             if (signal?.aborted) {
//                 console.warn("⚠️ [usePagination] Request aborted")
//                 throw err
//             }
//             if (attempt < retries) {
//                 const backoff = retryBackoffMs * Math.pow(2, attempt)
//                 console.warn(`[usePagination] Retry attempt ${attempt + 1} in ${backoff}ms`, err)
//                 await new Promise(r => setTimeout(r, backoff))
//                 return _request(params, attempt + 1)
//             }
//             console.error("❌ [usePagination] Request failed:", err)
//             throw err
//         }
//     }

//     // 📥 First fetch (like store.fetchFirst)
//     async function fetchFirst(params = {}) {
//         console.info("🚀 [usePagination] fetchFirst called", params)
//         reset()
//         loading.value = true
//         inFlight = true
//         error.value = null

//         try {
//             const response = await _request(params)

//             if (!response.success) {
//                 error.value = response.errors || [{ message: response.message }]
//                 return response
//             }

//             products.value = response.data || []
//             nextCursor.value = response.meta?.next_cursor ?? response.next_cursor ?? null
//             hasNext.value = response.meta?.has_next ?? response.has_next ?? false

//             console.info(`✅ [usePagination] Initial load: ${products.value.length} products`)
//             return response
//         } catch (err) {
//             error.value = err
//             console.error("[usePagination] fetchFirst error", err)
//             // throw err
//             return error.value
//         } finally {
//             loading.value = false
//             inFlight = false
//         }
//     }

//     // ➕ Load more (like store.loadMore)
//     async function loadMore(params = {}) {
//         console.info("📥 [usePagination] loadMore called", params)

//         if (!hasNext.value) {
//             console.warn("[usePagination] No more items to load")
//             return
//         }
//         if (loading.value || inFlight) {
//             console.warn("[usePagination] Already loading, skipping loadMore")
//             return
//         }

//         loading.value = true
//         inFlight = true
//         error.value = null

//         try {
//             const requestParams = { ...params }
//             if (nextCursor.value) requestParams.cursor = nextCursor.value

//             const response = await _request(requestParams)

//             if (!response.success) {
//                 error.value = response.errors || [{ message: response.message }]
//                 return response
//             }

//             const newProducts = Array.isArray(response.data)
//                 ? response.data
//                 : response.data
//                     ? [response.data]
//                     : []

//             // ✅ Deduplicate (same as store)
//             const map = new Map(products.value.map(p => [p[dedupeKey], p]))
//             for (const item of newProducts) map.set(item[dedupeKey], item)
//             products.value = Array.from(map.values())

//             nextCursor.value = response.meta?.next_cursor ?? response.next_cursor ?? null
//             hasNext.value = response.meta?.has_next ?? response.has_next ?? false

//             console.info(`✅ [usePagination] loadMore success. Added=${newProducts.length}, Total=${products.value.length}, hasNext=${hasNext.value}`)
//             return response
//         } catch (err) {
//             error.value = err
//             console.error("[usePagination] loadMore error", err)
//             throw err
//         } finally {
//             loading.value = false
//             inFlight = false
//         }
//     }

//     // ♻️ Force reload (just reset+fetchFirst)
//     async function forceReload(params = {}) {
//         console.info("♻️ [usePagination] forceReload called")
//         reset()
//         return fetchFirst(params)
//     }

//     if (options.autoFetch !== false) {
//         fetchFirst().catch(e => { console.warn("[usePagination] autoFetch failed", e) })
//     }

//     return {
//         // variables
//         products,
//         nextCursor,
//         hasNext,
//         loading,
//         error,
//         count,
//         // functions
//         fetchFirst,
//         loadMore,
//         reset,
//         forceReload,
//         _debug: () => ({ inFlight, aborted: currentAbort?.signal?.aborted ?? false }),
//     }
// }


// ~/composables/pagination/useBasePagination.js
import { ref, computed } from "vue"

export function usePagination(transportFn, options = {}) {
    const items = ref([])
    const nextCursor = ref(null)
    const hasNext = ref(true)
    const loading = ref(false)
    const error = ref(null)

    const pageSize = options.pageSize || 12
    const dedupeKey = options.dedupeKey || "id"
    const retries = options.retries || 0
    const retryBackoffMs = options.retryBackoffMs || 300
    const debug = !!options.debug

    let currentAbort = null
    let inFlight = false

    const count = computed(() => items.value.length)

    // 🔄 Reset state
    const reset = () => {
        items.value = []
        nextCursor.value = null
        hasNext.value = true
        error.value = null
        try { currentAbort?.abort() } catch { }
        currentAbort = null
        console.log("🔄 [usePagination] state reset")
    }

    // 🌐 Internal request wrapper (with retry + backoff)
    async function _request(params = {}, attempt = 0) {
        if (debug) console.log("🌐 [usePagination] Request start:", params)

        try {
            const resp = await transportFn({ ...params, page_size: pageSize })

            if (debug) console.info("✅ [usePagination] TransportFn response:", resp)

            if (!resp.success) {
                // error returned by transport
                throw resp
            }

            return resp
        } catch (err) {
            if (attempt < retries) {
                const backoff = retryBackoffMs * Math.pow(2, attempt)
                console.warn(`[usePagination] Retry attempt ${attempt + 1} in ${backoff}ms`, err)
                await new Promise(r => setTimeout(r, backoff))
                return _request(params, attempt + 1)
            }
            console.error("❌ [usePagination] Request failed:", err)
            throw err
        }
    }

    // 📥 First fetch
    async function fetchFirst(params = {}) {
        console.info("🚀 [usePagination] fetchFirst called", params)
        reset()
        loading.value = true
        inFlight = true
        error.value = null

        try {
            const response = await _request(params)

            items.value = response.data || []
            nextCursor.value = response.meta?.next_cursor ?? null
            hasNext.value = response.meta?.has_next ?? false

            console.info(`✅ [usePagination] Initial load: ${items.value.length} items`)
            return response
        } catch (err) {
            error.value = err
            console.error("[usePagination] fetchFirst error", err)
            return err
        } finally {
            loading.value = false
            inFlight = false
        }
    }

    // ➕ Load more
    async function loadMore(params = {}) {
        console.info("📥 [usePagination] loadMore called", params)

        if (!hasNext.value) {
            console.warn("[usePagination] No more items to load")
            return
        }
        if (loading.value || inFlight) {
            console.warn("[usePagination] Already loading, skipping loadMore")
            return
        }

        loading.value = true
        inFlight = true
        error.value = null

        try {
            const requestParams = { ...params }
            if (nextCursor.value) requestParams.cursor = nextCursor.value

            const response = await _request(requestParams)

            const newItems = Array.isArray(response.data)
                ? response.data
                : response.data ? [response.data] : []

            // ✅ Deduplicate
            const map = new Map(items.value.map(p => [p[dedupeKey], p]))
            for (const item of newItems) map.set(item[dedupeKey], item)
            items.value = Array.from(map.values())

            nextCursor.value = response.meta?.next_cursor ?? null
            hasNext.value = response.meta?.has_next ?? false

            console.info(`✅ [usePagination] loadMore success. Added=${newItems.length}, Total=${items.value.length}, hasNext=${hasNext.value}`)
            return response
        } catch (err) {
            error.value = err
            console.error("[usePagination] loadMore error", err)
            return err
        } finally {
            loading.value = false
            inFlight = false
        }
    }

    // ♻️ Force reload
    async function forceReload(params = {}) {
        console.info("♻️ [usePagination] forceReload called")
        reset()
        return fetchFirst(params)
    }

    if (options.autoFetch !== false) {
        fetchFirst().catch(e => { console.warn("[usePagination] autoFetch failed", e) })
    }

    return {
        // state
        items,
        nextCursor,
        hasNext,
        loading,
        error,
        count,
        // actions
        fetchFirst,
        loadMore,
        reset,
        forceReload,
        _debug: () => ({ inFlight, aborted: currentAbort?.signal?.aborted ?? false }),
    }
}
