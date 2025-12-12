
// ~/services/api/products/attribute.js
import { handleError, normalizeResponse } from "~/composables/core/base"

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
