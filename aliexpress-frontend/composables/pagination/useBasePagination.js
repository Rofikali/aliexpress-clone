

// // // ~/composables/pagination/useBasePagination.js
// // import { ref, computed } from 'vue'
// // import axios from '~/plugins/axios' // matches your existing import pattern

// // /**
// //  * Production-ready cursor pagination composable
// //  *
// //  * Exposes:
// //  *  - products, loading, error, hasNext, nextCursor, count
// //  *  - fetchFirst(params), loadMore(), reset(params), forceReload()
// //  *
// //  * Options:
// //  *  - pageSize (default 10)
// //  *  - dedupeKey (default 'id') -- used to de-duplicate appended products
// //  *  - retries (default 0), retryBackoffMs (default 300)
// //  *  - autoFetch (default true)
// //  *  - debug (bool)
// //  */
// // export function usePagination(url, options = {}) {
// //     const $axios = axiosFactory().provide.instance


// //     const products = ref([])
// //     const nextCursor = ref(null)
// //     const hasNext = ref(true)
// //     const loading = ref(false)
// //     const error = ref(null)

// //     const pageSize = options.pageSize || 10
// //     const dedupeKey = options.dedupeKey || 'id'
// //     const retries = (options.retries || 0)
// //     const retryBackoffMs = options.retryBackoffMs || 300
// //     const debug = !!options.debug

// //     // AbortController to cancel in-flight requests on new calls (modern browsers)
// //     let currentAbort = null
// //     let inFlight = false

// //     const count = computed(() => products.value.length)

// //     function _dedupeAppend(existing, incoming) {
// //         if (!dedupeKey) return existing.concat(incoming)
// //         const map = new Map()
// //         for (const r of existing) map.set(r[dedupeKey], r)
// //         for (const r of incoming) map.set(r[dedupeKey], r)
// //         return Array.from(map.values())
// //     }

// //     async function _request(params = {}, attempt = 0) {
// //         if (currentAbort) {
// //             try { currentAbort.abort() } catch (e) { /* ignore */ }
// //             currentAbort = null
// //         }
// //         currentAbort = new AbortController()
// //         const signal = currentAbort.signal

// //         try {
// //             const resp = await $axios.get(url, {
// //                 params: { ...params, page_size: pageSize },
// //                 signal
// //             })
// //             return resp.data
// //         } catch (err) {
// //             // don't retry on explicit abort
// //             if (signal && signal.aborted) {
// //                 if (debug) console.warn('pagination request aborted')
// //                 throw err
// //             }
// //             if (attempt < retries) {
// //                 const backoff = retryBackoffMs * Math.pow(2, attempt)
// //                 if (debug) console.warn(`retry attempt ${attempt + 1} in ${backoff}ms`, err)
// //                 await new Promise(r => setTimeout(r, backoff))
// //                 return _request(params, attempt + 1)
// //             }
// //             throw err
// //         } finally {
// //             // keep currentAbort for possible cancellation; do not null here so consumer can check aborted
// //         }
// //     }

// //     async function fetchFirst(params = {}) {
// //         loading.value = true
// //         error.value = null
// //         inFlight = true
// //         try {
// //             const data = await _request({ ...params })
// //             // support multiple response shapes
// //             const items = data.products || data.products || []
// //             products.value = Array.isArray(items) ? items : []
// //             nextCursor.value = data.next_cursor ?? null
// //             hasNext.value = !!data.has_next ?? (nextCursor.value !== null)
// //             return products.value
// //         } catch (err) {
// //             error.value = err
// //             if (debug) console.error('[usePagination] fetchFirst error', err)
// //             throw err
// //         } finally {
// //             loading.value = false
// //             inFlight = false
// //         }
// //     }

// //     async function loadMore(params = {}) {
// //         if (!hasNext.value || loading.value || inFlight) return
// //         loading.value = true
// //         error.value = null
// //         inFlight = true
// //         try {
// //             const requestParams = { ...params }
// //             if (nextCursor.value) requestParams.cursor = nextCursor.value
// //             const data = await _request(requestParams)
// //             const newItems = data.products || data.products || []
// //             // append with dedupe
// //             products.value = _dedupeAppend(products.value, Array.isArray(newItems) ? newItems : [])
// //             nextCursor.value = data.next_cursor ?? null
// //             hasNext.value = !!data.has_next ?? (nextCursor.value !== null && (Array.isArray(newItems) ? newItems.length > 0 : true))
// //             return newItems
// //         } catch (err) {
// //             error.value = err
// //             if (debug) console.error('[usePagination] loadMore error', err)
// //             throw err
// //         } finally {
// //             loading.value = false
// //             inFlight = false
// //         }
// //     }

// //     async function reset(params = {}) {
// //         // cancel in-flight
// //         try { currentAbort?.abort() } catch (e) { }
// //         currentAbort = null
// //         products.value = []
// //         nextCursor.value = null
// //         hasNext.value = true
// //         error.value = null
// //         return fetchFirst(params)
// //     }

