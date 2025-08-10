// ~/composables/pagination/usePagination.js
import { ref, computed } from 'vue'
import { useNuxtApp } from '#app'

/**
 * usePagination
 * @param {String} url - API endpoint (e.g. '/posts/')
 * @param {Object} options - { initialParams: {}, pageSize: 15, autoFetch: true }
 */
export function usePagination(url, options = {}) {
    const nuxtApp = useNuxtApp()
    const $axios = nuxtApp.$axios

    const results = ref([])
    const nextCursor = ref(null)
    const loading = ref(false)
    const error = ref(null)
    const hasNext = ref(true)

    const initialParams = options.initialParams || {}
    const pageSize = options.pageSize || 15

    // computed meta (optional)
    const count = computed(() => results.value.length)

    async function reset(params = {}) {
        results.value = []
        nextCursor.value = null
        hasNext.value = true
        error.value = null
        await fetchFirst({ ...initialParams, ...params })
    }

    async function fetchFirst(params = {}) {
        loading.value = true
        error.value = null
        try {
            const resp = await $axios.get(url, {
                params: { ...params, page_size: pageSize }
            })
            // expecting backend shape { results, next_cursor, has_next }
            results.value = resp.data.results || []
            nextCursor.value = resp.data.next_cursor || null
            hasNext.value = !!resp.data.has_next
        } catch (err) {
            error.value = err
            console.error('pagination fetchFirst error', err)
        } finally {
            loading.value = false
        }
    }

    async function loadMore() {
        if (!hasNext.value || loading.value) return
        loading.value = true
        error.value = null
        try {
            const params = { page_size: pageSize }
            if (nextCursor.value) params.cursor = nextCursor.value

            const resp = await $axios.get(url, { params })
            const newResults = resp.data.results || []
            // append (de-dup optional)
            results.value.push(...newResults)
            nextCursor.value = resp.data.next_cursor || null
            hasNext.value = !!resp.data.has_next
        } catch (err) {
            error.value = err
            console.error('pagination loadMore error', err)
        } finally {
            loading.value = false
        }
    }

    // optionally auto-fetch the first page
    if (options.autoFetch !== false) {
        // Note: do not block here (caller may call reset instead)
        fetchFirst()
    }

    return {
        results,
        nextCursor,
        loading,
        error,
        hasNext,
        count,
        fetchFirst,
        loadMore,
        reset
    }
}
