<template>
  <section class="relative w-full h-96 overflow-hidden rounded-lg">
    <div v-if="data.banners && data.banners.length">
      <img
        :src="data.banners[0].image"
        :alt="data.banners[0].alt_text || data.banners[0].title"
        class="w-full h-full object-cover"
      />
      <div class="absolute bottom-4 left-4 text-white bg-black bg-opacity-50 p-2 rounded">
        <h1 class="text-xl font-bold">{{ data.banners[0].title }}</h1>
        <a v-if="data.banners[0].link_url" :href="data.banners[0].link_url" class="underline">
          Shop Now
        </a>
      </div>
    </div>
    <div v-else>
      <p>No Hero Banner Found</p>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>
