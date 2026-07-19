import { useNuxtApp } from "#app"
import { createIdempotencyKey } from "~/shared/api/identifiers"
import { normalizeResponse, handleApiError } from "~/utils/api/base"

/**
 * Checkout response types
 * -----------------------
 * Adjust fields based on backend response
 */
export interface CheckoutOrder {
    id: string
    order_number: string
    total_amount: number
    currency: string
    status: string
    created_at: string
}

export interface CheckoutResponse {
    order: CheckoutOrder
    redirect_url?: string
}

const ENDPOINT = "/checkout/"

/**
 * Create checkout from current cart
 * ---------------------------------
 * - Requires non-empty cart
 * - Server validates cart & stock
 * - Returns created order
 * - Normalized response always
 */
export async function createCheckout(idempotencyKey = createIdempotencyKey()) {
    const { $api } = useNuxtApp()

    try {
        const res = await $api.post(ENDPOINT, undefined, {
            headers: { "Idempotency-Key": idempotencyKey },
        })

        return normalizeResponse<CheckoutResponse>(res)
    } catch (error) {
        return handleApiError(error)
    }
}
