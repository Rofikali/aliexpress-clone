<template>
  <div class="product-info">
    <h1>Title - {{ product?.title }}</h1>
    <p class="price">Price - ₹{{ product?.price }}</p>
    <p class="price">Descount Price - ₹{{ product?.discount_price }}</p>
    <p class="stock" :class="{ 'out-of-stock': !product?.in_stock }">
      {{ product?.in_stock ? "In Stock" : "Out of Stock" }}
    </p>
    <p class="description">Description - {{ product?.description }}</p>
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
