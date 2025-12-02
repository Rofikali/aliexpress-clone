import { useApi } from "~/app/composables/core/base"
import { normalizeResponse } from "~/services/helpers/response"

/**
 * Comment API Service
 * -------------------
 * Endpoints for managing comments on products/posts.
 */

const BASE = "/comments/"

/** Fetch paginated comments */
export async function getComments(params = {}) {
    return normalizeResponse(await useApi(BASE, { method: "GET", params }))
}

/** Get a single comment by ID */
export async function getCommentById(id) {
    return normalizeResponse(await useApi(`${BASE}${id}/`, { method: "GET" }))
}

/** Create a new comment */
export async function createComment(commentData) {
    return normalizeResponse(
        await useApi(BASE, { method: "POST", body: commentData })
    )
}

/** Update an existing comment */
export async function updateComment(id, commentData) {
    return normalizeResponse(
        await useApi(`${BASE}${id}/`, { method: "PUT", body: commentData })
    )
}

/** Delete a comment */
export async function deleteComment(id) {
    return normalizeResponse(await useApi(`${BASE}${id}/`, { method: "DELETE" }))
}
