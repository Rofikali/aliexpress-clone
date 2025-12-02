
// // ~/composables/search/useBaseSearch.js
// import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
// import { usePagination } from '~/composables/pagination/usePagination'
// import { useObserverCore } from '~/composables/observer/useObserverCore'
// import { useDebouncedSearch } from '~/composables/debounce/useDebouncedSearch'

// /**
//  * useBaseSearch
//  *
//  * Universal search composable that composes:
//  *  - usePagination (cursor pagination, dedupe, aborts)
//  *  - useObserverCore (infinite scroll sentinel)
//  *  - useDebouncedSearch (debounced user input)
//  *
//  * Designed to be endpoint-agnostic and production-ready.
//  *
//  * Options:
//  *  - endpoint (required)
//  *  - params (static query params merged with search q)
//  *  - pageSize
//  *  - itemsPath (delegates to usePagination)
//  *  - debounceMs
//  *  - autoFetch (false by default)
//  *  - autoStartObserver (true by default)
//  */
// export function useBaseSearch(options = {}) {
//     const {
//         endpoint,
//         params = {},
//         pageSize = 10,
//         itemsPath = ['results', 'data', 'products', 'items'],
//         debounceMs = 300,
//         autoFetch = false,
//         autoStartObserver = true,
//         dedupeKey = 'id',
//         debug = false
//     } = options

//     if (!endpoint) throw new Error('useBaseSearch: endpoint is required')

//     // Core reactive state
//     const query = ref('')
//     const target = ref(null) // sentinel for infinite scroll

//     // Pagination composable (handles network requests, aborts, dedupe)
//     const pagination = usePagination(endpoint, {
//         pageSize,
//         itemsPath,
//         autoFetch: false,
//         dedupeKey,
//         debug
//     })

//     // Observer for infinite scroll
//     const observer = useObserverCore({ defaultThreshold: 0.1, debug })

//     // Combined error: prefer pagination error, then debounce error
//     const debounceError = ref(null)
//     const error = computed(() => pagination.error.value || debounceError.value)

//     // Expose items and loading directly
//     const items = pagination.products
//     const loading = pagination.loading
//     const hasNext = pagination.hasNext
//     const count = pagination.count

//     // Internal: perform immediate search (resets pagination & fetches first page)
//     async function performSearchImmediate(q = '') {
//         // update query state
//         query.value = q ?? ''

//         // call reset on pagination with merged params
//         return pagination.reset({ q: String(query.value).trim(), ...params })
//     }

//     // Debounced search wrapper using your improved useDebouncedSearch
//     const fetchFnForDebounce = async (q) => {
//         try {
//             const res = await performSearchImmediate(q)
//             // return in a shape compatible with useDebouncedSearch
//             return { data: res, error: null }
//         } catch (err) {
//             return { data: null, error: err }
//         }
//     }
//     const { result: debouncedResult, isSearching: isDebouncing, error: dbError, trigger: triggerDebounce } =
//         useDebouncedSearch(fetchFnForDebounce, debounceMs)

//     // Mirror debounce error for unified error computed above
//     watch(dbError, (v) => { debounceError.value = v })

//     // Manual search API (non-debounced)
//     async function searchImmediate(q = '') {
//         debounceError.value = null
//         try {
//             await performSearchImmediate(q)
//         } catch (err) {
//             // bubble error via pagination.error already set inside usePagination
//             if (debug) console.error('[useBaseSearch] searchImmediate error', err)
//             throw err
//         }
//     }

//     // Generic search method that uses debounce (what UI should call)
//     function search(q = '') {
//         // trigger immediate reset when query cleared to avoid stale UI
//         if (!q) {
//             // clear local state & reset pagination
//             query.value = ''
//             triggerDebounce('') // this will early-return in the debounced implementation and reset result
//             return
//         }
//         // set local query but rely on debounce for network call
//         query.value = q
//         triggerDebounce(q)
//     }

//     // loadMore wrapper for manual "Load more" button or prefetch
//     async function loadMore() {
//         if (!hasNext.value || loading.value) return []
//         try {
//             // pass current query and static params
//             const newItems = await pagination.loadMore({ q: String(query.value).trim(), ...params })
//             return newItems
//         } catch (err) {
//             if (debug) console.error('[useBaseSearch] loadMore error', err)
//             throw err
//         }
//     }

//     // Observer callback: loads more when sentinel intersects
//     async function _onIntersect(entry) {
//         if (!entry.isIntersecting) return
//         // only trigger real network call if not loading and more exists
//         if (hasNext.value && !loading.value) {
//             await loadMore()
//         }
//     }

//     function startObserver() {
//         if (!target.value) {
//             if (debug) console.warn('[useBaseSearch] startObserver called but target is not bound yet')
//         }
//         // observe the target ref; useObserverCore accepts ref or node
//         try {
//             observer.observe(target, _onIntersect, { once: false, threshold: 0.1 })
//         } catch (err) {
//             if (debug) console.warn('[useBaseSearch] observer.observe failed', err)
//         }
//     }

//     function stopObserver() {
//         try {
//             observer.unobserve(target)
//         } catch (e) { /* swallow */ }
//     }

//     // Auto-start observer on mount if requested
//     onMounted(() => {
//         if (autoStartObserver && target.value) startObserver()
//     })

//     // Clean up observer & any in-flight state
//     onBeforeUnmount(() => {
//         try {
//             observer.stop()
//         } catch (e) { /* noop */ }
//     })

