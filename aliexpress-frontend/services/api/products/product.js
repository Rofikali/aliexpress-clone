// // ~/services/api/products/product.js
//  * Product API Service
//  * -------------------
//  * A thin wrapper around backend product endpoints.
//  * 
//  * ✅ Provides consistent, documented methods per endpoint
//  * ✅ Normalizes responses via `normalizeResponse`
//  * ✅ Keeps business logic outside (only handles transport)
//  * 


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
