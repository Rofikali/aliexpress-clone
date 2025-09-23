// import { defineStore } from "pinia"
// import {
//     getAttributes,
//     getAttributeById,
// } from "~/services/api/products/attribute"
// import { usePagination } from "~/composables/pagination/useBasePagination"

// export const useAttributeStore = defineStore("attributeStore", () => {
//     // ============ Pagination (list of attributes per variant) ============
//     const pagination = usePagination(getAttributes, { pageSize: 20, debug: true })

//     // ============ Single attribute ============
//     const selectedAttribute = ref(null)
//     const attributeLoading = ref(false)
//     const attributeError = ref(null)

//     async function fetchAttributes(productId, variantId) {
//         console.info(
//             "🚀 [attributeStore] fetchAttributes for variant:",
//             variantId
//         )
//         pagination.reset()
//         await pagination.fetchFirst({ product_pk: productId, variant_pk: variantId })
//     }

//     async function fetchAttributeById(productId, variantId, attributeId) {
//         console.info(
//             "🚀 [attributeStore] fetchAttributeById:",
//             attributeId
//         )
//         attributeLoading.value = true
//         attributeError.value = null
//         selectedAttribute.value = null

//         const response = await getAttributeById(productId, variantId, attributeId)
//         if (response.success) {
//             selectedAttribute.value = response.data
//             console.info("✅ [attributeStore] attribute loaded:", response.data)
//         } else {
//             attributeError.value = response
//             console.error("❌ [attributeStore] failed to load attribute:", response)
//         }

//         attributeLoading.value = false
//         return response
//     }

//     function setSelectedAttribute(attribute) {
//         selectedAttribute.value = attribute
//     }

//     return {
//         // List
//         attributes: pagination.items,
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
//         selectedAttribute,
//         attributeLoading,
//         attributeError,
//         fetchAttributes,
//         fetchAttributeById,
//         setSelectedAttribute,
//     }
// })


// // ~/stores/modules/product/attributeStore.js
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { getVariantAttributes, getVariantAttributeById } from "~/services/api/products/attribute"

// export const useAttributeStore = defineStore("attributeStore", () => {
//     const attributes = ref([])
//     const selectedAttribute = ref(null)
//     const attributeLoading = ref(false)
//     const attributeError = ref(null)

//     // ✅ Fetch all attributes for a variant
//     async function fetchAttributes(productId, variantId) {
//         if (!productId || !variantId) return
//         attributeLoading.value = true
//         attributeError.value = null
//         try {
//             const res = await getVariantAttributes(productId, variantId)
//             if (res.success) {
//                 attributes.value = res.data
//             } else {
//                 attributeError.value = res
//             }
//             return res
//         } catch (err) {
//             attributeError.value = err
//             return err
//         } finally {
//             attributeLoading.value = false
//         }
//     }

//     // ✅ Fetch a single attribute by ID
//     async function fetchAttributeById(productId, variantId, attributeId) {
//         if (!productId || !variantId || !attributeId) return
//         attributeLoading.value = true
//         attributeError.value = null
//         try {
//             const res = await getVariantAttributeById(productId, variantId, attributeId)
//             if (res.success) {
//                 selectedAttribute.value = res.data
//             } else {
//                 attributeError.value = res
//             }
//             return res
//         } catch (err) {
//             attributeError.value = err
//             return err
//         } finally {
//             attributeLoading.value = false
//         }
//     }

//     return {
//         attributes,
//         selectedAttribute,
//         attributeLoading,
//         attributeError,
//         fetchAttributes,
//         fetchAttributeById,
//     }
// })


// // ~/stores/modules/product/attributeStore.js
// import { defineStore } from "pinia"
// import { getAttributes, getAttributeById } from "~/services/api/products/attribute"

// export const useAttributeStore = defineStore("attributeStore", () => {
//     const attributes = ref([])             // lightweight list
//     const expandedAttributes = ref({})     // cache of full details { id: {...} }
//     const attrLoading = ref(false)
//     const attrError = ref(null)

//     // Fetch list of attributes for a variant
//     async function fetchAttributes(productId, variantId) {
//         if (!productId || !variantId) return
//         attrLoading.value = true
//         attrError.value = null

//         try {
//             const res = await getAttributes(productId, variantId)
//             if (res.success) {
//                 attributes.value = res.data
//             } else {
//                 attrError.value = res
//             }
//             return res
//         } catch (err) {
//             attrError.value = err
//             return err
//         } finally {
//             attrLoading.value = false
//         }
//     }

//     // Fetch single attribute detail (cached on expand)
//     async function fetchAttributeById(productId, variantId, attributeId) {
//         if (!productId || !variantId || !attributeId) return

//         if (expandedAttributes.value[attributeId]) {
//             return expandedAttributes.value[attributeId] // cached
//         }

//         attrLoading.value = true
//         attrError.value = null

//         try {
//             const res = await getAttributeById(productId, variantId, attributeId)
//             if (res.success) {
//                 expandedAttributes.value[attributeId] = res.data
//                 return res.data
//             } else {
//                 attrError.value = res
//             }
//             return res
//         } catch (err) {
//             attrError.value = err
//             return err
//         } finally {
//             attrLoading.value = false
//         }
//     }

//     return {
//         attributes,
//         expandedAttributes,
//         attrLoading,
//         attrError,
//         fetchAttributes,
//         fetchAttributeById,
//     }
// })

import { defineStore } from "pinia"
import { getAttributes, getAttributeById } from "~/services/api/products/attribute"

export const useAttributeStore = defineStore("attributeStore", () => {
    const attributes = ref([])
    const attributeLoading = ref(false)
    const attributeError = ref(null)

    const attributeDetail = ref(null)
    const detailLoading = ref(false)
    const detailError = ref(null)

    // Fetch all attributes for a variant
    async function fetchAttributes(productId, variantId) {
        if (!productId || !variantId) return
        attributeLoading.value = true
        attributeError.value = null
        try {
            const res = await getAttributes(productId, variantId)
            if (res.success) attributes.value = res.data
            else attributeError.value = res
            return res
        } catch (err) {
            attributeError.value = err
            return err
        } finally {
            attributeLoading.value = false
        }
    }

    // Fetch single attribute detail
    async function fetchAttributeById(productId, variantId, attrId) {
        if (!productId || !variantId || !attrId) return
        detailLoading.value = true
        detailError.value = null
        try {
            const res = await getAttributeById(productId, variantId, attrId)
            if (res.success) attributeDetail.value = res.data
            else detailError.value = res
            return res
        } catch (err) {
            detailError.value = err
            return err
        } finally {
            detailLoading.value = false
        }
    }

    return {
        // state
        attributes,
        attributeLoading,
        attributeError,
        attributeDetail,
        detailLoading,
        detailError,
        // actions
        fetchAttributes,
        fetchAttributeById,
    }
})
