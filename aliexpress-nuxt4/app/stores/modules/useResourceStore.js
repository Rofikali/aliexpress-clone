// ~/stores/modules/useResourceStore.js
import { defineStore } from "pinia"
import { usePagination } from "~/composables/pagination/useBasePagination"

/**
 * Factory function to create a store for any cursor-based resource.
 *
 * @param {string} storeId - unique Pinia store ID
 * @param {Function} fetchFn - async function(params) => ApiResponse
 * @param {Object} options - pagination options (pageSize, dedupeKey, etc.)
 */
export function createResourceStore(storeId, fetchFn, options = {}) {
    return defineStore(storeId, () => {
        const {
            products: items,
            nextCursor,
            hasNext,
            loading,
            error,
            count,
            fetchFirst,
            loadMore,
            reset,
            forceReload
        } = usePagination(fetchFn, options)

        // Optional aliasing for semantic clarity
        const data = items

        return {
            data,
            nextCursor,
            hasNext,
            loading,
            error,
            count,
            fetchFirst,
            loadMore,
            reset,
            forceReload
        }
    })
}




// ~/stores/modules/categoryStore.js
import { createResourceStore } from "./useResourceStore"
import { getCategories } from "~/services/api/categories"

export const useCategoryStore = createResourceStore("categoryStore", getCategories, {
    pageSize: 10,
    dedupeKey: "id",
    autoFetch: false
})


// ~/stores/modules/brandStore.js
import { createResourceStore } from "./useResourceStore"
import { getBrands } from "~/services/api/brands"

export const useBrandStore = createResourceStore("brandStore", getBrands, {
    pageSize: 10,
    dedupeKey: "id",
    autoFetch: false
})
