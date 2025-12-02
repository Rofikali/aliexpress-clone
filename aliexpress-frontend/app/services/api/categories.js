import { useApi } from "~/app/composables/core/base"
import { normalizeResponse } from "~/services/helpers/response"

/**
 * Category API Service
 * --------------------
 * Endpoints for browsing and managing product categories.
 */

const BASE = "/categories/"

/** Fetch paginated categories */
export async function getCategories(params = {}) {
    return normalizeResponse(await useApi(BASE, { method: "GET", params }))
}

/** Get a single category by ID */
export async function getCategoryById(id) {
    return normalizeResponse(await useApi(`${BASE}${id}/`, { method: "GET" }))
}

/** Create a new category (Admin only) */
export async function createCategory(categoryData) {
    return normalizeResponse(
        await useApi(BASE, { method: "POST", body: categoryData })
    )
}

/** Update an existing category */
export async function updateCategory(id, categoryData) {
    return normalizeResponse(
        await useApi(`${BASE}${id}/`, { method: "PUT", body: categoryData })
    )
}

/** Delete a category */
export async function deleteCategory(id) {
    return normalizeResponse(await useApi(`${BASE}${id}/`, { method: "DELETE" }))
}
