
// // // ~/stores/modules/product/variantStore.js
// // import { defineStore } from "pinia"
// // import { ref } from "vue"      // <<-- ADDED
// // import { getVariants, getVariantById } from "~/services/api/products/variant"

// // export const useVariantStore = defineStore("variantStore", () => {
// //     // 🔹 State
// //     const variants = ref([])            // All variants of a product
// //     const selectedVariant = ref(null)   // Active variant
// //     const variantLoading = ref(false)
// //     const variantError = ref(null)

// //     // 🔹 Fetch all variants of a product
// //     async function fetchVariants(productId) {
// //         if (!productId) return

// //         variantLoading.value = true
// //         variantError.value = null

// //         try {
// //             const res = await getVariants(productId)
// //             console.log('does variants getched in variant Store ', res);
// //             if (res.success) {
// //                 variants.value = res.data
// //                 // auto-select first variant if available
// //                 selectedVariant.value = res.data[0] || null
// //             } else {
// //                 variantError.value = res
// //             }
// //             return res
// //         } catch (err) {
// //             variantError.value = err
// //             return err
// //         } finally {
// //             variantLoading.value = false
// //         }
// //     }

// //     // 🔹 Fetch a single variant by ID
// //     async function fetchVariantById(productId, variantId) {
// //         if (!productId || !variantId) return

// //         variantLoading.value = true
// //         variantError.value = null

// //         try {
// //             const res = await getVariantById(productId, variantId)
// //             console.log('does single variant getched in variant Store ', res);
// //             if (res.success) {
// //                 selectedVariant.value = res.data
// //             } else {
// //                 variantError.value = res
// //             }
// //             return res
// //         } catch (err) {
// //             variantError.value = err
// //             return err
// //         } finally {
// //             variantLoading.value = false
// //         }
// //     }

// //     // 🔹 Change selected variant manually
// //     function setSelectedVariant(variant) {
// //         selectedVariant.value = variant
// //     }

// //     return {
// //         // state
// //         variants,
// //         selectedVariant,
// //         variantLoading,
// //         variantError,
// //         // actions
// //         fetchVariants,
// //         fetchVariantById,
// //         setSelectedVariant,
// //     }
// // })

// // ********* Above Codebase is Older 100% Working ****************

// // ~/stores/modules/product/variantStore.js
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { getVariants, getVariantById } from "~/services/api/products/variant"

// export const useVariantStore = defineStore("variantStore", () => {

//     // 🔹 State (UNCHANGED)
//     const variants = ref([])                // list of variant objects
//     const available_attributes = ref({})    // all attribute groups
//     const combination_map = ref({})         // map: attributeCombo → variantId

//     const selectedVariant = ref(null)       // currently active variant
//     const variantLoading = ref(false)
//     const variantError = ref(null)

//     // ============================
//     // 🔹 Fetch ALL variants of a product
//     // ============================
//     async function fetchVariants(productId) {
//         if (!productId) return

//         variantLoading.value = true
//         variantError.value = null

//         try {
//             const res = await getVariants(productId)

//             if (res.success) {
//                 const data = res.data

//                 // API FORMAT YOU GAVE:
//                 // variants: [...]
//                 // available_attributes: {...}
//                 // combination_map: {...}

//                 variants.value = data.variants || []
//                 available_attributes.value = data.available_attributes || {}
//                 combination_map.value = data.combination_map || {}

//                 // Auto-select a variant:
//                 selectedVariant.value =
//                     variants.value.find(v => v.stock > 0) ||
//                     variants.value[0] ||
//                     null

//             } else {
//                 variantError.value = res
//             }

//             return res

//         } catch (err) {
//             variantError.value = err
//             return err
//         } finally {
//             variantLoading.value = false
//         }
//     }

//     // ============================
//     // 🔹 Fetch single variant by ID
//     // ============================
//     async function fetchVariantById(productId, variantId) {
//         if (!productId || !variantId) return

//         variantLoading.value = true
//         variantError.value = null

//         try {
//             const res = await getVariantById(productId, variantId)

//             if (res.success) {
//                 selectedVariant.value = res.data
//             } else {
//                 variantError.value = res
//             }

//             return res

//         } catch (err) {
//             variantError.value = err
//             return err
//         } finally {
//             variantLoading.value = false
//         }
//     }

