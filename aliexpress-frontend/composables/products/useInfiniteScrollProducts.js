// // ~/composables/pagination/useInfiniteScrollProducts.js
// import { useProductStore } from "~/stores/modules/productStore"
// import { useInfiniteScroll } from "../pagination/useInfiniteScroll"

// export function useInfiniteScrollProducts(opts = {}) {
//     const productStore = useProductStore()

//     const { sentinelRef, bindSentinel, unbindSentinel } = useInfiniteScroll({
//         loadMore: productStore.loadMore,
//         hasNext: productStore.hasNext,
//         isLoading: productStore.loading,
//         prefetch: opts.prefetch,
//         debug: opts.debug,
//     })

//     return {
//         products: productStore.products,
//         isLoading: productStore.loading,
//         hasNext: productStore.hasNext,
//         error: productStore.error,
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,
//     }
// }


// // ~/composables/products/useInfiniteScrollProducts.js
// import { useProductStore } from "~/stores/modules/productStore"
// import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

// export function useInfiniteScrollProducts(opts = {}) {
//     const productStore = useProductStore()

//     // Hook into generic infinite scroll composable
//     const { sentinelRef, bindSentinel, unbindSentinel } = useInfiniteScroll({
//         loadMore: productStore.loadMore,
//         hasNext: productStore.hasNext,
//         isLoading: productStore.loading,
//         prefetch: opts.prefetch,
//         debug: opts.debug,
//     })

//     return {
//         // Expose product store state
//         products: productStore.products,
//         isLoading: productStore.loading,
//         hasNext: productStore.hasNext,
//         error: productStore.error,

//         // Infinite scroll controls
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,

//         // Optional: expose reset/fetch manually
//         resetProducts: productStore.resetProducts,
//         fetchProducts: productStore.fetchProducts,
//     }
// }

// ~/composables/products/useInfiniteScrollProducts.js
import { createInfiniteScrollResource } from "~/composables/pagination/createInfiniteScrollResource"
import { useApi } from "~/composables/core/useApi"

/**
 * Infinite scroll composable for products
 * Fully cursor-based, compatible with your DRF backend
 */
export function useInfiniteScrollProducts(opts = {}) {
    let cursor = "first" // initial cursor

    async function fetchProducts(_, pageSize = 12) {
        const { data, status } = await useApi(`/products/?cursor=${cursor}&page_size=${pageSize}`, {
            method: "GET",
        })

        if (status !== 200 || !data) throw new Error(data?.message || "Failed to fetch products")

        cursor = data?.next_cursor || null

        return {
            results: data?.products || [],
            next: cursor,
        }
    }

    return createInfiniteScrollResource(fetchProducts, opts)
}
