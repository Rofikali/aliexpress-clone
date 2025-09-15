<template>
  <div class="related-products">
    <h2>Related Products</h2>
    <div class="related-list">
      <div v-for="p in related" :key="p.id" class="related-card">
        <NuxtLink :to="{ name: 'products-id', params: { id: p.id } }" class="block">
          <NuxtImg class="rounded-T" :src="p.image" alt="User Image" loading="lazy" />
          <p>{{ p.title }}</p>
          <p>₹{{ p.price }}</p>
          <p>₹{{ p.description.substring(0, 10) }}</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  related: { type: Array, default: () => [] }
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
