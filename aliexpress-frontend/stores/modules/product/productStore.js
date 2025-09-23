// ~/stores/modules/productStore.js

// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { getProducts } from "~/services/api/products"

// export const useProductStore = defineStore("productStore", () => {
//     const products = ref([])
//     const loading = ref(false)
//     const error = ref(null)
//     const nextCursor = ref(null)
//     const hasNext = ref(true)

//     // 🔄 Reset state
//     const reset = () => {
//         products.value = []
//         nextCursor.value = null
//         hasNext.value = true
//         error.value = null
//         console.log("🔄 Product store reset")
//     }

//     // 📥 First fetch
//     const fetchFirst = async (params = {}) => {
//         reset()
//         loading.value = true

//         const response = await getProducts(params)

//         if (!response.success) {
//             error.value = response.errors || [{ message: response.message }]
//             loading.value = false
//             return response
//         }

//         products.value = response.data || []
//         loading.value = false
//         nextCursor.value = response.meta?.next_cursor ?? null
//         hasNext.value = response.meta?.has_next ?? false

//         console.log(`✅ Initial load: ${products.value.length} products`)
//         return response
//     }

//     // ➕ Load more (cursor-based pagination)
//     const loadMore = async (params = {}) => {
//         if (!hasNext.value) {
//             console.log("⚠️ No more products to load")
//             return
//         }
//         if (loading.value) {
//             console.log("⏳ Already loading, skipping loadMore")
//             return
//         }

//         loading.value = true

//         const requestParams = { ...params }
//         if (nextCursor.value) requestParams.cursor = nextCursor.value

//         const response = await getProducts(requestParams)
//         console.log('load More calling her ', response);
//         if (!response.success) {
//             error.value = response.errors || [{ message: response.message }]
//             loading.value = false
//             return response
//         }

//         const newProducts = Array.isArray(response.data)
//             ? response.data
//             : response.data
//                 ? [response.data]
//                 : []

//         // ✅ Deduplicate by `id`
//         const map = new Map(products.value.map(p => [p.id, p]))
//         for (const item of newProducts) map.set(item.id, item)
//         products.value = Array.from(map.values())

//         nextCursor.value = response.meta?.next_cursor ?? null
//         hasNext.value = response.meta?.has_next ?? false

//         loading.value = false
//         console.log(`✅ Total products: ${products.value.length}`)

//         return response
//     }

//     return {
//         products,
//         loading,
//         error,
//         nextCursor,
//         hasNext,
//         fetchFirst,
//         loadMore,
//         reset,
//     }
// })


// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { usePagination } from "~/composables/pagination/useBasePagination"

// export const useProductStore = defineStore("productStore", () => {
//     console.info("🛒 [ProductStore] Initializing...")

//     const {
//         products,
//         nextCursor,
//         hasNext,
//         loading,
//         error,
//         fetchFirst,
//         loadMore,
//         reset,
//         forceReload,
//     } = usePagination("/products", {
//         pageSize: 12,
//         dedupeKey: "id",
//         retries: 1,
//         retryBackoffMs: 500,
//         debug: true,      // enable internal pagination logs
//         autoFetch: false, // we control fetch manually
//     })

//     // Wrap actions with extra logging
//     const fetchFirstWithLog = async (params = {}) => {
//         console.info("🚀 [ProductStore] Fetching first products...", params)
//         try {
//             const res = await fetchFirst(params)
//             console.info(`✅ [ProductStore] First fetch done. Count=${products.value.length}`)
//             return res
//         } catch (err) {
//             console.error("❌ [ProductStore] fetchFirst failed:", err)
//             // throw err
//             return err
//         }
//     }

//     const loadMoreWithLog = async (params = {}) => {
//         console.info("📥 [ProductStore] Loading more products...", params)
//         try {
//             const res = await loadMore(params)
//             if (!res || res.length === 0) {
//                 console.warn("⚠️ [ProductStore] No more products returned from loadMore")
//             } else {
//                 console.info(`✅ [ProductStore] Loaded ${res.length} more. Total=${products.value.length}`)
//             }
//             return res
//         } catch (err) {
//             console.error("❌ [ProductStore] loadMore failed:", err)
//             // throw err
//             return err
//         }
//     }

//     const resetWithLog = async (params = {}) => {
//         console.info("🔄 [ProductStore] Resetting store and refetching...", params)
//         return reset(params)
//     }

//     return {
//         products,
//         nextCursor,
//         hasNext,
//         loading,
//         error,
//         fetchFirst: fetchFirstWithLog,
//         loadMore: loadMoreWithLog,
//         reset: resetWithLog,
//         forceReload,
//     }
// })



// //  *** Never touch above code base 
// // Above both code working fine 
// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { usePagination } from "~/composables/pagination/useBasePagination"
// import { getProducts } from "~/services/api/products"

// export const useProductStore = defineStore("productStore", () => {
//     // Pass the transport function directly
//     const pagination = usePagination(getProducts, { pageSize: 12, debug: true })

//     return {
//         products: pagination.items,
//         loading: pagination.loading,
//         error: pagination.error,
//         nextCursor: pagination.nextCursor,
//         hasNext: pagination.hasNext,
//         count: pagination.count,
//         fetchFirst: pagination.fetchFirst,
//         loadMore: pagination.loadMore,
//         reset: pagination.reset,
//         forceReload: pagination.forceReload,
//     }
// })

// ~/stores/modules/productStore.js
import { defineStore } from "pinia"
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
