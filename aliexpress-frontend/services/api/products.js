// // ~/services/api/product.js
// import { useApi } from "~/composables/core/useApi"
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
//     return normalizeResponse(await useApi(BASE, { method: "GET", params }))
// }

// /**
//  * Get a single product by ID
//  * 
//  * @param {string|number} id - product identifier
//  * @returns {Promise<{data: Object, error: Object|null, status: number}>}
//  */
// export async function getProductById(id) {
//     return normalizeResponse(await useApi(`${BASE}${id}/`, { method: "GET" }))
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
//         await useApi(`${BASE}search/`, {
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
//         await useApi(BASE, {
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
//         await useApi(`${BASE}${id}/`, {
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
//     return normalizeResponse(await useApi(`${BASE}${id}/`, { method: "DELETE" }))
// }


// ~/services/api/product.js
import { useApi } from "~/composables/core/useApi"

const BASE = "/products/"

/**
 * Product API Service
 * -------------------
 * Thin wrappers for backend product endpoints.
 *
 * ✅ Returns unified { status, success, code, message, request, meta, errors, data }
 * ✅ Keeps transport/normalization in useApi
 * ✅ Easy to extend with new endpoints
 */

/**
 * Fetch paginated products
 * 
 * @param {Object} params - query params (e.g., { cursor, page_size, category })
 * @returns {Promise<ApiResponse<Array>>}
 */
export function getProducts(params = {}) {
    return useApi(BASE, { method: "GET", params })
}

/**
 * Get a single product by ID
 * 
 * @param {string|number} id - product identifier
 * @returns {Promise<ApiResponse<Object>>}
 */
export function getProductById(id) {
    return useApi(`${BASE}${id}/`, { method: "GET" })
}

/**
 * Search products by keyword
 * 
 * @param {string} query - search keyword
 * @param {Object} params - filters (e.g., { sort, cursor })
 * @returns {Promise<ApiResponse<Array>>}
 */
export function searchProducts(query, params = {}) {
    return useApi(`${BASE}search/`, {
        method: "GET",
        params: { q: query, ...params },
    })
}

/**
 * Create a new product (Seller/Admin only)
 * 
 * @param {Object} productData - product payload
 * @returns {Promise<ApiResponse<Object>>}
 */
export function createProduct(productData) {
    return useApi(BASE, {
        method: "POST",
        body: productData,
    })
}

/**
 * Update an existing product
 * 
 * @param {string|number} id - product identifier
 * @param {Object} productData - product payload
 * @returns {Promise<ApiResponse<Object>>}
 */
export function updateProduct(id, productData) {
    return useApi(`${BASE}${id}/`, {
        method: "PUT",
        body: productData,
    })
}

/**
 * Delete a product
 * 
 * @param {string|number} id - product identifier
 * @returns {Promise<ApiResponse<null>>}
 */
export function deleteProduct(id) {
    return useApi(`${BASE}${id}/`, { method: "DELETE" })
}
