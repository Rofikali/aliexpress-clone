<template>
  <div class="product-info">
    <h1>{{ product?.name }}</h1>
    <p class="price">₹{{ product?.price }}</p>
    <p class="stock" :class="{ 'out-of-stock': !product?.in_stock }">
      {{ product?.in_stock ? "In Stock" : "Out of Stock" }}
    </p>
    <p class="description">{{ product?.short_description }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  product: { type: Object, default: null }
})
</script>

<style scoped>
.price {
  font-size: 1.5rem;
  font-weight: bold;
}
.stock.out-of-stock {
  color: red;
}
</style>
