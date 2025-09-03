// ~/composables/pagination/createInfiniteScrollResource.js
import { ref } from "vue"
import { useInfiniteScroll } from "./useInfiniteScroll"

export function createInfiniteScrollResource(fetcher, opts = {}) {
    const items = ref([])
    const isLoading = ref(false)
    const error = ref(null)
    const hasNext = ref(true)

    async function loadMore() {
        if (isLoading.value || !hasNext.value) return
        try {
            isLoading.value = true
            const { results, next } = await fetcher(items.value.length, opts.pageSize ?? 12)

            items.value.push(...results)
            hasNext.value = !!next
        } catch (err) {
            error.value = err.message || "Failed to load"
        } finally {
            isLoading.value = false
        }
    }

    const { sentinelRef, bindSentinel, unbindSentinel } = useInfiniteScroll({
        loadMore,
        hasNext,
        isLoading,
        ...opts,
    })

    return {
        items,
        isLoading,
        error,
        hasNext,
        sentinelRef,
        bindSentinel,
        unbindSentinel,
        loadMore,
    }
}
