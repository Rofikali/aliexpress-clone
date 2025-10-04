<!-- <template>
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
</script> -->


<template>
  <div>
    <section class="relative bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-6 py-24 flex flex-col items-center text-center">
<!-- <h2>data id - {{  data.id }}</h2> -->
        <div v-if="data && data.length">
          <!-- <NuxtLink :to="{name: 'home-id', params: {id: data[0].id } }"> -->
          <img
            :src="data[0].image"
            :alt="data[0].alt_text || data[0].title"
            class="w-full h-full object-cover"
          />
            <h1 class="text-xl font-bold">{{ data[0].title }}</h1>
            <a v-if="data[0].link_url" :href="data[0].link_url" class="underline">
            </a>
          <!-- </NuxtLink> -->
        </div>

        <h1 class="text-4xl md:text-6xl font-bold mb-6">{{ data[0].title }}</h1>
        <p class="text-lg md:text-xl max-w-2xl mb-8">
          {{ data[0].alt_text }}
        </p>
        <button
            class="bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg shadow hover:bg-gray-100"
              >
              Shop Now
        </button>

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