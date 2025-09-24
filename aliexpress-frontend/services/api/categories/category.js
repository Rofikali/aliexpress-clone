import { handleError, normalizeResponse } from "~/composables/core/base"

const BASE = "/category/"

// 🛠 Debug helpers
function logRequest(method, url, payload) {
    console.info(`[API REQUEST] ${method.toUpperCase()} ${url}`, payload || "")
}
function logSuccess(method, url, response) {
    console.info(`[API SUCCESS] ${method.toUpperCase()} ${url} →`, response?.data ?? response)
}
function logError(method, url, error) {
    console.error(`[API ERROR] ${method.toUpperCase()} ${url} →`, error)
}

// ===============================
// Category API Service
// ===============================
export async function getCategoryWithProducts(categoryId, params = {}) {
    const { $api } = useNuxtApp()
    const url = `${BASE}${categoryId}/`
    console.log('category url is ', url);
    try {
        logRequest("get", url, params)
        const res = await $api.get(url, { params })
        logSuccess("get", url, res)
        console.log('response data from category with product id ', normalizeResponse(res));
        return normalizeResponse(res)
    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}
