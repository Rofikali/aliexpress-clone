<template>
  <div class="checkout-page">
    <h1>Checkout</h1>

    <div v-if="loading">Loading checkout...</div>

    <div v-else-if="checkout" class="checkout-layout">
      <CheckoutAddress />
      <CheckoutPayment />
      <CheckoutSummary :checkout="checkout" />
      <CheckoutActions />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { useCheckout } from "~/composables/checkout/useCheckout"

import CheckoutAddress from "~/components/checkout/CheckoutAddress.vue"
import CheckoutPayment from "~/components/checkout/CheckoutPayment.vue"
import CheckoutSummary from "~/components/checkout/CheckoutSummary.vue"
import CheckoutActions from "~/components/checkout/CheckoutActions.vue"

const { checkout, loading, initCheckout } = useCheckout()

onMounted(initCheckout)
</script>



<!-- <CheckoutAddress>
  <AddressSelector />
</CheckoutAddress> -->
