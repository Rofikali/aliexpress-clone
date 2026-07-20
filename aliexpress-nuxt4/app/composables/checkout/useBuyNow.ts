import { useCartStore } from "~/stores/modules/cart/cartStore"
import { useRouter } from "vue-router"

export function useBuyNow() {
    const cartStore = useCartStore()
    const router = useRouter()

    async function buyNow(variantId: string, quantity = 1) {
        if (!variantId) {
            throw new Error("Variant required")
        }

        // optional: clear cart
        // await cartStore.clearCart()

        await cartStore.addItem({
            product_variant_id: variantId,
            quantity
        })

        await router.push("/checkout")
    }

    return { buyNow }
}
