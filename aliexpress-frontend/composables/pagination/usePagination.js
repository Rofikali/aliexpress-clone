// // ~/composables/pagination/usePagination.js


import { ref, computed } from 'vue'
import axios from '~/plugins/axios'

// tiny helper for deep access: "a.b.c" -> data[a][b][c]
function getByPath(obj, path, fallback = undefined) {
    if (!obj || !path) return fallback
    const parts = Array.isArray(path) ? path : String(path).split('.')
    let cur = obj
    for (const p of parts) {
        if (cur && Object.prototype.hasOwnProperty.call(cur, p)) cur = cur[p]
        else return fallback
    }
    return cur
}

/**
 * Production-ready cursor pagination composable
 *
 * Options (new):
 *  - itemsPath: dot-path to array of items (default tries: results, data, products, items)
 *  - nextCursorPath: dot-path to next cursor (default: next_cursor)
 *  - hasNextPath: dot-path to boolean (optional; fallback derives from next_cursor)
 */
export function usePagination(url, options = {}) {
    const $axios = axios().provide.axios

    const products = ref([])
    const nextCursor = ref(null)
    const hasNext = ref(true)
    const loading = ref(false)
    const error = ref(null)

    const pageSize = options.pageSize || 10
    const dedupeKey = options.dedupeKey || 'id'
    // const dedupeKey = options.dedupeKey || 'id'
    const retries = (options.retries || 0)
    const retryBackoffMs = options.retryBackoffMs || 300
    const debug = !!options.debug

    // NEW: response shape preferences
    const itemsPath = options.itemsPath || ['results', 'data', 'products', 'items']
    const nextCursorPath = options.nextCursorPath || 'next_cursor'
    const hasNextPath = options.hasNextPath || null

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
            try { currentAbort.abort() } catch (e) { }
            currentAbort = null
        }
        currentAbort = new AbortController()
        const signal = currentAbort.signal

        try {
            const resp = await $axios.get(url, {
                params: { ...params, page_size: pageSize },
                signal
            })
            return resp.data
        } catch (err) {
            if (signal && signal.aborted) {
                if (debug) console.warn('pagination request aborted')
                throw err
            }
            if (attempt < retries) {
                const backoff = retryBackoffMs * Math.pow(2, attempt)
                if (debug) console.warn(`retry attempt ${attempt + 1} in ${backoff}ms`, err)
                await new Promise(r => setTimeout(r, backoff))
                return _request(params, attempt + 1)
            }
            throw err
        }
    }

    function _extractItems(data) {
        if (Array.isArray(itemsPath)) {
            for (const path of itemsPath) {
                const arr = getByPath(data, path)
                if (Array.isArray(arr)) return arr
            }
            return Array.isArray(data) ? data : []
        }
        const val = getByPath(data, itemsPath)
        return Array.isArray(val) ? val : (Array.isArray(data) ? data : [])
    }

    function _extractNextCursor(data) {
        return getByPath(data, nextCursorPath, null)
    }

    function _extractHasNext(data, newItems) {
        if (hasNextPath) {
            const v = getByPath(data, hasNextPath, null)
            if (typeof v === 'boolean') return v
        }
        const nc = _extractNextCursor(data)
        if (nc !== null && nc !== undefined) return true
        return Array.isArray(newItems) ? newItems.length > 0 : false
    }

    async function fetchFirst(params = {}) {
        loading.value = true
        error.value = null
        inFlight = true
        try {
            const data = await _request({ ...params })
            const items = _extractItems(data)
            products.value = Array.isArray(items) ? items : []
            nextCursor.value = _extractNextCursor(data)
            hasNext.value = _extractHasNext(data, items)
            return products.value
        } catch (err) {
            error.value = err
            if (debug) console.error('[usePagination] fetchFirst error', err)
            throw err
        } finally {
            loading.value = false
            inFlight = false
        }
    }

    async function loadMore(params = {}) {
        if (!hasNext.value || loading.value || inFlight) return
        loading.value = true
        error.value = null
        inFlight = true
        try {
            const requestParams = { ...params }
            if (nextCursor.value) requestParams.cursor = nextCursor.value
            const data = await _request(requestParams)
            const newItems = _extractItems(data)
            products.value = _dedupeAppend(products.value, Array.isArray(newItems) ? newItems : [])
            nextCursor.value = _extractNextCursor(data)
            hasNext.value = _extractHasNext(data, newItems)
            return newItems
        } catch (err) {
            error.value = err
            if (debug) console.error('[usePagination] loadMore error', err)
            throw err
        } finally {
            loading.value = false
            inFlight = false
        }
    }

    async function reset(params = {}) {
        try { currentAbort?.abort() } catch (e) { }
        products.value = []
        nextCursor.value = null
        hasNext.value = true
        error.value = null
        return fetchFirst(params)
    }

    async function forceReload(params = {}) {
        return reset(params)
    }

    if (options.autoFetch !== false) {
        fetchFirst().catch(e => { if (debug) console.warn('autofetch failed', e) })
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
        _debug: () => ({ inFlight, aborted: currentAbort?.signal?.aborted ?? false })
    }
}

// *** BLOW CODE WORKING 100% FINE 
// import { ref, computed } from 'vue'
// import axios from '~/plugins/axios' // matches your existing import pattern

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
//     // const $axios = axiosFactory().provide.instance
//     const $axios = axios().provide.axios

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
//             const resp = await $axios.get(url, {
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

