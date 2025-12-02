
// // ~/services/api/products/attributes.js
// // Product Attributes API Service
// // -----------------------------
// // Handles endpoints:
// // GET /products/{product_pk}/variants/{variant_pk}/attributes/
// // GET /products/{product_pk}/variants/{variant_pk}/attributes/{id}/

// import { handleError, normalizeResponse } from "~/composables/core/base"

// const BASE = "/products/"

// function logRequest(method, url, payload) {
//     console.info(`[API REQUEST] ${method.toUpperCase()} ${url}`, payload || "")
// }

// function logSuccess(method, url, response) {
//     console.info(`[API SUCCESS] ${method.toUpperCase()} ${url} →`, response?.data ?? response)
// }

// function logError(method, url, error) {
//     console.error(`[API ERROR] ${method.toUpperCase()} ${url} →`, error)
// }

// // ✅ List all attributes for a variant
// export async function getAttributes(productId, variantId, params = {}) {
//     const { $api } = useNuxtApp()
//     const url = `${BASE}${productId}/variants/${variantId}/attributes/`
//     try {
//         logRequest("get", url, params)
//         const res = await $api.get(url, { params })
//         logSuccess("get", url, res)
//         return normalizeResponse(res)
//     } catch (e) {
//         logError("get", url, e)
//         return handleError(e)
//     }
// }

// // ✅ Retrieve single attribute by ID
// export async function getAttributeById(productId, variantId, attributeId) {
//     const { $api } = useNuxtApp()
//     const url = `${BASE}${productId}/variants/${variantId}/attributes/${attributeId}/`
//     try {
//         logRequest("get", url)
//         const res = await $api.get(url)
//         logSuccess("get", url, res)
//         return normalizeResponse(res)
//     } catch (e) {
//         logError("get", url, e)
//         return handleError(e)
//     }
// }



// // ~/services/api/product/attribute.js
// import { handleError, normalizeResponse } from "~/composables/core/base"

// const BASE = "/products"

// function logRequest(method, url, payload) {
//     console.info(`[API REQUEST] ${method.toUpperCase()} ${url}`, payload || "")
// }
// function logSuccess(method, url, response) {
//     console.info(`[API SUCCESS] ${method.toUpperCase()} ${url} →`, response?.data ?? response)
// }
// function logError(method, url, error) {
//     console.error(`[API ERROR] ${method.toUpperCase()} ${url} →`, error)
// }

// // ✅ Get all attributes for a variant
// export async function getVariantAttributes(productId, variantId, params = {}) {
//     if (!productId || !variantId) throw new Error("Product ID and Variant ID are required")
//     const { $api } = useNuxtApp()
//     const url = `${BASE}/${productId}/variants/${variantId}/attributes/`

//     try {
//         logRequest("get", url, params)
//         const res = await $api.get(url, { params })
//         logSuccess("get", url, res)
//         return normalizeResponse(res)
//     } catch (e) {
//         logError("get", url, e)
//         return handleError(e)
//     }
// }

// // ✅ Get a single attribute by ID
// export async function getVariantAttributeById(productId, variantId, attributeId) {
//     if (!productId || !variantId || !attributeId) {
//         throw new Error("Product, Variant, and Attribute ID are required")
//     }
//     const { $api } = useNuxtApp()
//     const url = `${BASE}/${productId}/variants/${variantId}/attributes/${attributeId}/`

//     try {
//         logRequest("get", url)
//         const res = await $api.get(url)
//         logSuccess("get", url, res)
//         return normalizeResponse(res)
//     } catch (e) {
//         logError("get", url, e)
//         return handleError(e)
//     }
// }

// ~/services/api/products/attribute.js
import { handleError, normalizeResponse } from "~/app/composables/core/base"

const BASE = "/products"

function logRequest(method, url) {
    console.info(`[API REQUEST] ${method.toUpperCase()} ${url}`)
}
function logError(method, url, error) {
    console.error(`[API ERROR] ${method.toUpperCase()} ${url}`, error)
}
function logSuccess(method, url, res) {
    console.info(`[API SUCCESS] ${method.toUpperCase()} ${url}`, res?.data)
}

// ✅ List attributes for a variant
export async function getAttributes(productId, variantId, params = {}) {
    const { $api } = useNuxtApp()
    const url = `${BASE}/${productId}/variants/${variantId}/attributes/`
    try {
        logRequest("get", url)
        const res = await $api.get(url, { params })
        logSuccess("get", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}

// ✅ Single attribute detail
export async function getAttributeById(productId, variantId, attributeId) {
    const { $api } = useNuxtApp()
    const url = `${BASE}/${productId}/variants/${variantId}/attributes/${attributeId}/`
    try {
        logRequest("get", url)
        const res = await $api.get(url)
        logSuccess("get", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}
