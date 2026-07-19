/**
 * Base API response normalizer
 * ----------------------------
 * Ensures frontend always receives
 * a predictable response shape
 */

export interface NormalizedResponse<T> {
    success: boolean
    code: number | null
    message: string | null
    data: T | null
}

type ApiRecord = Record<string, unknown>

function isRecord(value: unknown): value is ApiRecord {
    return typeof value === "object" && value !== null
}

function responseMessage(payload: unknown, fallback: string): string {
    if (!isRecord(payload)) {
        return fallback
    }
    if (typeof payload.message === "string") {
        return payload.message
    }
    if (typeof payload.detail === "string") {
        return payload.detail
    }
    return fallback
}

export function normalizeResponse<T>(payload: unknown): NormalizedResponse<T> {
    const response = isRecord(payload) ? payload : {}
    return {
        success: Boolean(response.success),
        code: typeof response.code === "number" ? response.code : null,
        message: typeof response.message === "string" ? response.message : null,
        data: (response.data as T | null | undefined) ?? null
    }
}

export function handleApiError(error: unknown): NormalizedResponse<null> {
    const response = isRecord(error) && isRecord(error.response) ? error.response : null
    const status = response && typeof response.status === "number" ? response.status : 500
    const payload = response?.data
    const fallback = isRecord(error) && typeof error.message === "string"
        ? error.message
        : "Unable to complete the request"

    return {
        success: false,
        code: status,
        message: responseMessage(payload, fallback),
        data: null
    }
}
