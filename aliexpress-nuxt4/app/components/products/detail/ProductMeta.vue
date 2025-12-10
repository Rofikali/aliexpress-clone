
<template>
    <!-- EXTRA META INFO -->
    <div class="space-y-2 text-sm mt-4">
      <p><strong>SKU:</strong> {{ product?.sku }}</p>
      <p><strong>Category:</strong> {{ product?.category?.name }}</p>
      <p><strong>Tags:</strong> {{ product?.tags?.join(', ') }}</p>
      <p><strong>Brand:</strong> {{ product?.brand?.name }}</p>
    </div>
</template>

<script setup  lang="ts">
const props = defineProps({
  product: { type: Object, required: true }
})
</script>
