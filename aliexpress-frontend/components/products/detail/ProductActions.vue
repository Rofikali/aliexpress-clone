<template>
  <div class="product-actions">
    <button @click="$emit('add-to-cart', product)">🛒 Add to Cart</button>
    <button @click="$emit('wishlist', product)">❤️ Wishlist</button>
    <button @click="shareProduct">🔗 Share</button>
  </div>
</template>

<script setup>
const props = defineProps({
  product: { type: Object, default: null }
})

function shareProduct() {
  if (navigator.share) {
    navigator.share({
      title: props.product?.name,
      url: window.location.href
    })
  } else {
    alert("Share not supported on this browser")
  }
}
</script>

<style scoped>
.product-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
button {
  padding: 0.6rem 1.2rem;
  border: 1px solid #ddd;
  background: #f9f9f9;
  cursor: pointer;
}
</style>
