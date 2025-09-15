<template>
  <div class="review-item">
    <p class="author"><strong>{{ review.author }}</strong></p>
    <p class="rating">⭐ {{ review.rating }}/5</p>
    <p class="comment">{{ review.comment }}</p>
  </div>
</template>

<script setup>
const props = defineProps({
  review: { type: Object, required: true }
})
</script>

<style scoped>
.review-item {
  border-bottom: 1px solid #ddd;
  padding: 1rem 0;
}
.rating {
  color: #f39c12;
}
</style>
