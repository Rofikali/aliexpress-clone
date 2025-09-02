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


import { useInfiniteScrollProducts } from "~/composables/pagination/useInfiniteScrollProducts"

export default {
    setup() {
        const {
            products,
            isLoading,
            hasNext,
            error,
            sentinelRef,
        } = useInfiniteScrollProducts()

        return {
            products,
            isLoading,
            hasNext,
            error,
            sentinelRef,
        }
    },
}
