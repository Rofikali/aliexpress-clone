<!-- <template>
  <div id="CategoryPage" class="mt-4 max-w-[1200px] mx-auto px-2">
    Categories Listing from Homepage
    <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">

      <div v-if="products" v-for="product in products" :key="product.id">
        <lazy-products-product-list :product="product" />
      </div>


      <div ref="sentinelRef" class="h-1"></div>

      <div v-if="loading" class="loading">Loading more...</div>
      <div v-if="error" class="error">{{ error.message }}</div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useCategoryProductsStore } from '~/stores/modules/category/categoryPorductStore'
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

const route = useRoute()
const categoryId = route.params.id

const categoryStore = useCategoryProductsStore()
const { products, loading, hasNext, error } = storeToRefs(categoryStore)
const { fetchFirst, loadMore } = categoryStore

const { sentinelRef, bindSentinel } = useInfiniteScroll({
  loadMore: () => loadMore(categoryId), // pass categoryId
  hasNext,
  isLoading: loading,
  prefetch: true,
  debug: true,
})


onMounted(async () => {
  console.info("🚀 [Category] Fetching products for category:", categoryId)
  await fetchFirst(categoryId)
  console.info("✅ [Category] Initial load complete")

  bindSentinel(sentinelRef)
})
</script>

<style scoped>
.loading,
.end {
  text-align: center;
  padding: 1rem;
  font-weight: bold;
}
</style> -->


<template>
  <div id="CategoryPage" class="mt-4 max-w-[1200px] mx-auto px-2">
    <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
      <!-- Render products -->
      <div v-for="product in products" :key="product.id">
        <lazy-products-product-list :product="product" />
      </div>

      <!-- 👇 sentinel controlled by useInfiniteScroll -->
      <div ref="sentinelRef" class="h-1"></div>

      <div v-if="loading" class="loading">Loading more...</div>
      <div v-if="error" class="error">{{ error.message }}</div>
    </div>
  </div>
</template>

<script setup>
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

const props = defineProps({
  products: Array,
  loading: Boolean,
  hasNext: Boolean,
  loadMore: Function,
  error: Object
})

// ✅ Hook up infinite scroll using props
const { sentinelRef, bindSentinel } = useInfiniteScroll({
  loadMore: props.loadMore,
  hasNext: toRef(props, 'hasNext'),
  isLoading: toRef(props, 'loading'),
  prefetch: true,
  debug: true,
})

onMounted(() => {
  bindSentinel(sentinelRef)
})
</script>

<style scoped>
.loading {
  text-align: center;
  padding: 1rem;
  font-weight: bold;
}
</style>
