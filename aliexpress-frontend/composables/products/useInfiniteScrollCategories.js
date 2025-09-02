// ~/composables/pagination/useInfiniteScrollCategories.js
import { useCategoryStore } from "~/stores/modules/categoryStore"
import { useInfiniteScroll } from "./useInfiniteScroll"

export function useInfiniteScrollCategories(opts = {}) {
    const categoryStore = useCategoryStore()

    const { sentinelRef, bindSentinel } = useInfiniteScroll({
        loadMore: categoryStore.loadMore,
        hasNext: categoryStore.hasNext,
        isLoading: categoryStore.loading,
    })

    return {
        categories: categoryStore.categories,
        isLoading: categoryStore.loading,
        hasNext: categoryStore.hasNext,
        error: categoryStore.error,
        sentinelRef,
        bindSentinel,
    }
}
