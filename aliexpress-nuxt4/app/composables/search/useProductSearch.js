// ~/composables/search/useProductSearch.js
import { useBaseSearch } from '~/composables/search/useBaseSearch'

export function useProductSearch(opts = {}) {
    return useBaseSearch({
        endpoint: '/api/v1/searchproducts/',
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