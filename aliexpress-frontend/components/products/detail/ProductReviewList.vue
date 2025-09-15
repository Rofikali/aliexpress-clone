<template>
  <div class="review-list">
    <h2>Customer Reviews</h2>

    <div v-if="loading">Loading reviews...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <ProductReviewItem
      v-for="review in reviews"
      :key="review.id"
      :review="review"
    />

    <button
      v-if="hasNext && !loading"
      @click="loadMore"
      class="load-more"
    >
      Load More
    </button>
  </div>
</template>

<script setup>
// import { useReviewPagination } from "~/composables/useReviewPagination"
// import ProductReviewItem from "./ProductReviewItem.vue"

const props = defineProps({
  productId: { type: String, required: true }
})

// const pagination = useReviewPagination(props.productId)

// const reviews = pagination.products
// const { loading, error, hasNext, loadMore } = pagination
</script>

<style scoped>
.error {
  color: red;
}
.load-more {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
}
</style>
