// // ~/stores/modules/categoryStore.js
// import { defineStore } from "pinia"
// import { getCategoryWithProducts } from "~/services/api/categories/category"
// // import { getCategories, getCategoryWithProducts } from "~/services/api/categories/category"
// // import { usePagination } from "~/composables/pagination/useBasePagination"

// export const useCategoryProductsStore = defineStore("categoryStore", () => {
//     // ============ Pagination (list of products) ============
//     // const pagination = usePagination(getCategories, { pageSize: 12, debug: true })
//     // console.log('pagination in category store for all categories --------> ', pagination);

//     // const category = ref(null)         // category info (id, name, description)
//     const products = ref([])           // product list
//     const nextCursor = ref(null)       // pagination cursor
//     const hasNext = ref(true)          // pagination flag
//     const loading = ref(false)
//     const error = ref(null)

//     async function fetchCategoryProducts(categoryId) {
//         loading.value = true
//         error.value = null
//         try {
//             const res = await getCategoryWithProducts(categoryId)
//             if (res.success) {
//                 products.value = res.data || []
//                 // category.value = res.data.category.name 
//                 nextCursor.value = res.meta?.next_cursor ?? null
//                 hasNext.value = res.meta?.has_next ?? false
//                 console.log("✅ First load:", products.value.length, "items")
//             } else {
//                 error.value = res
//             }
//             return res
//         } catch (e) {
//             error.value = e
//             return e
//         } finally {
//             loading.value = false
//         }
//     }

//     async function loadMore(categoryId) {
//         console.info("📥 [categoryStore] loadMore called", { categoryId, cursor: nextCursor.value })

//         if (!hasNext.value) {
//             console.warn("[categoryStore] No more items to load")
//             return
//         }
//         if (loading.value) {
//             console.warn("[categoryStore] Already loading, skipping loadMore")
//             return
//         }

//         loading.value = true
//         error.value = null

//         try {
//             const res = await getCategoryWithProducts(categoryId, { cursor: nextCursor.value })

//             if (res.success) {
//                 const newItems = Array.isArray(res.data)
//                     ? res.data
//                     : res.data ? [res.data] : []

//                 // ✅ Deduplicate like usePagination
//                 const map = new Map(products.value.map(p => [p.id, p]))
//                 for (const item of newItems) map.set(item.id, item)
//                 products.value = Array.from(map.values())

//                 nextCursor.value = res.meta?.next_cursor ?? null
//                 hasNext.value = res.meta?.has_next ?? false

//                 console.info(`✅ loadMore success. Added=${newItems.length}, Total=${products.value.length}, hasNext=${hasNext.value}`)
//             } else {
//                 error.value = res
//             }

//             return res
//         } catch (e) {
//             error.value = e
//             console.error("[categoryStore] loadMore error", e)
//             return e
//         } finally {
//             loading.value = false
//         }
//     }

//     return {
//         // // Listing categories
//         // categories: pagination.items,
//         // loading: pagination.loading,
//         // error: pagination.error,
//         // nextCursor: pagination.nextCursor,
//         // hasNext: pagination.hasNext,
//         // // count: pagination.count,
//         // fetchCategories: pagination.fetchFirst,
//         // loadMore: pagination.loadMore,
//         // reset: pagination.reset,
//         // forceReload: pagination.forceReload,

//         // single category related products,
//         products,
//         nextCursor,
//         hasNext,
//         loading,
//         error,
//         fetchCategoryProducts,
//         loadMore,
//     }
// })



// ~/stores/modules/useCategoryProductsStore.js
import { defineStore } from "pinia"
import { getCategoryWithProducts } from "~/services/api/categories/category"

export const useCategoryProductsStore = defineStore("categoryProducts", () => {
    const products = ref([])          // Products in the current category
    const nextCursor = ref(null)    // Cursor for pagination
    const hasNext = ref(true)
    const loading = ref(false)
    const error = ref(null)

    /**
     * Fetch first page of products for a given category
     */
    async function fetchProductsByCategory(categoryId) {
        loading.value = true
        error.value = null
        try {
            const res = await getCategoryWithProducts(categoryId)
            if (res.success) {
                products.value = res.data || []
                nextCursor.value = res.meta?.next_cursor ?? null
                hasNext.value = res.meta?.has_next ?? false
                console.log(`✅ [CategoryProducts] Initial load: ${products.value.length} items`)
            } else {
                error.value = res
            }
            return res
        } catch (err) {
            console.error("[CategoryProducts] fetch error:", err)
            error.value = err
            return err
        } finally {
            loading.value = false
        }
    }

    /**
     * Load next page of products (pagination)
     */
    async function loadMore(categoryId) {
        console.info("📥 [CategoryProducts] loadMoreProducts()", { categoryId, cursor: nextCursorId.value })

        if (!hasNext.value || loading.value) {
            console.warn("[CategoryProducts] Skipping loadMore (no next or already loading)")
            return
        }

        loading.value = true
        error.value = null
        try {
            const res = await getCategoryWithProducts(categoryId, { cursor: nextCursorId.value })
            if (res.success) {
                const newItems = Array.isArray(res.data) ? res.data : res.data ? [res.data] : []
                const map = new Map(products.value.map(p => [p.id, p]))
                newItems.forEach(p => map.set(p.id, p))
                products.value = Array.from(map.values())

                nextCursorId.value = res.meta?.next_cursor ?? null
                hasNext.value = res.meta?.has_next ?? false

                console.info(`✅ [CategoryProducts] loadMore success: added ${newItems.length}, total ${products.value.length}, hasNext=${hasNext.value}`)
            } else {
                error.value = res
            }
            return res
        } catch (err) {
            console.error("[CategoryProducts] loadMore error:", err)
            error.value = err
            return err
        } finally {
            loading.value = false
        }
    }

    return {
        products,
        nextCursor,
        hasNext,
        loading,
        error,
        fetchProductsByCategory,
        loadMore,
    }
})
