// // // ~/composables/pagination/useInfiniteScroll.js
// // import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
// // import { useObserverCore } from './useObserverCore'
// // import { usePagination } from './usePagination'

// // // /**
// // //  * Production-ready infinite scroll using cursor pagination + observer core
// // //  *
// // //  * @param {String} url             API endpoint
// // //  * @param {Object} opts            options passed to pagination and observer
// // //  *
// // //  * Options (examples):
// // //  *  - pageSize, dedupeKey, retries, retryBackoffMs, autoFetch, debug
// // //  *  - threshold, rootMargin, debounceMs, throttleMs, once, prefetch
// // //  **/
// // export function useInfiniteScroll(url, opts = {}) {
// //     if (!url) throw new Error('useInfiniteScroll requires url')

// // after viewport check this codebase 
// import { ref, computed, nextTick, onMounted, onBeforeUnmount } from 'vue'
// // import { useObserverCore } from './useObserverCore'
// import { useObserverCore } from '../observer/useObserverCore'
// import { usePagination } from './usePagination'
// import { useFillViewport } from './useFillViewport' // ✅ new import

// export function useInfiniteScroll(url, opts = {}) {
//     if (!url) throw new Error('useInfiniteScroll requires url')

//     const pagination = usePagination(url, opts)
//     const {
//         products, hasNext, loading, error, fetchFirst, loadMore, reset
//     } = pagination

//     const core = useObserverCore({ debug: !!opts.debug })
//     const sentinelRef = ref(null)
//     const isObserving = ref(false)
//     const isLoading = loading

//     let destroyed = false

//     async function safeLoad(entry = null) {
//         if (destroyed || loading.value) return false
//         try {
//             const res = await loadMore()
//             if (!hasNext.value) core.unobserve(sentinelRef.value)
//             return !!hasNext.value
//         } catch (err) {
//             if (opts.debug) console.error('[useInfiniteScroll] safeLoad error', err)
//             throw err
//         }
//     }

//     const onEntry = async (entry) => {
//         if (entry?.isIntersecting && opts.prefetch !== false) {
//             try { await safeLoad(entry) } catch { }
//         }
//     }

//     function bindSentinel(nodeOrRef) {
//         const node = nodeOrRef?.value || nodeOrRef
//         if (!node) return
//         if (sentinelRef.value && sentinelRef.value !== node) {
//             core.unobserve(sentinelRef.value)
//         }
//         sentinelRef.value = node
//         core.observe(node, onEntry, {
//             threshold: opts.threshold ?? 0.1,
//             root: opts.root ?? null,
//             rootMargin: opts.rootMargin ?? '0px'
//         })
//         isObserving.value = true
//     }

//     function unbindSentinel() {
//         if (sentinelRef.value) core.unobserve(sentinelRef.value)
//         sentinelRef.value = null
//         isObserving.value = false
//     }

//     const { checkAndLoadUntilScrollable } = useFillViewport(safeLoad, hasNext, {
//         maxLoops: opts.maxFillLoops ?? 20,
//         debug: !!opts.debug
//     })

//     onMounted(() => {
//         if (sentinelRef.value) core.observe(sentinelRef.value, onEntry)
//         nextTick(checkAndLoadUntilScrollable) // ✅ auto-fill for large screens
//     })

//     onBeforeUnmount(() => {
//         destroyed = true
//         unbindSentinel()
//         core.stop()
//     })

//     return {
//         products,
//         hasNext,
//         isLoading,
//         error,
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel
//     }
// }

// *** ABOVE CODE WORKING 100 % FINE
// ~/composables/pagination/useInfiniteScroll.js


import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { useObserverCore } from '../observer/useObserverCore'
import { usePagination } from './usePagination'
import { useFillViewport } from './useFillViewport'

/**
 * Production-ready infinite scroll using cursor pagination + observer core
 * with API shape bulletproofing
 */
export function useInfiniteScroll(url, opts = {}) {
    if (!url) throw new Error('useInfiniteScroll requires url')

    const pagination = usePagination(url, opts)
    const {
        products,
        hasNext,
        loading,
        error,
        fetchFirst,
        loadMore,
        reset
    } = pagination

    const core = useObserverCore({ debug: !!opts.debug })
    const sentinelRef = ref(null)
    const isObserving = ref(false)
    const isLoading = loading

    let destroyed = false

    // ✅ Extra layer: bulletproof item extraction if products is empty
    function extractItems(data) {
        // if (Array.isArray(data?.results)) return data.results
        if (Array.isArray(data?.products)) return data.products
        // if (Array.isArray(data?.items)) return data.items
        return []
    }

    async function safeLoad(entry = null) {
        if (destroyed || loading.value) return false
        try {
            const res = await loadMore()
            // If loadMore didn’t populate products but returned raw data, try extracting manually
            if (Array.isArray(res) && res.length && products.value.length === 0) {
                products.value = extractItems({ results: res })
            }
            if (!hasNext.value) core.unobserve(sentinelRef.value)
            return !!hasNext.value
        } catch (err) {
            if (opts.debug) console.error('[useInfiniteScroll] safeLoad error', err)
            throw err
        }
    }

    const onEntry = async (entry) => {
        if (entry?.isIntersecting && opts.prefetch !== false) {
            try { await safeLoad(entry) } catch { /* silent fail */ }
        }
    }

    function bindSentinel(nodeOrRef) {
        const node = nodeOrRef?.value || nodeOrRef
        if (!node) return
        if (sentinelRef.value && sentinelRef.value !== node) {
            core.unobserve(sentinelRef.value)
        }
        sentinelRef.value = node
        core.observe(node, onEntry, {
            threshold: opts.threshold ?? 0.1,
            root: opts.root ?? null,
            rootMargin: opts.rootMargin ?? '0px'
        })
        isObserving.value = true
    }

    function unbindSentinel() {
        if (sentinelRef.value) core.unobserve(sentinelRef.value)
        sentinelRef.value = null
        isObserving.value = false
    }

    const { checkAndLoadUntilScrollable } = useFillViewport(safeLoad, hasNext, {
        maxLoops: opts.maxFillLoops ?? 20,
        debug: !!opts.debug
    })

    onMounted(() => {
        if (sentinelRef.value) core.observe(sentinelRef.value, onEntry)
        nextTick(checkAndLoadUntilScrollable) // auto-fill for large screens
    })

    onBeforeUnmount(() => {
        destroyed = true
        unbindSentinel()
        core.stop()
    })

    return {
        products,
        hasNext,
        isLoading,
        error,
        sentinelRef,
        bindSentinel,
        unbindSentinel
    }
}
