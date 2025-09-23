<!-- <template>
  <div>
    <h1>Page home</h1>

    <lazy-home-hero :data="hero"/>

    <lazy-home-featured-products :featuredProducts="data"
      :loading="loading"
      :error="error"
    />

    <lazy-home-categories :categories="categories"/>
    <lazy-home-banner :banners="banners" />
    <lazy-home-testimonials  :testimonials="testimonials" />

  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from "pinia"
const data = ref(null);

import { useHomepageStore } from '~/stores/modules/homepage/homepageStore'
const homeStore = useHomepageStore()



const {  hero, banners, categories, testimonials, loading, error  } = storeToRefs(homeStore)
const { fetchHomepageData } = homeStore


onMounted( async() => {
  data.value = await fetchHomepageData()
  console.log('does homepage fetching data or not ---- . ', data);
})
</script> -->






<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Homepage</h1>

    <!-- loading / error states -->
    <div v-if="loading" class="text-center py-10">Loading homepage...</div>
    <div v-else-if="error" class="text-center text-red-500 py-10">
      {{ error.message || "Something went wrong" }}
    </div>

    <!-- homepage sections -->
    <div v-else>
      <!-- Hero Section -->
      <LazyHomeHero v-if="heroSection" :data="heroSection" />

      <!-- Banners -->
      <LazyHomeBanner v-if="bannerSection" :data="bannerSection" />

      <!-- Featured Products -->
      <LazyHomeFeaturedProducts
        v-if="featuredProductsSection"
        :data="featuredProductsSection"
      />

      <!-- Categories -->
      <LazyHomeCategories v-if="categoriesSection" :data="categoriesSection" />

      <!-- Testimonials -->
      <LazyHomeTestimonials v-if="testimonialsSection" :data="testimonialsSection" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"
import { storeToRefs } from "pinia"
import { useHomepageStore } from "~/stores/modules/homepage/homepageStore"

const homeStore = useHomepageStore()
const { sections, loading, error } = storeToRefs(homeStore)
const { fetchHomepageData } = homeStore

onMounted(() => {
  fetchHomepageData()
})

// ✅ Computed references for each section
const heroSection = computed(() => sections.value.find(s => s.type === "hero"))
const bannerSection = computed(() => sections.value.find(s => s.type === "banner"))
const featuredProductsSection = computed(() => sections.value.find(s => s.type === "products"))
const categoriesSection = computed(() => sections.value.find(s => s.type === "categories"))
const testimonialsSection = computed(() => sections.value.find(s => s.type === "testimonials"))
</script>