// //     async function forceReload(params = {}) {
// //         // convenience to forcibly re-fetch current first page without clearing if preferred.
// //         return reset(params)
// //     }

// //     // auto-fetch unless explicitly disabled
// //     if (options.autoFetch !== false) {
// //         // do not await here (caller can await fetchFirst)
// //         fetchFirst().catch(e => { if (debug) console.warn('autofetch failed', e) })
// //     }

// //     return {
// //         products,
// //         nextCursor,
// //         hasNext,
// //         loading,
// //         error,
// //         count,
// //         fetchFirst,
// //         loadMore,
// //         reset,
// //         forceReload,
// //         // debug/diagnostics
// //         _debug: () => ({ inFlight, aborted: currentAbort?.signal?.aborted ?? false })
// //     }
// // }




// // ~/composables/pagination/useBasePagination.js
// import { ref, computed } from 'vue'
// // import axios from '~/plugins/axios' // matches your existing import pattern
// import { useNuxtApp } from '#app'

// /**
//  * Production-ready cursor pagination composable
//  *
//  * Exposes:
//  *  - products, loading, error, hasNext, nextCursor, count
//  *  - fetchFirst(params), loadMore(), reset(params), forceReload()
//  *
//  * Options:
//  *  - pageSize (default 10)
//  *  - dedupeKey (default 'id') -- used to de-duplicate appended products
//  *  - retries (default 0), retryBackoffMs (default 300)
//  *  - autoFetch (default true)
//  *  - debug (bool)
//  */
// export function usePagination(url, options = {}) {
//     const { $api } = useNuxtApp()


//     const products = ref([])
//     const nextCursor = ref(null)
//     const hasNext = ref(true)
//     const loading = ref(false)
//     const error = ref(null)

//     const pageSize = options.pageSize || 10
//     const dedupeKey = options.dedupeKey || 'id'
//     const retries = (options.retries || 0)
//     const retryBackoffMs = options.retryBackoffMs || 300
//     const debug = !!options.debug

//     // AbortController to cancel in-flight requests on new calls (modern browsers)
//     let currentAbort = null
//     let inFlight = false

//     const count = computed(() => products.value.length)

//     function _dedupeAppend(existing, incoming) {
//         if (!dedupeKey) return existing.concat(incoming)
//         const map = new Map()
//         for (const r of existing) map.set(r[dedupeKey], r)
//         for (const r of incoming) map.set(r[dedupeKey], r)
//         return Array.from(map.values())
//     }

//     async function _request(params = {}, attempt = 0) {
//         if (currentAbort) {
//             try { currentAbort.abort() } catch (e) { /* ignore */ }
//             currentAbort = null
//         }
//         currentAbort = new AbortController()
//         const signal = currentAbort.signal

//         try {
//             const resp = await $api.get(url, {
//                 params: { ...params, page_size: pageSize },
//                 signal
//             })
//             return resp.data
//         } catch (err) {
//             // don't retry on explicit abort
//             if (signal && signal.aborted) {
//                 if (debug) console.warn('pagination request aborted')
//                 throw err
//             }
//             if (attempt < retries) {
//                 const backoff = retryBackoffMs * Math.pow(2, attempt)
//                 if (debug) console.warn(`retry attempt ${attempt + 1} in ${backoff}ms`, err)
//                 await new Promise(r => setTimeout(r, backoff))
//                 return _request(params, attempt + 1)
//             }
//             throw err
//         } finally {
//             // keep currentAbort for possible cancellation; do not null here so consumer can check aborted
//         }
//     }

//     async function fetchFirst(params = {}) {
//         loading.value = true
//         error.value = null
//         inFlight = true
//         try {
//             const data = await _request({ ...params })
//             // support multiple response shapes
//             const items = data.products || data.products || []
//             products.value = Array.isArray(items) ? items : []
//             nextCursor.value = data.next_cursor ?? null
//             hasNext.value = !!data.has_next ?? (nextCursor.value !== null)
//             return products.value
//         } catch (err) {
//             error.value = err
//             if (debug) console.error('[usePagination] fetchFirst error', err)
//             throw err
//         } finally {
//             loading.value = false
//             inFlight = false
//         }
//     }

//     async function loadMore(params = {}) {
//         if (!hasNext.value || loading.value || inFlight) return
//         loading.value = true
//         error.value = null
//         inFlight = true
//         try {
//             const requestParams = { ...params }
//             if (nextCursor.value) requestParams.cursor = nextCursor.value
//             const data = await _request(requestParams)
//             const newItems = data.products || data.products || []
//             // append with dedupe
//             products.value = _dedupeAppend(products.value, Array.isArray(newItems) ? newItems : [])
//             nextCursor.value = data.next_cursor ?? null
//             hasNext.value = !!data.has_next ?? (nextCursor.value !== null && (Array.isArray(newItems) ? newItems.length > 0 : true))
//             return newItems
//         } catch (err) {
//             error.value = err
//             if (debug) console.error('[usePagination] loadMore error', err)
//             throw err
//         } finally {
//             loading.value = false
//             inFlight = false
//         }
//     }

