

<template>
  <div class="product-actions">
    <button
      class="add-to-cart"
      :disabled="!selectedVariant || cartLoading"
      @click="handleAddToCart"
    >
      {{ cartLoading ? "Adding..." : "Add to Cart" }}
    </button>

    <button
      class="buy-now"
      :disabled="!selectedVariant || checkoutLoading"
      @click="handleBuyNow"
    >
      Buy Now
    </button>
  </div>
</template>

<script setup lang="ts">
import { useCart } from "~/composables/cart/useCart"
import { useCheckout } from "~/composables/checkout/useCheckout"

const props = defineProps<{
  selectedVariant: any | null
}>()

const { addToCart, loading: cartLoading } = useCart()
const { buyNow, loading: checkoutLoading } = useCheckout()

async function handleAddToCart() {
  if (!props.selectedVariant) return

  await addToCart({
    product_variant_id: props.selectedVariant.id,
    quantity: 1
  })
}

async function handleBuyNow() {
  if (!props.selectedVariant) return

  await addToCart({
    product_variant_id: props.selectedVariant.id,
    quantity: 1
  })
  await buyNow()
}
</script>

<style scoped>
.product-actions {
  display: flex;
  gap: 12px;
  margin-top: 1rem;
}

.add-to-cart {
  flex: 1;
  background: #dc2626;
  color: white;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
}

.buy-now {
  flex: 1;
  background: #111827;
  color: white;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

















































