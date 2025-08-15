// ~/composables/cache/useSearchCache.js
// import { LRUCache } from './LRUCache'
import { LRUCache } from '~/utils/cache/lruCache'

export function useSearchCache({ size = 50, ttlMs = 5 * 60 * 1000, persistKey = 'search_cache' } = {}) {
    const cache = new LRUCache(size, ttlMs, persistKey)

    function buildKey(endpoint, params, query) {
        return `${endpoint}::${JSON.stringify(params)}::${query}`
    }

    return { cache, buildKey }
}
