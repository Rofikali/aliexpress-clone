<!-- <template>
  <section class="relative w-full h-96 overflow-hidden rounded-lg">
    <strong>Hero Section 2</strong>
    <h2>{{ data.title }}</h2>
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
console.log('what is inside data in herosectio dud ',props.data);

</script> -->



<template>
  <div>
    <section class="relative bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-6 py-24 flex flex-col items-center text-center">

        <img src="/google-logo.png" alt="" class="h-20 w-20 mb-4" />
        <img
        :src="data.banners[0].image"
        :alt="data.banners[0].alt_text || data.banners[0].title"
        class="h-20 w-20 mb-4" 
      />
        <div v-if="data.banners && data.banners.length">
          <img
            :src="data.banners[0].image"
            :alt="data.banners[0].alt_text || data.banners[0].title"
            class="w-full h-full object-cover"
          />
            <h1 class="text-xl font-bold">{{ data.banners[0].title }}</h1>
          <a v-if="data.banners[0].link_url" :href="data.banners[0].link_url" class="underline">
            Shop Now
          </a>
        </div>

        <h1 class="text-4xl md:text-6xl font-bold mb-6">Welcome to MyShop</h1>
        <p class="text-lg md:text-xl max-w-2xl mb-8">
          Discover amazing products, top categories, and exclusive deals all in one place.
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