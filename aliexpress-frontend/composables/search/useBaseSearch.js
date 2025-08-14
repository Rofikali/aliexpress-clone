// ~/composables/search/useBaseSearch.js
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { usePagination } from '~/composables/pagination/usePagination'
import { useObserverCore } from '~/composables/observer/useObserverCore'
import { useDebouncedSearch } from '~/composables/debounce/useDebouncedSearch'
import { createLRUCache } from '~/utils/cache/lruCache'

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
        cacheSize = 50 // LRU cache max entries
    } = options

    if (!endpoint) throw new Error('useBaseSearch: endpoint is required')

    // Core reactive state
    const query = ref('')
    const target = ref(null)
    const cache = createLRUCache(cacheSize)

    // Pagination
    const pagination = usePagination(endpoint, {
        pageSize,
        itemsPath,
        autoFetch: false,
        dedupeKey,
        debug
    })

    // Observer for infinite scroll
    const observer = useObserverCore({ defaultThreshold: 0.1, debug })

    // Combined error state
    const debounceError = ref(null)
    const error = computed(() => pagination.error.value || debounceError.value)

    const items = pagination.products
    const loading = pagination.loading
    const hasNext = pagination.hasNext
    const count = pagination.count

    // Immediate search (resets pagination)
    async function performSearchImmediate(q = '') {
        query.value = q ?? ''
        const cacheKey = `${endpoint}::${query.value}`
        if (cache.has(cacheKey)) {
            const cached = cache.get(cacheKey)
            await pagination.reset({ ...cached.params })
            return cached.items
        }

        const results = await pagination.reset({ q: String(query.value).trim(), ...params })
        cache.set(cacheKey, { params: { q: String(query.value).trim(), ...params }, items: results })
        return results
    }

    // Debounced fetch function
    const fetchFnForDebounce = async (q) => {
        try {
            const res = await performSearchImmediate(q)
            return { data: res, error: null }
        } catch (err) {
            return { data: null, error: err }
        }
    }

    const { result: debouncedResult, isSearching: isDebouncing, error: dbError, trigger: triggerDebounce } =
        useDebouncedSearch(fetchFnForDebounce, debounceMs)

    watch(dbError, (v) => { debounceError.value = v })

    // Public search APIs
    async function searchImmediate(q = '') {
        debounceError.value = null
        try {
            await performSearchImmediate(q)
        } catch (err) {
            if (debug) console.error('[useBaseSearch] searchImmediate error', err)
            throw err
        }
    }

    function search(q = '') {
        if (!q) {
            query.value = ''
            triggerDebounce('')
            return
        }
        query.value = q
        triggerDebounce(q)
    }

    async function loadMore() {
        if (!hasNext.value || loading.value) return []
        try {
            const newItems = await pagination.loadMore({ q: String(query.value).trim(), ...params })
            return newItems
        } catch (err) {
            if (debug) console.error('[useBaseSearch] loadMore error', err)
            throw err
        }
    }

    // Observer
    async function _onIntersect(entry) {
        if (!entry.isIntersecting) return
        if (hasNext.value && !loading.value) await loadMore()
    }

    function startObserver() {
        if (!target.value) {
            if (debug) console.warn('[useBaseSearch] startObserver: target not bound yet')
        }
        observer.observe(target, _onIntersect, { once: false, threshold: 0.1 })
    }

    function stopObserver() {
        try { observer.unobserve(target) } catch { }
    }

    onMounted(() => {
        if (autoStartObserver && target.value) startObserver()
    })
    onBeforeUnmount(() => { observer.stop() })

    if (autoFetch) {
        if (query.value) triggerDebounce(query.value)
        else searchImmediate('')
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
            pagination: pagination._debug?.(),
            observer: observer._debug?.(),
            debouncedResult: debouncedResult?.value ?? null
        })
    }
}
