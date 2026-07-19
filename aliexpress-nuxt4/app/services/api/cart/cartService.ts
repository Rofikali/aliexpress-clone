

import { useNuxtApp } from "#app"
import { normalizeResponse, handleApiError } from "~/utils/api/base"


const ENDPOINT = "/cart/"

export interface AddToCartPayload {
    product_variant_id: string
    quantity?: number
}

export async function fetchCart() {
    const { $api } = useNuxtApp()
    const url = ENDPOINT
    try {
        const res = await $api.get(url)
        return normalizeResponse(res)
    } catch (err) {
        return handleApiError(err)
    }
}

export async function addItemToCart(payload: AddToCartPayload) {
    const { $api } = useNuxtApp()
    const url = ENDPOINT + "add_item/"
    try {
        const res = await $api.post(url, payload)
        return normalizeResponse(res)
    } catch (err) {
        return handleApiError(err)
    }
}
