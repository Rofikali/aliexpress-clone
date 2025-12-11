// import { defineStore } from "pinia"
// import { getVariants, getVariantById } from "~/services/api/products/variant"
// import { usePagination } from "~/composables/pagination/useBasePagination"

// export const useVariantStore = defineStore("variantStore", () => {
//     // ============ Pagination (list of variants per product) ============
//     const pagination = usePagination(getVariants, { pageSize: 12, debug: true })

//     // ============ Single variant ============
//     const selectedVariant = ref(null)
//     const variantLoading = ref(false)
//     const variantError = ref(null)

//     async function fetchVariants(productId) {
//         console.info("🚀 [variantStore] fetchVariants:", productId)
//         pagination.reset()
//         await pagination.fetchFirst({ product_pk: productId })
//     }

//     async function fetchVariantById(productId, variantId) {
//         console.info("🚀 [variantStore] fetchVariantById:", variantId)
//         variantLoading.value = true
//         variantError.value = null
//         selectedVariant.value = null

//         const response = await getVariantById(productId, variantId)
//         if (response.success) {
//             selectedVariant.value = response.data
//             console.info("✅ [variantStore] variant loaded:", response.data)
//         } else {
//             variantError.value = response
//             console.error("❌ [variantStore] failed to load variant:", response)
//         }

//         variantLoading.value = false
//         return response
//     }

//     function setSelectedVariant(variant) {
//         selectedVariant.value = variant
//     }

//     return {
//         // List
//         variants: pagination.items,
//         loading: pagination.loading,
//         error: pagination.error,
//         nextCursor: pagination.nextCursor,
//         hasNext: pagination.hasNext,
//         count: pagination.count,
//         fetchFirst: pagination.fetchFirst,
//         loadMore: pagination.loadMore,
//         reset: pagination.reset,
//         forceReload: pagination.forceReload,

//         // Single
//         selectedVariant,
//         variantLoading,
//         variantError,
//         fetchVariants,
//         fetchVariantById,
//         setSelectedVariant,
//     }
// })



// // ~/stores/modules/variantStore.js
// import { defineStore } from "pinia"
// import { getVariants, getVariantById } from "~/services/api/products/variant"
// import { usePagination } from '~/composables/pagination/useBasePagination'

// export const useVariantStore = defineStore("variantStore", () => {
//     // ============ Pagination (list of variants for a product) ============
//     const pagination = usePagination(getVariants, { pageSize: 10, debug: true })

//     // ============ Single variant ============
//     const variant = ref(null)
//     const variantLoading = ref(false)
//     const variantError = ref(null)

//     async function fetchVariantById(productId, variantId) {
//         variantLoading.value = true
//         variantError.value = null
//         variant.value = null

//         const res = await getVariantById(productId, variantId)
//         if (res.success) {
//             variant.value = res.data
//         } else {
//             variantError.value = res
//         }
//         variantLoading.value = false
//         return res
//     }

//     return {
//         // List
//         variants: pagination.items,
//         loading: pagination.loading,
//         error: pagination.error,
//         nextCursor: pagination.nextCursor,
//         hasNext: pagination.hasNext,
//         count: pagination.count,
//         fetchFirst: pagination.fetchFirst,
//         loadMore: pagination.loadMore,
//         reset: pagination.reset,
//         forceReload: pagination.forceReload,

//         // Single
//         variant,
//         variantLoading,
//         variantError,
//         fetchVariantById,
//     }
// })



// // ~/stores/modules/product/variantStore.js
// import { defineStore } from "pinia"
// import { getVariants } from "~/services/api/products/variant"
// import { usePagination } from "~/composables/pagination/useBasePagination"

// export const useVariantStore = defineStore("variantStore", () => {
//     const productId = ref(null)
//     // ============ Pagination (list of products) ============
//     const pagination = usePagination(getVariants, { pageSize: 12, debug: true })
//     // console.log('pagination in products store ', pagination);
//     // const pagination = usePagination(
//     //     (params) => getVariants(productId.value, params),
//     //     { pageSize: 12, debug: true }
//     // )
//     console.log('pagination in variantstore ', pagination);

//     // const variants = ref([])            // All variants of a product
//     // const selectedVariant = ref(null)   // Active variant
//     // const variantLoading = ref(false)
//     // const variantError = ref(null)

//     // // 🔹 Fetch all variants of a product
//     // async function fetchVariants(productId) {
//     //     if (!productId) return

//     //     variantLoading.value = true
//     //     variantError.value = null

//     //     try {
//     //         const res = await getVariants(productId)
//     //         if (res.success) {
//     //             variantLoading.value = res.data
//     //             selectedVariant.value = res.data[0] || null  // Select first by default
//     //         } else {
//     //             variantError.value = res
//     //         }
//     //         return res
//     //     } catch (err) {
//     //         variantError.value = err
//     //         return err
//     //     } finally {
//     //         variantLoading.value = false
//     //     }
//     // }

//     // // 🔹 Change selected variant manually
//     // function setSelectedVariant(variant) {
//     //     selectedVariant.value = variant
//     // }

//     return {

//         variants: pagination.items,
//         variantLoading: pagination.loading,
//         variantError: pagination.error,
//         // nextCursor: pagination.nextCursor,
//         // hasNext: pagination.hasNext,
//         fetchVariants: pagination.fetchFirst,
//         // loadMore: pagination.loadMore,
//         // reset: pagination.reset,
//         // forceReload: pagination.forceReload,

//         // list variants 

//         // single variant 
//         // variants,
//         // selectedVariant,
//         // variantLoading,
//         // variantError,
//         // fetchVariants,
//         // setSelectedVariant,
//     }
// })



// ~/stores/modules/product/variantStore.js
import { defineStore } from "pinia"
import { getVariants, getVariantById } from "~/services/api/products/variant"

export const useVariantStore = defineStore("variantStore", () => {
    // 🔹 State
    const variants = ref([])            // All variants of a product
    const selectedVariant = ref(null)   // Active variant
    const variantLoading = ref(false)
    const variantError = ref(null)

    // 🔹 Fetch all variants of a product
    async function fetchVariants(productId) {
        if (!productId) return

        variantLoading.value = true
        variantError.value = null

        try {
            const res = await getVariants(productId)
            console.log('does variants getched in variant Store ', res);
            if (res.success) {
                variants.value = res.data
                // auto-select first variant if available
                selectedVariant.value = res.data[0] || null
            } else {
                variantError.value = res
            }
            return res
        } catch (err) {
            variantError.value = err
            return err
        } finally {
            variantLoading.value = false
        }
    }

    // 🔹 Fetch a single variant by ID
    async function fetchVariantById(productId, variantId) {
        if (!productId || !variantId) return

        variantLoading.value = true
        variantError.value = null

        try {
            const res = await getVariantById(productId, variantId)
            console.log('does single variant getched in variant Store ', res);
            if (res.success) {
                selectedVariant.value = res.data
            } else {
                variantError.value = res
            }
            return res
        } catch (err) {
            variantError.value = err
            return err
        } finally {
            variantLoading.value = false
        }
    }

    // 🔹 Change selected variant manually
    function setSelectedVariant(variant) {
        selectedVariant.value = variant
    }

    return {
        // state
        variants,
        selectedVariant,
        variantLoading,
        variantError,
        // actions
        fetchVariants,
        fetchVariantById,
        setSelectedVariant,
    }
})
