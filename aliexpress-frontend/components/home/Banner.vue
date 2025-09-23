<template>
  <section>
    <h2>{{ data.title }}</h2>
    <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
      <div v-for="banner in data.banners" :key="banner.id" class="p-2 border">
        <img
          :src="banner.image"
          :alt="banner.alt_text || banner.title"
          class="w-full h-40 object-cover"
        />
        <p class="mt-1 text-sm">{{ banner.title }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>