//     // Auto-fetch initial results if requested
//     if (autoFetch) {
//         // if query present do debounced search, otherwise fetch first page with empty query
//         if (query.value) {
//             triggerDebounce(query.value)
//         } else {
//             // direct fetch (no debounce)
//             searchImmediate('')
//         }
//     }

//     return {
//         // state
//         query,
//         items,
//         loading,
//         error,
//         hasNext,
//         count,
//         target, // bind this ref to sentinel element in template

//         // methods
//         search,            // debounced search (UI should call)
//         searchImmediate,   // immediate search (use for programmatic resets or server-driven calls)
//         loadMore,          // load next page manually
//         startObserver,
//         stopObserver,
//         _debug: () => ({
//             pagination: pagination._debug?.(),
//             observer: observer._debug?.(),
//             debouncedResult: debouncedResult?.value ?? null
//         })
//     }
// }


// *** Notes ***
// // Above code working 100% fine 

// ~/composables/search/useBaseSearch.js

// ~/composables/search/useBaseSearch.js
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { usePagination } from '~/app/composables/pagination/useBasePagination'
import { useObserverCore } from '~/app/composables/observer/useObserverCore'
import { useDebouncedSearch } from '~/app/composables/debounce/useDebouncedSearch'
import { useSearchCache } from '~/app/composables/cache/useSearchCache'
import { fuzzySearch } from '~/utils/sesarch/fuzzySearch'

export function useBaseSearch(options = {}) {
    const {
        endpoint,
        params = {},
        pageSize = 10,
        itemsPath = ['results', 'data', 'products', 'items'],
        debounceMs = 300,
        autoFetch = false,
        autoStartObserver = true,
        dedupeKey = 'id',
        debug = false,
        cacheSize = 50,
        cacheTTL = 5 * 60 * 1000,
        persistKey = 'search_cache',
        fuzzyFields = [],
        enableFuzzy = false
    } = options

    if (!endpoint) throw new Error('useBaseSearch: endpoint is required')

    const query = ref('')
    const target = ref(null)
    const { cache, buildKey } = useSearchCache({ size: cacheSize, ttlMs: cacheTTL, persistKey })

    const pagination = usePagination(endpoint, {
        pageSize,
        itemsPath,
        autoFetch: false,
        dedupeKey,
        debug
    })

    const observer = useObserverCore({ defaultThreshold: 0.1, debug })

    const debounceError = ref(null)
    const error = computed(() => pagination.error.value || debounceError.value)

    const items = pagination.products
    const loading = pagination.loading
    const hasNext = pagination.hasNext
    const count = pagination.count

    const inFlight = new Set()

    async function performSearchImmediate(q = '') {
        query.value = q ?? ''
        const cacheKey = buildKey(endpoint, params, query.value)

        if (cache.has(cacheKey)) {
            const cached = cache.get(cacheKey)
            if (enableFuzzy && fuzzyFields.length) {
                return fuzzySearch(cached.items, query.value, fuzzyFields)
            }
            return [...cached.items]
        }

        if (inFlight.has(cacheKey)) {
            if (debug) console.warn('[useBaseSearch] duplicate request skipped', cacheKey)
            return []
        }
        inFlight.add(cacheKey)

        try {
            const results = await pagination.reset({ q: String(query.value).trim(), ...params })
            cache.set(cacheKey, { params: { q: String(query.value).trim(), ...params }, items: results })
            return results
        } catch (err) {
            console.error('[useBaseSearch] reset failed', err)
            throw err
        } finally {
            inFlight.delete(cacheKey)
        }
    }

    const fetchFnForDebounce = async (q) => {
        try {
            const res = await performSearchImmediate(q)
            return { data: res, error: null }
        } catch (err) {
            return { data: null, error: err }
        }
    }

    const { result: debouncedResult, error: dbError, trigger: triggerDebounce } =
        useDebouncedSearch(fetchFnForDebounce, debounceMs)

    watch(dbError, (v) => { debounceError.value = v })

    async function searchImmediate(q = '') {
        debounceError.value = null
        triggerDebounce.cancel?.()
        return performSearchImmediate(q)
    }

    function search(q = '') {
        query.value = q
        triggerDebounce(q)
    }

    async function loadMore() {
        if (!hasNext.value || loading.value) return []
        return pagination.loadMore({ q: String(query.value).trim(), ...params })
    }

    async function _onIntersect(entry) {
        if (entry.isIntersecting && hasNext.value && !loading.value) {
            await loadMore()
        }
    }

    function startObserver() {
        if (target.value) {
            observer.observe(target, _onIntersect, { once: false, threshold: 0.1 })
        }
    }

    function stopObserver() {
        observer.unobserve(target)
    }

    onMounted(() => {
        if (autoStartObserver && target.value) startObserver()
    })

    onBeforeUnmount(() => {
        stopObserver()
    })

    if (autoFetch && !query.value) {
        searchImmediate('')
    }

    return {
        query,
        items,
        loading,
        error,
        hasNext,
        count,
        target,
        search,
        searchImmediate,
        loadMore,
        startObserver,
        stopObserver,
        _debug: () => ({
            cacheSize: cache.size(),
            inFlight: Array.from(inFlight),
            pagination: pagination._debug?.(),
            observer: observer._debug?.()
        }),
        enableFuzzy, // ✅ expose this
        fuzzyFields     // ✅ expose fuzzyFields too
    }
} 