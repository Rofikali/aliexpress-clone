// // ~/composables/search/useProductSearch.js
// import { useBaseSearch } from '~/composables/search/useBaseSearch'

// export function useProductSearch(opts = {}) {
//     return useBaseSearch({
//         endpoint: '/api/searchproducts/',
//         itemsPath: 'products',
//         pageSize: opts.pageSize ?? 10,
//         debounceMs: opts.debounceMs ?? 300,
//         autoFetch: opts.autoFetch ?? false,
//         autoStartObserver: opts.autoStartObserver ?? true,
//         dedupeKey: 'id',
//         ...opts
//     })
// }
// *** Notes ***
// Above code working 100%

// ~/composables/search/useProductSearch.js
import { useBaseSearch } from './useBaseSearch'

/**
 * useProductSearch
 *
 * Specialized wrapper around useBaseSearch for products.
 * Sets endpoint, default pageSize, debounce, and cache.
 *
 * Options:
 *  - pageSize
 *  - debounceMs
 *  - autoFetch
 *  - autoStartObserver
 *  - debug
 */
export function useProductSearch(options = {}) {
    const {
        pageSize = 10,
        debounceMs = 350,
        autoFetch = false,
        autoStartObserver = true,
        debug = false
    } = options

    const base = useBaseSearch({
        endpoint: '/api/searchproducts/',
        pageSize,
        debounceMs,
        autoFetch,
        autoStartObserver,
        debug,
        cacheSize: 100, // LRU cache entries for product search
        itemsPath: ['data'], // adjust depending on your API shape
    })

    return {
        ...base
    }
}