//     async function reset(params = {}) {
//         // cancel in-flight
//         try { currentAbort?.abort() } catch (e) { }
//         currentAbort = null
//         products.value = []
//         nextCursor.value = null
//         hasNext.value = true
//         error.value = null
//         return fetchFirst(params)
//     }

//     async function forceReload(params = {}) {
//         // convenience to forcibly re-fetch current first page without clearing if preferred.
//         return reset(params)
//     }

//     // auto-fetch unless explicitly disabled
//     if (options.autoFetch !== false) {
//         // do not await here (caller can await fetchFirst)
//         fetchFirst().catch(e => { if (debug) console.warn('autofetch failed', e) })
//     }

//     return {
//         products,
//         nextCursor,
//         hasNext,
//         loading,
//         error,
//         count,
//         fetchFirst,
//         loadMore,
//         reset,
//         forceReload,
//         // debug/diagnostics
//         _debug: () => ({ inFlight, aborted: currentAbort?.signal?.aborted ?? false })
//     }
// }

// ~/composables/pagination/useBasePagination.js
import { ref, computed } from "vue"
import { useNuxtApp } from "#app"

export function usePagination(url, options = {}) {
    const { $api } = useNuxtApp()

    const products = ref([])
    const nextCursor = ref(null)
    const hasNext = ref(true)
    const loading = ref(false)
    const error = ref(null)

    const pageSize = options.pageSize || 10
    const dedupeKey = options.dedupeKey || "id"
    const retries = options.retries || 0
    const retryBackoffMs = options.retryBackoffMs || 300
    const debug = !!options.debug

    let currentAbort = null
    let inFlight = false

    const count = computed(() => products.value.length)

    function _dedupeAppend(existing, incoming) {
        if (!dedupeKey) return existing.concat(incoming)
        const map = new Map()
        for (const r of existing) map.set(r[dedupeKey], r)
        for (const r of incoming) map.set(r[dedupeKey], r)
        return Array.from(map.values())
    }

    async function _request(params = {}, attempt = 0) {
        if (currentAbort) {
            try { currentAbort.abort() } catch { }
            currentAbort = null
        }
        currentAbort = new AbortController()
        const signal = currentAbort.signal

        if (debug) console.log("🌐 [usePagination] Request start:", url, params)

        try {
            const resp = await $api.get(url, {
                params: { ...params, page_size: pageSize },
                signal,
            })
            if (debug) console.info("✅ [usePagination] Request success:", resp)
            return resp
        } catch (err) {
            if (signal?.aborted) {
                console.warn("⚠️ [usePagination] Request aborted")
                throw err
            }
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

    async function fetchFirst(params = {}) {
        console.info("🚀 [usePagination] fetchFirst called", params)
        loading.value = true
        error.value = null
        inFlight = true
        try {
            const data = await _request(params)
            const items = data.products || data.data || []
            products.value = Array.isArray(items) ? items : []
            nextCursor.value = data.next_cursor ?? null
            hasNext.value = !!data.has_next ?? (nextCursor.value !== null)
            console.info(`[usePagination] fetchFirst success. Loaded=${products.value.length}, hasNext=${hasNext.value}`)
            return products.value
        } catch (err) {
            error.value = err
            console.error("[usePagination] fetchFirst error", err)
            throw err
        } finally {
            loading.value = false
            inFlight = false
        }
    }

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
        error.value = null
        inFlight = true
        try {
            const requestParams = { ...params }
            if (nextCursor.value) requestParams.cursor = nextCursor.value
            const data = await _request(requestParams)
            const newItems = data.products || data.data || []
            products.value = _dedupeAppend(products.value, Array.isArray(newItems) ? newItems : [])
            nextCursor.value = data.next_cursor ?? null
            hasNext.value = !!data.has_next ?? (nextCursor.value !== null && newItems.length > 0)
            console.info(`[usePagination] loadMore success. Added=${newItems.length}, Total=${products.value.length}, hasNext=${hasNext.value}`)
            return newItems
        } catch (err) {
            error.value = err
            console.error("[usePagination] loadMore error", err)
            throw err
        } finally {
            loading.value = false
            inFlight = false
        }
    }

    async function reset(params = {}) {
        console.info("🔄 [usePagination] reset called")
        try { currentAbort?.abort() } catch { }
        currentAbort = null
        products.value = []
        nextCursor.value = null
        hasNext.value = true
        error.value = null
        return fetchFirst(params)
    }

    async function forceReload(params = {}) {
        console.info("♻️ [usePagination] forceReload called")
        return reset(params)
    }

    if (options.autoFetch !== false) {
        fetchFirst().catch(e => { console.warn("[usePagination] autoFetch failed", e) })
    }

    return {
        products,
        nextCursor,
        hasNext,
        loading,
        error,
        count,
        fetchFirst,
        loadMore,
        reset,
        forceReload,
        _debug: () => ({ inFlight, aborted: currentAbort?.signal?.aborted ?? false }),
    }
}
