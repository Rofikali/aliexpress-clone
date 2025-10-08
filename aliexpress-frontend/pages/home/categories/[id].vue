<template>
  <div class="container mx-auto p-4">
    <h1>Home/Category/Id Page </h1>
{{ products }}
    <!-- <lazy-category-products :id='categoryId' /> -->
  </div>
</template>


<script setup>

import { storeToRefs } from 'pinia';
import { useCategoryProductsStore } from '~/stores/modules/category/categoryPorductStore'
// import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"
const route = useRoute()
const categoryId = route.params.id
const categoryProductStore = useCategoryProductsStore()

const { products, loading, hasNext, error } = storeToRefs(categoryProductStore)
const { fetchCategoryProducts, loadMore } = categoryProductStore


// ✅ Hook up useInfiniteScroll
// const { sentinelRef, bindSentinel } = useInfiniteScroll({
//   loadMore,
//   hasNext,
//   loading,
//   prefetch: true, // auto load when visible
//   debug: true,    // optional logging
// })


onMounted(async () => {
  console.info("🚀 [Index] Fetching initial products…")
  await fetchCategoryProducts(categoryId)
  console.info("✅ [Index] Initial categoryProducts Loding completed")
  // bindSentinel(sentinelRef)
})

</script>
