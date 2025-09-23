<template>
  <section>
    <h2>{{ data.title }}</h2>
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="item in data.products" :key="item.id" class="p-2 border">
        <img :src="item.product.image" :alt="item.product.title" class="w-full h-40 object-cover"/>
        <h3>{{ item.product.title }}</h3>
        <p>\${{ item.product.price }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>
