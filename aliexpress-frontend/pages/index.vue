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
import { useProductStore } from "~/stores/modules/productStore";

const productStore = useProductStore();
console.log('inside productsStore is ', productStore);
await useAsyncData("products", () => productStore.fetchProducts({ page: 1 }));
</script>

<template>
    <div class="p-6">
        <h1 class="text-2xl font-bold mb-4">Products</h1>


        <div v-if="productStore.loading" class="text-gray-500">Loading...</div>


        <div v-else-if="productStore.error" class="text-red-600">
            {{ productStore.error }}
        </div>

        <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="product in productStore.products" :key="product.id"
                class="border p-4 rounded-lg shadow-sm hover:shadow-md">
                <img v-if="product.image" :src="product.image" alt="product" class="w-full h-40 object-cover mb-2" />
                <h2 class="font-semibold">{{ product.title }}</h2>
                <p class="text-sm text-gray-500">{{ product.category?.name }}</p>
                <p class="text-lg font-bold mt-1">${{ product.price }}</p>
            </div>
        </div>


        <div class="flex justify-between mt-6">
            <button v-if="productStore.pagination.previous" @click="productStore.fetchProducts({ page: 1 })"
                class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
                Prev
            </button>
            <button v-if="productStore.pagination.next" @click="productStore.fetchProducts({ page: 2 })"
                class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
                Next
            </button>
        </div>
    </div>
</template> -->

<template>
    <div id="IndexPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
            <div v-if="products" v-for="product in products" :key="product.id">
                <lazy-product-list :product="product" />
            </div>

            <!-- Sentinel -->
            <div ref="sentinelRef" class="h-1"></div>

            <!-- Loading / Error states -->
            <div v-if="loading" class="loading">Loading more...</div>
            <div v-if="error" class="error">{{ error }}</div>
        </div>
    </div>
</template>

<script setup>
definePageMeta({
    layout: "default",
});

import { onMounted } from "vue";
import { useUserStore } from "~/stores/user";
import { useProductStore } from "~/stores/modules/productStore";
import { useInfiniteProducts } from "~/composables/products/useInfiniteProducts";

const userStore = useUserStore();
const store = useProductStore();

// infinite scroll composable (observer only)
const { products, loading, error, sentinelRef, bindSentinel } =
    useInfiniteProducts({ pageSize: 12, debug: false });

console.log('products in index page ', products);

onMounted(async () => {
    // initial fetch
    if (!products.length) {
        await store.fetchProducts({ page_size: 12 });
    }
    bindSentinel(sentinelRef);

    // simulate userStore loading fadeout
    setTimeout(() => (userStore.isLoading = false), 300);
});
</script>
