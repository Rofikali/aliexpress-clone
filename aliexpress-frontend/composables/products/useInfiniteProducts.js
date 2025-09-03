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


// ~/composables/products/useInfiniteScrollProducts.js
import { useProductStore } from "~/stores/modules/productStore"
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

export function useInfiniteScrollProducts(opts = {}) {
    const productStore = useProductStore()

    // Hook into generic infinite scroll composable
    const { sentinelRef, bindSentinel, unbindSentinel } = useInfiniteScroll({
        loadMore: productStore.loadMore,
        hasNext: productStore.hasNext,
        isLoading: productStore.loading,
        prefetch: opts.prefetch,
        debug: opts.debug,
    })

    return {
        // Expose product store state
        products: productStore.products,
        isLoading: productStore.loading,
        hasNext: productStore.hasNext,
        error: productStore.error,

        // Infinite scroll controls
        sentinelRef,
        bindSentinel,
        unbindSentinel,

        // Optional: expose reset/fetch manually
        resetProducts: productStore.resetProducts,
        fetchProducts: productStore.fetchProducts,
    }
}
