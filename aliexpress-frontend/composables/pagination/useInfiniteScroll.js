// // ~/composables/pagination/useInfiniteScroll.js
// import { ref, computed, watch, nextTick, onMounted, onBeforeUnmount } from 'vue'
// import { useObserverCore } from './useObserverCore'
// import { usePagination } from './usePagination'

// // /**
// //  * Production-ready infinite scroll using cursor pagination + observer core
// //  *
// //  * @param {String} url             API endpoint
// //  * @param {Object} opts            options passed to pagination and observer
// //  *
// //  * Options (examples):
// //  *  - pageSize, dedupeKey, retries, retryBackoffMs, autoFetch, debug
// //  *  - threshold, rootMargin, debounceMs, throttleMs, once, prefetch
// //  **/
// export function useInfiniteScroll(url, opts = {}) {
//     if (!url) throw new Error('useInfiniteScroll requires url')

// after viewport check this codebase 
import { ref, computed, nextTick, onMounted, onBeforeUnmount } from 'vue'
// import { useObserverCore } from './useObserverCore'
import { useObserverCore } from '../observer/useObserverCore'
import { usePagination } from './usePagination'
import { useFillViewport } from './useFillViewport' // ✅ new import

export function useInfiniteScroll(url, opts = {}) {
    if (!url) throw new Error('useInfiniteScroll requires url')

    const pagination = usePagination(url, opts)
    const {
        products, hasNext, loading, error, fetchFirst, loadMore, reset
    } = pagination

    const core = useObserverCore({ debug: !!opts.debug })
    const sentinelRef = ref(null)
    const isObserving = ref(false)
    const isLoading = loading

    let destroyed = false

    async function safeLoad(entry = null) {
        if (destroyed || loading.value) return false
        try {
            const res = await loadMore()
            if (!hasNext.value) core.unobserve(sentinelRef.value)
            return !!hasNext.value
        } catch (err) {
            if (opts.debug) console.error('[useInfiniteScroll] safeLoad error', err)
            throw err
        }
    }

    const onEntry = async (entry) => {
        if (entry?.isIntersecting && opts.prefetch !== false) {
            try { await safeLoad(entry) } catch { }
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
        nextTick(checkAndLoadUntilScrollable) // ✅ auto-fill for large screens
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

// *** ABOVE CODE WORKING 100 % FINE
// import { ref, nextTick, onMounted, onBeforeUnmount, watch, isRef } from 'vue'
// import { useObserverCore } from './useObserverCore'
// import { usePagination } from './usePagination'
// import { useFillViewport } from './useFillViewport'

// /**
//  * Production-ready infinite scroll using cursor pagination + observer core
//  *
//  * @param {String} url
//  * @param {Object} opts
//  *   - paramsRef?: Ref<Record<string, any>> | Record<string, any>  (search/filters)
//  *   - prefetch?: boolean (default true)
//  *   - maxFillLoops?: number
//  *   - ...plus any usePagination options
//  */
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

//     const paramsRef = isRef(opts.paramsRef) ? opts.paramsRef : ref(opts.paramsRef || {})

//     let destroyed = false

//     async function safeLoad(entry = null) {
//         if (destroyed || loading.value) return false
//         try {
//             const res = await loadMore(paramsRef.value || {})
//             if (!hasNext.value && sentinelRef.value) core.unobserve(sentinelRef.value)
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

//     // NEW: react to params changes (e.g., new search query)
//     async function resetWithParams(newParams = {}) {
//         // replace params and reset the pagination
//         paramsRef.value = { ...(newParams || {}) }
//         await reset(paramsRef.value)
//         await nextTick()
//         // optional: auto-fill viewport
//         if (opts.fillOnReset !== false) await checkAndLoadUntilScrollable()
//     }

//     // If paramsRef changes deeply, reset (opt-in: pass opts.watchParamsDeep = true)
//     if (opts.watchParamsDeep) {
//         watch(paramsRef, async () => {
//             await resetWithParams(paramsRef.value)
//         }, { deep: true })
//     }

//     onMounted(() => {
//         if (sentinelRef.value) core.observe(sentinelRef.value, onEntry)
//         nextTick(checkAndLoadUntilScrollable)
//     })

//     onBeforeUnmount(() => {
//         destroyed = true
//         unbindSentinel()
//         core.stop()
//     })

//     return {
//         // state
//         products,
//         hasNext,
//         isLoading,
//         error,

//         // observer
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,

//         // params
//         paramsRef,
//         resetWithParams,
//     }
// }
