// ~/services/helpers/response.js
export function normalizeResponse({ data, error, status }) {
    if (error) {
        const message =
            error?.data?.detail ||
            error?.message ||
            "An unexpected error occurred"
        const code = error?.status || status || 500

        return {
            data: null,
            error: { message, code },
            status: code,
        }
    }

    return { data, error: null, status }
}
