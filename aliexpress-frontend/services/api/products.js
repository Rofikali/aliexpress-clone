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

// ~/services/api/product.js
import { handleError, normalizeResponse } from "~/composables/core/base"

const BASE = "/products/"

export async function getProducts(params = {}) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.get(BASE, { params })
        return normalizeResponse(res)
    } catch (e) {
        return handleError(e)
    }
}

export async function getProductById(id) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.get(`${BASE}${id}/`)
        return normalizeResponse(res)
    } catch (e) {
        return handleError(e)
    }
}

export async function searchProducts(query, params = {}) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.get(`${BASE}search/`, {
            params: { q: query, ...params },
        })
        return normalizeResponse(res)
    } catch (e) {
        return handleError(e)
    }
}

export async function createProduct(productData) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.post(BASE, productData)
        return normalizeResponse(res)
    } catch (e) {
        return handleError(e)
    }
}

export async function updateProduct(id, productData) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.put(`${BASE}${id}/`, productData)
        return normalizeResponse(res)
    } catch (e) {
        return handleError(e)
    }
}

export async function deleteProduct(id) {
    const { $api } = useNuxtApp()
    try {
        const res = await $api.delete(`${BASE}${id}/`)
        return normalizeResponse(res)
    } catch (e) {
        return handleError(e)
    }
}
