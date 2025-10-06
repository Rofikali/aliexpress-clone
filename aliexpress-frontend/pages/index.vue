
<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Homepage</h1>

    <div v-if="loading" class="text-center py-10">Loading homepage...</div>
    <div v-else-if="error" class="text-center text-red-500 py-10">
      {{ error.message || "Something went wrong" }}
    </div>

    <div v-else>
      <strong>Hero Section</strong>
      <LazyHomeHero v-if="heroSection" :data="heroSection.data" />
      <br>

      <strong>Banner Section</strong>
      <LazyHomeBanner v-if="bannerSection" :data="bannerSection.data" />

      <strong>Featured Products</strong>

      <!-- {{ featuredProductsSection }}</h1> -->
      <LazyHomeFeaturedProducts
        v-if="featuredProductsSection"
        :data="featuredProductsSection.data"
      />

      <h1>Categoires Data </h1>
      <!-- {{ categoriesSection.data }} -->
      <LazyHomeCategories v-if="categoriesSection" :data="categoriesSection.data" />

      <!-- <h1>Promotions - {{ promotions }}</h1> -->
      <LazyHomePromoSection 
        v-if="promotions" 
        :data="promotions.data" 
      />
      <div v-else>No promotions data</div>

      <strong>For Feauture Plan</strong>
      <LazyHomeTestimonials v-if="testimonialsSection" :data="testimonialsSection.data" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"
import { storeToRefs } from "pinia"
import { useHomepageStore } from "~/stores/modules/homepage/homepageStore"

const homeStore = useHomepageStore()
const { sections, loading, error } = storeToRefs(homeStore)
console.log('sectins in index.vue ', sections);
const { fetchHomepageData } = homeStore

onMounted(() => {
  fetchHomepageData()
})

const heroSection = computed(() => sections.value.find(s => s.type === "hero"))
const bannerSection = computed(() => sections.value.find(s => s.type === "banner"))
const featuredProductsSection = computed(() => sections.value.find(s => s.type === "products"))
const categoriesSection = computed(() => sections.value.find(s => s.type === "categories"))
const promotions = computed(() => {
  return sections.value.find(s => s.type === "promo");
});
// for future 
const testimonialsSection = computed(() => sections.value.find(s => s.type === "testimonials"))

</script>

<style scoop>
</style>
