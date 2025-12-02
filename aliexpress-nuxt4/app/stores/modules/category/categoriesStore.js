// ~/stores/modules/categoryStore.js
import { defineStore } from "pinia"
import { getCategories } from "~/services/api/categories/category"
import { usePagination } from "~/composables/pagination/useBasePagination"

export const useCategoryStore = defineStore("categoryStore", () => {
    // ============ Pagination (list of products) ============
    const pagination = usePagination(getCategories, { pageSize: 12, debug: true })
    console.log('pagination in category store for all categories --------> ', pagination);

    return {
        // Listing categories
        categories: pagination.items,
        loading: pagination.loading,
        error: pagination.error,
        nextCursor: pagination.nextCursor,
        hasNext: pagination.hasNext,
        // count: pagination.count,
        fetchCategories: pagination.fetchFirst,
        loadMore: pagination.loadMore,
        reset: pagination.reset,
        forceReload: pagination.forceReload,
    }
})
