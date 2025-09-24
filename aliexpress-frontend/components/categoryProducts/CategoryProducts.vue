<!-- <script setup>
import { onMounted } from "vue"
import { useCategoryStore } from "~/stores/modules/category/categoryStore"

const route = useRoute()
const categoryId = route.params.id
const categoryStore = useCategoryStore()

onMounted(() => {
  categoryStore.fetchFirst(categoryId)
})


</script>

<template>
  <section>
    <header v-if="categoryStore.category">
      <h1>{{ categoryStore.category.name }}</h1>
      <p>{{ categoryStore.category.description }}</p>
    </header>

    <div v-if="categoryStore.error" class="error">
      {{ categoryStore.error.message || 'Error loading category' }}
    </div>

    <ul>
      <li v-for="p in categoryStore.products" :key="p.id">
        <h1>Category Name - {{ p.category.name }}</h1>
         <NuxtLink :to="{ name: 'products-id', params: { id: p.id } }" class="block"><h3>{{ p.title }}</h3></NuxtLink>
        <img :src="p.image" :alt="p.title" />
        <p>{{ p.price }} {{ p.currency }}</p>
      </li>
    </ul>

    <div v-if="categoryStore.loading">Loading...</div>
    <div v-if="!categoryStore.hasNext">No more products</div>
  </section>
</template> -->



<template>
  <div id="CategoryPage" class="mt-4 max-w-[1200px] mx-auto px-2">
    <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
      <!-- Render products -->
      <div v-if="products" v-for="product in products" :key="product.id">
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
import { onMounted } from "vue"
import { storeToRefs } from "pinia"
import { useCategoryStore } from "~/stores/modules/category/categoryStore"
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

const route = useRoute()
const categoryId = route.params.id

const categoryStore = useCategoryStore()
const { products, loading, hasNext, error, category } = storeToRefs(categoryStore)
const { fetchFirst, loadMore } = categoryStore

// ✅ Hook up useInfiniteScroll
const { sentinelRef, bindSentinel } = useInfiniteScroll({
  loadMore: () => loadMore(categoryId), // pass categoryId
  hasNext,
  isLoading: loading,
  prefetch: true,
  debug: true,
})

// Initial load
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
</style>
