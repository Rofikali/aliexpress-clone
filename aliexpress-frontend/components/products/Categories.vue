<template>
  <div class="related-products">
    <div class="related-list">
      <div v-for="category in categories" :key="category.id" class="related-card">
        <!-- <NuxtLink :to="{ name: 'products-id', params: { id: p.id } }" class="block"> -->
          <NuxtImg class="rounded-T" :src="category.image" alt="User Image" loading="lazy" />
          <p>{{ category.title }}</p>
          <p>₹{{ category.price }}</p>
          <p>₹{{ category.description.substring(0, 10) }}</p>
        <!-- </NuxtLink> -->
      </div>
       <!-- categories - {{ categories }} -->
    </div>
  </div>
</template>

<script setup>

const props = defineProps({
  categories: {
    type: Array,
    required: false,
    default: () => []
  }
})


</script>

<style scoped>
.related-list {
  display: flex;
  gap: 1rem;
  overflow-x: auto;
}

.related-card {
  min-width: 150px;
  border: 1px solid #eee;
  padding: 1rem;
}
</style>
