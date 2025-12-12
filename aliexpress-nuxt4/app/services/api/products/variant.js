import { handleError, normalizeResponse } from "~/composables/core/base"

const BASE = "/products"

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

// ✅ Get all variants for a product
export async function getVariants(productId, params = {}) {
    if (!productId) throw new Error("Product ID is required for getVariants")
    const { $api } = useNuxtApp()
    // const url = BASE
    const url = `${BASE}/${productId}/variants/`
    console.log('getting url here ', url);
    try {
        logRequest("get", url, params)
        const res = await $api.get(url, { params })
        console.log('getting variants here ', url, res);
        logSuccess('get', url, res)
        return normalizeResponse(res)

    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}

// ✅ Get single variant by ID
export async function getVariantById(productId, variantId) {
    if (!productId || !variantId) throw new Error("Product ID and Variant ID are required")
    const { $api } = useNuxtApp()
    const url = `${BASE}/${productId}/variants/${variantId}/`
    try {
        logRequest("get", url)
        const res = await $api.get(url)
        logSuccess('get', url, res)
        return normalizeResponse(res)
    } catch (e) {
        logError("get", url, e)
        return handleError(e)
    }
}