//     // ============================
//     // 🔹 Manually change selected variant
//     // ============================
//     function setSelectedVariant(variant) {
//         selectedVariant.value = variant
//     }

//     return {
//         // state
//         variants,
//         available_attributes,
//         combination_map,

//         selectedVariant,
//         variantLoading,
//         variantError,

//         // actions
//         fetchVariants,
//         fetchVariantById,
//         setSelectedVariant,
//     }
// })

// // ********* Above Codebase is Older 100% Working TOO ****************


// ~/stores/modules/product/variantStore.js
import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { getVariants, getVariantById } from "~/services/api/products/variant"

export const useVariantStore = defineStore("variantStore", () => {
    // state (same names you already use)
    const variants = ref([])                // All variants for current product
    const available_attributes = ref({})    // attribute groups object from API
    const combination_map = ref({})         // map: comboKey -> variantId

    const selectedVariant = ref(null)       // currently selected variant (object)
    const variantLoading = ref(false)
    const variantError = ref(null)

    // caching last fetched product id (simple in-memory cache)
    const lastFetchedFor = ref(null)

    // computed lookup: key -> variant (O(1) variant resolution)
    const variantLookup = computed(() => {
        const map = {}
        for (const v of variants.value || []) {
            // create key from v.attributes array
            const keyParts = (v.attributes || [])
                .map(a => `${a.attribute_id}:${a.value_id}`)
                .sort()
            const key = keyParts.join("|")
            map[key] = v
        }
        return map
    })

    // Helper: extract API payload safely (your API returns res.data)
    function normalizeApiPayload(res) {
        // res is output of normalizeResponse(res) or $fetch result structure
        // Your API uses { success, data: { variants, available_attributes, combination_map } }
        const payload = (res && (res.data ?? res)) || {}
        const data = payload.data ?? payload // some helpers may return nested
        return data || {}
    }

    // Fetch all variants
    async function fetchVariants(productId, { force = false } = {}) {
        if (!productId) return { success: false, message: "productId required" }

        // caching: if we already fetched same product and not forcing, return current values
        if (!force && lastFetchedFor.value === productId && variants.value.length) {
            return {
                success: true,
                variants: variants.value,
                available_attributes: available_attributes.value,
                combination_map: combination_map.value,
                default_variant: selectedVariant.value,
            }
        }

        variantLoading.value = true
        variantError.value = null

        try {
            const res = await getVariants(productId)
            // If getVariants uses normalizeResponse, res.data contains the API payload
            const data = normalizeApiPayload(res)

            // Expecting data.variants, data.available_attributes, data.combination_map
            variants.value = data.variants || []
            available_attributes.value = data.available_attributes || {}
            combination_map.value = data.combination_map || {}

            // auto-select first available (stock > 0) or first
            selectedVariant.value =
                variants.value.find(v => v.stock > 0) || variants.value[0] || null

            lastFetchedFor.value = productId

            return {
                success: true,
                variants: variants.value,
                available_attributes: available_attributes.value,
                combination_map: combination_map.value,
                default_variant: selectedVariant.value,
            }
        } catch (err) {
            variantError.value = err
            return {
                success: false,
                variants: [],
                available_attributes: {},
                combination_map: {},
                default_variant: null,
            }
        } finally {
            variantLoading.value = false
        }
    }

    // Fetch single variant by id (from API)
    async function fetchVariantById(productId, variantId) {
        if (!productId || !variantId) return
        variantLoading.value = true
        variantError.value = null
        try {
            const res = await getVariantById(productId, variantId)
            const data = normalizeApiPayload(res) || res.data || res
            // If the API returns the variant object directly in data
            const variantObj = data || res.data || res
            selectedVariant.value = variantObj
            return res
        } catch (err) {
            variantError.value = err
            return err
        } finally {
            variantLoading.value = false
        }
    }

    function setSelectedVariant(variant) {
        selectedVariant.value = variant
    }

    return {
        // state
        variants,
        available_attributes,
        combination_map,
        selectedVariant,
        variantLoading,
        variantError,
        // computed
        variantLookup,
        // actions
        fetchVariants,
        fetchVariantById,
        setSelectedVariant,
    }
})
