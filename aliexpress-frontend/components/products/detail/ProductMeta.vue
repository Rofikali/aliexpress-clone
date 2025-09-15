<template>
  <div class="product-meta">
    <p><strong>SKU:</strong> {{ product?.sku }}</p>
    <p><strong>Category:</strong> {{ product?.category?.name }}</p>
    <p><strong>Tags:</strong> {{ product?.tags?.join(", ") }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  product: { type: Object, default: null }
})
</script>
