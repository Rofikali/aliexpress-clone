<!-- <template>
  <div class="related-products">
    Categories Listing here
    <div class="related-list">
      <div v-for="category in categories" :key="category.id" class="related-card">
        <NuxtLink :to="{ name: 'products-id', params: { id: category.id } }" class="block">
          <NuxtImg class="rounded-T" :src="category.image" alt="User Image" loading="lazy" />
          <p>{{ category.title }}</p>
          <p>₹{{ category.price }}</p>
          <p>₹{{ category.description.substring(0, 15) }}</p>
        </NuxtLink>
      </div>

    </div>
  </div>
</template> -->


<template>
  <div id="CategoryPage" class="mt-4 max-w-[1200px] mx-auto px-2">
   categories
   <div v-for="item in categories" :key="item.id">
    <h1>name - {{ item.name }}</h1>
    <h1>slug - {{ item.slug }}</h1>
    <h2>desc - {{ item.description }}</h2>
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
.loading,
.end {
  text-align: center;
  padding: 1rem;
  font-weight: bold;
}
</style>
