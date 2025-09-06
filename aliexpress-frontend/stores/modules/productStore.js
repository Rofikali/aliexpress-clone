// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { useApi } from "~/composables/core/useApi"

// export const useProductStore = defineStore("productStore", () => {
//     const products = ref([])
//     const loading = ref(false)
//     const error = ref(null)

//     // Pagination state
//     const cursor = ref("first")  // backend cursor key
//     const hasNext = ref(true)
//     const pageSize = 12  // default page size; adjust in backend if needed

//     /**
//      * Reset products (e.g., on filter/search change)
//      */
//     function resetProducts() {
//         products.value = []
//         cursor.value = "first"
//         hasNext.value = true
//         error.value = null
//     }

//     /**
//      * Fetch products from backend (supports cursor-based pagination)
//      */
//     async function fetchProducts({ cursorParam = cursor.value } = {}) {
//         loading.value = true
//         error.value = null

//         try {
//             const { data, status, error: fetchError } = await useApi(
//                 `/products/?cursor=${cursorParam}&page_size=${pageSize}`,
//                 { method: "GET" }
//             )

//             if (status !== 200 || fetchError) {
//                 throw fetchError || new Error("Failed to fetch products")
//             }

//             // Backend response: { data: { results: [...], next: cursor } }
//             const results = data?.data?.results || data?.data?.products || []
//             const nextCursor = data?.data?.next || null

//             // Prevent duplicates
//             const existingIds = new Set(products.value.map(p => p.id))
//             const newProducts = results.filter(p => !existingIds.has(p.id))

//             products.value.push(...newProducts)
//             cursor.value = nextCursor || null
//             hasNext.value = Boolean(nextCursor) && newProducts.length > 0

//             return { products: products.value, next: nextCursor }

//         } catch (err) {
//             console.error("[productStore] fetchProducts failed:", err)
//             error.value = err.message || "Unknown error"
//             throw err
//         } finally {
//             loading.value = false
//         }
//     }

//     /**
//      * Load next page (for infinite scroll)
//      */
//     async function loadMore() {
//         if (!hasNext.value || loading.value) return
//         await fetchProducts({ cursorParam: cursor.value })
//     }

//     /**
//      * Fetch single product by ID
//      */
//     async function fetchProductById(id) {
//         loading.value = true
//         error.value = null

//         try {
//             const { data, status, error: fetchError } = await useApi(`/products/${id}/`, { method: "GET" })

//             if (status !== 200 || fetchError) {
//                 throw fetchError || new Error("Failed to fetch product")
//             }

//             // Replace or add product in store
//             const index = products.value.findIndex(p => p.id === id)
//             if (index > -1) products.value[index] = data.data || data
//             else products.value.push(data.data || data)

//             return data.data || data

//         } catch (err) {
//             console.error("[productStore] fetchProductById failed:", err)
//             error.value = err.message || "Unknown error"
//             throw err
//         } finally {
//             loading.value = false
//         }
//     }

//     return {
//         // state
//         products,
//         loading,
//         error,
//         cursor,
//         hasNext,

//         // actions
//         resetProducts,
//         fetchProducts,
//         loadMore,
//         fetchProductById,
//     }
// })


// ~/stores/modules/productStore.js
import { defineStore } from "pinia"
import { useInfiniteScrollProducts } from "~/composables/products/useInfiniteScrollProducts"

export const useProductStore = defineStore("productStore", () => {
    // Infinite scroll composable handles cursor, loading, errors
    const {
        items: products,
        isLoading,
        error,
        hasNext,
        loadMore,
        sentinelRef,
        bindSentinel,
        unbindSentinel,
    } = useInfiniteScrollProducts({ pageSize: 12 }) // default pageSize configurable

    /**
     * Reset the store and reload first page
     */
    function reset() {
        products.value = []
        hasNext.value = true
        sentinelRef.value = null
        loadMore()
    }

    /**
     * Manual reload (useful for filters/search)
     */
    async function reload() {
        products.value = []
        hasNext.value = true
        await loadMore()
    }

    /**
     * Fetch single product by ID
     * Useful for product detail page
     */
    async function fetchProductById(id) {
        try {
            const { data, status } = await useApi(`/products/${id}/`, { method: "GET" })
            if (status !== 200 || !data) throw new Error(data?.message || "Failed to fetch product")
            return data
        } catch (err) {
            console.error("fetchProductById failed:", err)
            throw err
        }
    }

    return {
        // Data
        products,
        isLoading,
        error,
        hasNext,

        // Actions
        loadMore,
        reset,
        reload,
        fetchProductById,

        // Sentinel for infinite scroll binding
        sentinelRef,
        bindSentinel,
        unbindSentinel,
    }
})
