// ~/composables/search/useProductSearch.js
import { useBaseSearch } from '~/composables/search/useBaseSearch'

export function useProductSearch(opts = {}) {
    return useBaseSearch({
        endpoint: '/api/searchproducts/',
        itemsPath: 'products',
        pageSize: opts.pageSize ?? 10,
        debounceMs: opts.debounceMs ?? 300,
        autoFetch: opts.autoFetch ?? false,
        autoStartObserver: opts.autoStartObserver ?? true,
        dedupeKey: 'id',
        ...opts
    })
}
// *** Notes ***
// Above code working 100%
// ~/composables/search/useProductSearch.js
// import { ref, onMounted } from 'vue'
// import { useBaseSearch } from './useBaseSearch'
// import { LRUCache } from '~/utils/cache/lruCache'

// const cache = new LRUCache(100) // 100 queries max

// export function useProductSearch(options = {}) {
//     const base = useBaseSearch({
//         endpoint: '/api/searchproducts/',
//         ...options
//     })

//     // Wrap the search method to use LRU cache
//     const originalSearch = base.search
//     base.search = async (q = '') => {
//         const trimmed = String(q).trim()
//         if (!trimmed) return originalSearch(q)

//         const cached = cache.get(trimmed)
//         if (cached) {
//             // Return cached result immediately
//             base.items.value = cached
//             return cached
//         }

//         // Otherwise, do normal debounced search
//         await originalSearch(trimmed)

//         // Cache the result after successful search
//         cache.set(trimmed, [...base.items.value])
//     }

//     return base
// }
