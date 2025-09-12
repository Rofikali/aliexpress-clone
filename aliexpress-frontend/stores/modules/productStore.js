// // // ~/stores/modules/productStore.js

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


// ~/stores/modules/productStore.js
import { defineStore } from "pinia"
import { usePagination } from "~/composables/pagination/useBasePagination"

export const useProductStore = defineStore("productStore", () => {
    console.info("🛒 [ProductStore] Initializing...")

    const {
        products,
        nextCursor,
        hasNext,
        loading,
        error,
        count,
        fetchFirst,
        loadMore,
        reset,
        forceReload,
    } = usePagination("/products", {
        pageSize: 12,
        dedupeKey: "id",
        retries: 1,
        retryBackoffMs: 500,
        debug: true,      // enable internal pagination logs
        autoFetch: false, // we control fetch manually
    })

    // Wrap actions with extra logging
    const fetchFirstWithLog = async (params = {}) => {
        console.info("🚀 [ProductStore] Fetching first products...", params)
        try {
            const res = await fetchFirst(params)
            console.info(`✅ [ProductStore] First fetch done. Count=${products.value.length}`)
            return res
        } catch (err) {
            console.error("❌ [ProductStore] fetchFirst failed:", err)
            throw err
        }
    }

    const loadMoreWithLog = async (params = {}) => {
        console.info("📥 [ProductStore] Loading more products...", params)
        try {
            const res = await loadMore(params)
            if (!res || res.length === 0) {
                console.warn("⚠️ [ProductStore] No more products returned from loadMore")
            } else {
                console.info(`✅ [ProductStore] Loaded ${res.length} more. Total=${products.value.length}`)
            }
            return res
        } catch (err) {
            console.error("❌ [ProductStore] loadMore failed:", err)
            throw err
        }
    }

    const resetWithLog = async (params = {}) => {
        console.info("🔄 [ProductStore] Resetting store and refetching...", params)
        return reset(params)
    }

    return {
        products,
        nextCursor,
        hasNext,
        loading,
        error,
        count,
        fetchFirst: fetchFirstWithLog,
        loadMore: loadMoreWithLog,
        reset: resetWithLog,
        forceReload,
    }
})





// // // ~/stores/modules/productStore.js
// // import { defineStore } from "pinia"
// // import { usePagination } from "~/composables/pagination/useBasePagination"

// // export const useProductStore = defineStore("productStore", () => {
// //     // ✅ Generic pagination composable for products
// //     const pagination = usePagination("/products/", {
// //         pageSize: 12,
// //         dedupeKey: "id",
// //         retries: 2,
// //         retryBackoffMs: 500,
// //         debug: true,
// //     })

// //     // 🔄 Reset with console log
// //     async function resetProducts(params = {}) {
// //         console.info("🔄 [ProductStore] Resetting products with params:", params)
// //         try {
// //             const res = await pagination.reset(params)
// //             console.info(`✅ [ProductStore] Reset complete. Loaded ${pagination.count.value} products.`)
// //             return res
// //         } catch (err) {
// //             console.error("❌ [ProductStore] Reset failed:", err)
// //             throw err
// //         }
// //     }

// //     // ⭐ Fetch first products
// //     async function fetchFirst(params = {}) {
// //         console.info("⭐ [ProductStore] Fetching featured products…", params)
// //         try {
// //             const res = await pagination.reset({ ...params, featured: true })
// //             console.info(`✅ [ProductStore] Fetched ${pagination.count.value} featured products.`)
// //             return res
// //         } catch (err) {
// //             console.error("❌ [ProductStore] Failed to fetch featured:", err)
// //             throw err
// //         }
// //     }

// //     // 🔍 Search products
// //     async function searchProducts(query, params = {}) {
// //         console.info(`🔍 [ProductStore] Searching products with query="${query}"`, params)
// //         try {
// //             const res = await pagination.reset({ ...params, q: query })
// //             console.info(`✅ [ProductStore] Search returned ${pagination.count.value} results.`)
// //             return res
// //         } catch (err) {
// //             console.error("❌ [ProductStore] Search failed:", err)
// //             throw err
// //         }
// //     }

// //     // 📦 Load next page (prefetch for UX)
// //     async function prefetchNext(params = {}) {
// //         if (pagination.hasNext.value && !pagination.loading.value) {
// //             console.info("📦 [ProductStore] Prefetching next page…")
// //             try {
// //                 const res = await pagination.loadMore(params)
// //                 console.info(`✅ [ProductStore] Prefetched ${res?.length || 0} products. Total: ${pagination.count.value}`)
// //                 return res
// //             } catch (err) {
// //                 console.warn("⚠️ [ProductStore] Prefetch failed:", err)
// //                 return []
// //             }
// //         } else {
// //             console.warn("⚠️ [ProductStore] Prefetch skipped: no next page or already loading.")
// //             return []
// //         }
// //     }

// //     return {
// //         // spread pagination state & methods directly
// //         ...pagination,

// //         // domain-specific actions with logs
// //         resetProducts,
// //         fetchFirst,
// //         searchProducts,
// //         prefetchNext,
// //     }
// // })

