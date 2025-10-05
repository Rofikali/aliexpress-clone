<template>
  <div class="product-detail-page">
    <h1>Home page Details</h1>
    <!-- <h2 v-if="banner">{{ banner }}</h2>
    <h2 v-else-if="bannerError">error {{ bannerError }} ..........</h2>
    <h2 v-else>Banner not found </h2> -->
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { storeToRefs } from 'pinia'
// import { useHomepageStore } from "~/stores/modules/homepage/homepageStore"


// const route = useRoute()
// const id = route.params.id
// const homepageStore = useHomepageStore()
// const { banner, bannerLoading, bannerError } = storeToRefs(homepageStore)
// const {  getHomepageDataById } = homepageStore

// // ✅ Load product and related products
// onMounted(async () => {
//   bannerLoading.value = true
//   await getHomepageDataById(id)
// })

</script>

<style scoped>

</style>


