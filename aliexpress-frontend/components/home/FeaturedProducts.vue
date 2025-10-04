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
            <!-- <img
              :src="item.product.image || '/github-logo.png'"
              :alt="item.product.title"
              class="w-full h-40 object-cover rounded-lg mb-4"
            /> -->
            <!-- <h2>item - {{  item }}</h2> -->
            <h1>id - {{ item.sort_order  }}</h1>
            <h3>featured rant - {{  item.featured_rank }}</h3>
            <!-- <h3 class="font-medium text-gray-800 flex-1">{{ item.title }}</h3>
            <p class="text-blue-600 font-bold mt-2">${{ item.product.default_price }}</p>
            <p class="text-blue-600 font-bold mt-2">${{ item.product.description.substring(0, 50) }}</p> -->
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