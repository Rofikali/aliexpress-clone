<!-- <template>
  <section>
    <h2>{{ data.title }}</h2>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="item in data.products" :key="item.id" class="p-2 border">
        <img :src="item.product.image" :alt="item.product.title" class="w-full h-40 object-cover"/>
        <h3>{{ item.product.title }}</h3>
        <p>\${{ item.product.price }}</p>
        <p>\${{ item.product.category.name }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script> -->


<template>
  <div>
<section class="bg-gray-100 py-16">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-2xl font-bold mb-8">Featured Products</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="item in data"
            :key="item.id"
            class="bg-white rounded-xl shadow p-4 hover:shadow-lg cursor-pointer flex flex-col"
          >
            <NuxtImg class="rounded-T" :src="item.image" alt="No Fount Image" loading="lazy" />
            <p class="text-blue-600 font-bold mt-2">title - {{ item.product }}</p>
            <p class="text-blue-600 font-bold mt-2">desc - {{ item.description.substring(0, 15) }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>

<style scoped>

</style>