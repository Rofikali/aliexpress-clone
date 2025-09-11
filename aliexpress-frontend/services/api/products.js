// // ~/services/api/product.js
// import { api } from "~/composables/core/api"
// import { normalizeResponse } from "~/services/helpers/response"

// /**
//  * Product API Service
//  * -------------------
//  * A thin wrapper around backend product endpoints.
//  * 
//  * ✅ Provides consistent, documented methods per endpoint
//  * ✅ Normalizes responses via `normalizeResponse`
//  * ✅ Keeps business logic outside (only handles transport)
//  * 
//  * NOTE: All methods return `{ data, error, status }`
//  *       so consumers can always destructure safely.
//  */

// const BASE = "/products/"

// /**
//  * Fetch paginated products
//  * 
//  * @param {Object} params - query params (e.g., { page, page_size, category })
//  * @returns {Promise<{data: Array, error: Object|null, status: number}>}
//  */
// export async function getProducts(params = {}) {
//     return normalizeResponse(await api(BASE, { method: "GET", params }))
// }

// /**
//  * Get a single product by ID
//  * 
//  * @param {string|number} id - product identifier
//  * @returns {Promise<{data: Object, error: Object|null, status: number}>}
//  */
// export async function getProductById(id) {
//     return normalizeResponse(await api(`${BASE}${id}/`, { method: "GET" }))
// }

// /**
//  * Search products by keyword
//  * 
//  * @param {string} query - search keyword
//  * @param {Object} params - additional filters (e.g., { page, sort })
//  * @returns {Promise<{data: Array, error: Object|null, status: number}>}
//  */
// export async function searchProducts(query, params = {}) {
//     return normalizeResponse(
//         await api(`${BASE}search/`, {
//             method: "GET",
//             params: { q: query, ...params },
//         })
//     )
// }

// /**
//  * Create a new product (Seller/Admin only)
//  * 
//  * @param {Object} productData - product payload
//  * @returns {Promise<{data: Object, error: Object|null, status: number}>}
//  */
// export async function createProduct(productData) {
//     return normalizeResponse(
//         await api(BASE, {
//             method: "POST",
//             body: productData,
//         })
//     )
// }

// /**
//  * Update an existing product
//  * 
//  * @param {string|number} id - product identifier
//  * @param {Object} productData - product payload
//  * @returns {Promise<{data: Object, error: Object|null, status: number}>}
//  */
// export async function updateProduct(id, productData) {
//     return normalizeResponse(
//         await api(`${BASE}${id}/`, {
//             method: "PUT",
//             body: productData,
//         })
//     )
// }

// /**
//  * Delete a product
//  * 
//  * @param {string|number} id - product identifier
//  * @returns {Promise<{data: null, error: Object|null, status: number}>}
//  */
// export async function deleteProduct(id) {
//     return normalizeResponse(await api(`${BASE}${id}/`, { method: "DELETE" }))
// }

// // ~/services/api/product.js
// import { handleError, normalizeResponse } from "~/composables/core/base"

// const BASE = "/products/"

// export async function getProducts(params = {}) {
//     const { $api } = useNuxtApp()
//     try {
//         const res = await $api.get(BASE, { params })
//         return normalizeResponse(res)
//     } catch (e) {
//         return handleError(e)
//     }
// }

// export async function getProductById(id) {
//     const { $api } = useNuxtApp()
//     try {
//         const res = await $api.get(`${BASE}${id}/`)
//         return normalizeResponse(res)
//     } catch (e) {
//         return handleError(e)
//     }
// }

// export async function searchProducts(query, params = {}) {
//     const { $api } = useNuxtApp()
//     try {
//         const res = await $api.get(`${BASE}search/`, {
//             params: { q: query, ...params },
//         })
//         return normalizeResponse(res)
//     } catch (e) {
//         return handleError(e)
//     }
// }

// export async function createProduct(productData) {
//     const { $api } = useNuxtApp()
//     try {
//         const res = await $api.post(BASE, productData)
//         return normalizeResponse(res)
//     } catch (e) {
//         return handleError(e)
//     }
// }

// export async function updateProduct(id, productData) {
//     const { $api } = useNuxtApp()
//     try {
//         const res = await $api.put(`${BASE}${id}/`, productData)
//         return normalizeResponse(res)
//     } catch (e) {
//         return handleError(e)
//     }
// }

// export async function deleteProduct(id) {
//     const { $api } = useNuxtApp()
//     try {
//         const res = await $api.delete(`${BASE}${id}/`)
//         return normalizeResponse(res)
//     } catch (e) {
//         return handleError(e)
//     }
// }

// ~/services/api/product.js
import { handleError, normalizeResponse } from "~/composables/core/base"

const BASE = "/products/"

// 🛠 Debug logger helper
function logRequest(method, url, payload) {
    console.info(`[API REQUEST] ${method.toUpperCase()} ${url}`, payload || "")
}

function logSuccess(method, url, response) {
    console.info(
        `[API SUCCESS] ${method.toUpperCase()} ${url} →`,
        response?.data ?? response
    )
}

function logError(method, url, error) {
    console.error(`[API ERROR] ${method.toUpperCase()} ${url} →`, error)
}

// ===============================
// Products API Service
// ===============================
export async function getProducts(params = {}) {
    const { $api } = useNuxtApp()
    const url = BASE
    try {
        logRequest("get", url, params)
        const res = await $api.get(url, { params })
        logSuccess("get", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}

export async function getProductById(id) {
    const { $api } = useNuxtApp()
    const url = `${BASE}${id}/`
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

export async function searchProducts(query, params = {}) {
    const { $api } = useNuxtApp()
    const url = `${BASE}search/`
    try {
        logRequest("get", url, { q: query, ...params })
        const res = await $api.get(url, { params: { q: query, ...params } })
        logSuccess("get", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}

export async function createProduct(productData) {
    const { $api } = useNuxtApp()
    const url = BASE
    try {
        logRequest("post", url, productData)
        const res = await $api.post(url, productData)
        logSuccess("post", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("post", url, e)
        return handleError(e)
    }
}

export async function updateProduct(id, productData) {
    const { $api } = useNuxtApp()
    const url = `${BASE}${id}/`
    try {
        logRequest("put", url, productData)
        const res = await $api.put(url, productData)
        logSuccess("put", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("put", url, e)
        return handleError(e)
    }
}

export async function deleteProduct(id) {
    const { $api } = useNuxtApp()
    const url = `${BASE}${id}/`
    try {
        logRequest("delete", url)
        const res = await $api.delete(url)
        logSuccess("delete", url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("delete", url, e)
        return handleError(e)
    }
}
