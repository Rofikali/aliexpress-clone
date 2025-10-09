<!-- <template>
  <div class="container mx-auto p-4">
    <h1>Home/Category/Id Page </h1>
    {{ products }}
    <lazy-category-products :id='categoryId' />
    Loading State
    <lazy-category-products v-if="products && products.length" :products="products" />
    <div v-if="loading" class="flex justify-center items-center py-20">
      <span class="animate-spin border-4 border-gray-300 border-t-blue-600 rounded-full w-10 h-10"></span>
    </div>

    Error State
    <div v-else-if="error" class="text-red-600 text-center py-10">
      ⚠️ {{ error.message || 'Failed to load category products.' }}
    </div>
  </div>
</template>


<script setup>

import { storeToRefs } from 'pinia';
import { useCategoryProductsStore } from '~/stores/modules/category/categoryPorductStore'
const route = useRoute()
const categoryId = route.params.id
const categoryProductStore = useCategoryProductsStore()

const { products, loading, error } = storeToRefs(categoryProductStore)
const { fetchProductsByCategory } = categoryProductStore



onMounted(async () => {
  console.info("🚀 [Index] Fetching initial products…")
  await fetchProductsByCategory(categoryId)
  console.info("✅ [Index] Initial categoryProducts Loding completed")
})

</script> -->


<!-- <template>
  <div class="container mx-auto p-4">
    <nav class="text-sm text-gray-500 mb-4">
      <NuxtLink to="/">Home</NuxtLink> /
      <span>Hoem/Category/ID </span> /
      <span class="font-semibold">{{ category?.name || 'Loading...' }}</span>
    </nav>

    <h1 class="text-2xl font-bold mb-6 capitalize">
      {{ category?.name || 'Category Products' }}
    </h1>

    <div v-if="error" class="text-red-600 text-center py-10">
      ⚠️ {{ error.message || 'Failed to load category products.' }}
    </div>


    <lazy-category-products v-if="products && products.length" :products="products" :loading="loading"
      :has-next="hasNext" :loadMore="loadMore" />


    <div v-else-if="loading" class="flex justify-center items-center py-20">
      <span class="animate-spin border-4 border-gray-300 border-t-blue-600 rounded-full w-10 h-10"></span>
    </div>


    <div v-else class="text-center py-20 text-gray-500">
      No products found.
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useCategoryProductsStore } from '~/stores/modules/category/categoryPorductStore'

const route = useRoute()
const categoryId = route.params.id


const categoryStore = useCategoryProductsStore()
const { products, loading, hasNext, error } = storeToRefs(categoryStore)
const { fetchProductsByCategory, loadMore } = categoryStore


onMounted(async () => {
  console.info("🚀 Fetching products for category:", categoryId)
  await fetchProductsByCategory(categoryId)
  console.info("✅ Products loaded")
})
</script> -->


<template>
  <div class="container mx-auto p-4">
    <nav class="text-sm text-gray-500 mb-4">
      <NuxtLink to="/">Home</NuxtLink> /
      <span>Category</span> /
      <span class="font-semibold">{{ category?.name || 'Loading...' }}</span>
    </nav>

    <h1 class="text-2xl font-bold mb-6 capitalize">
      {{ category?.name || 'Category Products' }}
    </h1>

    <!-- Error State -->
    <div v-if="error" class="text-red-600 text-center py-10">
      ⚠️ {{ error.message || 'Failed to load category products.' }}
    </div>

    <!-- Pass store data & actions as props -->
    <lazy-category-products v-if="products && products.length" :products="products" :loading="loading"
      :has-next="hasNext" :load-more="loadMore" />

    <!-- Loading state -->
    <div v-else-if="loading" class="flex justify-center items-center py-20">
      <span class="animate-spin border-4 border-gray-300 border-t-blue-600 rounded-full w-10 h-10"></span>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-20 text-gray-500">
      No products found.
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useCategoryProductsStore } from '~/stores/modules/category/categoryPorductStore'

const route = useRoute()
const categoryId = route.params.id

const categoryStore = useCategoryProductsStore()
const { products, loading, hasNext, error, category } = storeToRefs(categoryStore)
const { fetchProductsByCategory, loadMore } = categoryStore

onMounted(async () => {
  console.info("🚀 Fetching products for category:", categoryId)
  await fetchProductsByCategory(categoryId)
  console.info("✅ Products loaded")
})
</script>
