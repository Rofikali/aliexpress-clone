<!-- <template>
    <div id="IndexPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
            <div v-if="products" v-for="product in products" :key="product.id">
                <lazy-product-list :product="product" />
            </div>
            <div ref="sentinelRef" class="h-1"></div>
            <div v-if="isLoading" class="loading">Loading more...</div>
            <div v-if="error" class="error">{{ error.message }}</div>
        </div>
    </div>
</template>

<script setup>
definePageMeta(
    {
        layout: 'default'
    }
)
import { useInfiniteScroll } from '~/composables/pagination/useInfiniteScroll'
import { useUserStore } from '~/stores/user';
const userStore = useUserStore();

const {
    products,
    isLoading,
    error,
    sentinelRef,
    bindSentinel
} = useInfiniteScroll('/products/', {
    pageSize: 12,
    dedupeKey: 'id',
    retries: 2,
    debug: false
})

import { onMounted } from 'vue'
onMounted(() => {
    bindSentinel(sentinelRef)
    setTimeout(() => userStore.isLoading = false, 1000)
})
</script> -->



<!-- <script setup>
import { onMounted } from "vue"
import { useInfiniteScrollProducts } from "~/composables/products/useInfiniteScrollProducts"

const {
    items: products,
    isLoading,
    hasNext,
    error,
    sentinelRef,
    loadMore,
    reset,
} = useInfiniteScrollProducts({ prefetch: true })

onMounted(() => {
    loadMore()
})
</script>

<template>
    <div>
        <div v-for="product in products" :key="product.id" class="p-2 border-b">
            {{ product.name }}
        </div>

        <div ref="sentinelRef" v-if="hasNext && !isLoading" class="text-center py-4">
            Loading more...
        </div>

        <div v-if="isLoading && !products.length" class="text-center py-4">
            Loading products...
        </div>

        <div v-if="error" class="text-red-500">
            {{ error }}
        </div>
    </div>
</template> -->


<script setup>
import { onMounted } from "vue"
import { useProductStore } from "~/stores/modules/productStore"

// Grab store instance
const productStore = useProductStore()

onMounted(() => {
    // optional: only if autoFetch=false in your usePagination
    productStore.fetchFirst()
})
</script>

<template>
    <div>
        <!-- Products list -->
        <div v-if="productStore.products" v-for="product in productStore.products" :key="product.id" class="p-2 border-b">
            {{ product.name }}
        </div>
        <h1>Loading</h1>

        <!-- Infinite scroll sentinel -->
        <div ref="productStore.sentinelRef" v-if="productStore.hasNext && !productStore.loading"
            class="text-center py-4">
            Loading more...
        </div>

        <!-- Loading state -->
        <div v-if="productStore.loading && !productStore.products.length" class="text-center py-4">
            Loading products...
        </div>

        <!-- Error state -->
        <div v-if="productStore.error" class="text-red-500">
            {{ productStore.error }}
        </div>
    </div>
</template>
