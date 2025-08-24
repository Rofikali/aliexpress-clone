<template>
    <div id="IndexPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
            <div v-if="products" v-for="product in products" :key="product.id">
                <lazy-product-list :product="product" />
            </div>
            <!-- Sentinel to trigger loading more -->
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
// import lazyProductList from '~/components/lazy-product-list.vue'
import { useInfiniteScroll } from '~/composables/pagination/useInfiniteScroll'
import { useUserStore } from '~/stores/user';
const userStore = useUserStore();

const {
    products,
    isLoading,
    error,
    sentinelRef,
    bindSentinel
} = useInfiniteScroll('/api/v1/products/', {
    pageSize: 12,
    dedupeKey: 'id',
    retries: 2,
    debug: false
})

// console.log('inside products ', products);

// Bind the sentinel ref when component mounts
import { onMounted } from 'vue'
// import { LazyProductList } from '#components';
onMounted(() => {
    bindSentinel(sentinelRef)
    setTimeout(() => userStore.isLoading = false, 1000)
})
</script>
