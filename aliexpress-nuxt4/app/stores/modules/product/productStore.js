// ~/stores/modules/productStore.js
import { defineStore } from "pinia"
import { ref } from "vue"      // <<-- ADDED
import { getProducts, getProductById } from "~/services/api/products/product"
import { usePagination } from "~/composables/pagination/useBasePagination"

export const useProductStore = defineStore("productStore", () => {
    // ============ Pagination (list of products) ============
    const pagination = usePagination(getProducts, { pageSize: 12, debug: true })
    console.log('pagination in products store ', pagination);

    // ============ Single product ============
    const product = ref(null)
    const productLoading = ref(false)
    const productError = ref(null)

    async function fetchProductById(id) {
        console.info("🚀 [productStore] fetchProductById:", id)
        productLoading.value = true
        productError.value = null
        product.value = null

        const response = await getProductById(id)

        if (response.success) {
            product.value = response.data
            console.info("✅ [productStore] product loaded:", response.data)
        } else {
            productError.value = response
            console.error("❌ [productStore] failed to load product:", response)
        }

        productLoading.value = false
        return response
    }

    return {
        // List
        products: pagination.items,
        loading: pagination.loading,
        error: pagination.error,
        nextCursor: pagination.nextCursor,
        hasNext: pagination.hasNext,
        count: pagination.count,
        fetchFirst: pagination.fetchFirst,
        loadMore: pagination.loadMore,
        reset: pagination.reset,
        forceReload: pagination.forceReload,

        // Single
        product,
        productLoading,
        productError,
        fetchProductById,
    }
})
