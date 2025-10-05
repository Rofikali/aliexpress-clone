// ~/services/api/homepage/homepage.js
import { handleError, normalizeResponse } from "~/composables/core/base"

const BASE = "/homepage/"

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
// HomePage API Service
// ===============================
export async function getHomepageData(params = {}) {
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

export async function getHomepageDataById(id) {
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