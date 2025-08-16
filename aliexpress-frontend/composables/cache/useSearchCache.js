// ~/composables/cache/useSearchCache.js
// import { LRUCache } from './LRUCache'
// import { LRUCache } from '~/utils/cache/lruCache'
// import { LRUCache } from "./lruCache"

// export function useSearchCache({ size = 50, ttlMs = 5 * 60 * 1000, persistKey = 'search_cache' } = {}) {
//     const cache = new LRUCache(size, ttlMs, persistKey)

//     function buildKey(endpoint, params, query) {
//         return `${endpoint}::${JSON.stringify(params)}::${query}`
//     }

//     return { cache, buildKey }
// }  


// ~/composables/cache/useSearchCache.js
import { LRUCache } from "./lruCache"

let _cache // singleton so only one cache instance exists

export function useSearchCache({ size = 50, ttlMs = 5 * 60 * 1000, persistKey = "search_cache" } = {}) {
    if (!_cache) {
        _cache = new LRUCache(size, ttlMs, persistKey)
    }

    function buildKey(endpoint, params, query) {
        return `${endpoint}::${JSON.stringify(params)}::${query}`
    }

    // Wrap LRUCache methods so Nuxt doesn’t try to serialize the class
    return {
        cache: {
            get: (key) => _cache.get(key),
            set: (key, val) => _cache.set(key, val),
            has: (key) => _cache.has(key),
            delete: (key) => _cache.delete(key),
            clear: () => _cache.clear(),
            size: () => _cache.size()
        },
        buildKey
    }
}
