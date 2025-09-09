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


<!-- <script setup>
import { onMounted } from "vue"
import { useProductStore } from "~/stores/modules/productStore"


const productStore = useProductStore()

onMounted(() => {

    productStore.fetchFirst()
})
</script>

<template>
    <div>

        <div v-if="productStore.products" v-for="product in productStore.products" :key="product.id" class="p-2 border-b">
            {{ product.name }}
        </div>
        <h1>Loading</h1>


        <div ref="productStore.sentinelRef" v-if="productStore.hasNext && !productStore.loading"
            class="text-center py-4">
            Loading more...
        </div>


        <div v-if="productStore.loading && !productStore.products.length" class="text-center py-4">
            Loading products...
        </div>


        <div v-if="productStore.error" class="text-red-500">
            {{ productStore.error }}
        </div>
    </div>
</template> -->




<!-- <template>
    <div class="products-container">

        <div v-if="productStore.products.length" class="products-grid">
            <div v-for="product in productStore.products" :key="product.id" class="product-card">
                <img :src="product.image" :alt="product.title" class="product-image" />
                <h3 class="product-title">{{ product.title }}</h3>
                <p class="product-price">${{ product.price }}</p>
            </div>
        </div>


        <div v-else-if="!productStore.loading && !productStore.error" class="empty-state">
            No products found.
        </div>


        <div v-if="productStore.loading" class="loading-state">
            Loading products...
        </div>


        <div v-if="productStore.error" class="error-state">
            Error: {{ productStore.error.message || "Something went wrong." }}
        </div>

 
        <div ref="sentinelRef" v-if="productStore.hasNext && !productStore.loading && !productStore.error"
            class="infinite-scroll-sentinel">
            Loading more products...
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue"
import { useProductStore } from "~/stores/modules/productStore"
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

const productStore = useProductStore()
const sentinelRef = ref(null)


const { bindSentinel, unbindSentinel } = useInfiniteScroll({
    loadMore: productStore.loadMore,
    hasNext: productStore.hasNext,
    isLoading: productStore.loading,
    threshold: 0.25,
    prefetch: true,
})

onMounted(async () => {
    const response = await productStore.fetchFirst()
    setTimeout(() => productStore.loading = false, 200)

    if (!productStore.error && response?.status === 200) {
        console.log(`✅ ${productStore.products.length} products loaded successfully!`)
    }

    if (sentinelRef.value) bindSentinel(sentinelRef.value)
})

onUnmounted(() => {
    unbindSentinel()
})

watch(
    () => productStore.products,
    (newVal) => {
        if (newVal.length && productStore.hasNext && sentinelRef.value) {
            bindSentinel(sentinelRef.value)
        }
    }
)
</script>

<style scoped>
.products-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}

.product-card {
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    overflow: hidden;
    padding: 0.5rem;
    text-align: center;
}

.product-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
}

.product-title {
    font-size: 1rem;
    margin: 0.5rem 0 0.25rem;
}

.product-price {
    font-size: 0.9rem;
    color: #555;
}

.loading-state,
.error-state,
.empty-state,
.infinite-scroll-sentinel {
    text-align: center;
    padding: 1rem;
    color: #777;
}
</style> -->


<template>
    <div class="products-container">
        <!-- Products List -->
        <div v-if="productStore.products.length" class="products-grid">
            <div v-for="product in productStore.products" :key="product.id" class="product-card">
                <!-- <img :src="product.image" :alt="product.title" class="product-image" /> -->
                <!-- <h3 class="product-title">{{ product.title }}</h3> -->
                <!-- <p class="product-price">${{ product.price }}</p> -->
                <lazy-product-list :product="product" />
            </div>
        </div>

        <!-- Empty State -->
        <div v-else-if="!productStore.loading && !productStore.error" class="empty-state">
            No products found.
        </div>

        <!-- Loading Spinner -->
        <div v-if="productStore.loading" class="loading-state">
            Loading products...
        </div>

        <!-- Error Message -->
        <div v-if="productStore.error" class="error-state">
            <div v-for="(err, idx) in productStore.error" :key="idx">
                ❌ {{ err.message || "Something went wrong." }}
            </div>
        </div>

        <!-- Infinite Scroll Sentinel -->
        <div ref="sentinelRef" v-if="productStore.hasNext && !productStore.loading && !productStore.error"
            class="infinite-scroll-sentinel">
            Loading more products...
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from "vue"
import { useProductStore } from "~/stores/modules/productStore"
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

const productStore = useProductStore()
const sentinelRef = ref(null)

// Infinite Scroll Setup
const { bindSentinel, unbindSentinel } = useInfiniteScroll({
    loadMore: productStore.loadMore,
    hasNext: productStore.hasNext,
    isLoading: productStore.loading,
    threshold: 0.25,
    prefetch: true,
})

onMounted(async () => {
    const response = await productStore.fetchFirst()
    setTimeout(() => productStore.loading = false, 300)

    if (response.success) {
        console.log(
            `✅ ${productStore.products.length} products loaded | Request ID: ${response.request?.id} | Region: ${response.request?.region} | Cache: ${response.request?.cache}`
        )
    } else {
        console.error("❌ Initial fetch failed:", response.errors)
    }

    if (sentinelRef.value) bindSentinel(sentinelRef.value)
})

onUnmounted(() => {
    unbindSentinel()
})

// Watch for new products to re-bind sentinel automatically
watch(
    () => productStore.products,
    (newVal) => {
        if (newVal.length && productStore.hasNext && sentinelRef.value) {
            bindSentinel(sentinelRef.value)
        }
    }
)
</script>

<style scoped>
.products-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
}

.product-card {
    border: 1px solid #ddd;
    border-radius: 0.5rem;
    overflow: hidden;
    padding: 0.5rem;
    text-align: center;
}

.product-image {
    width: 100%;
    height: 150px;
    object-fit: cover;
}

.product-title {
    font-size: 1rem;
    margin: 0.5rem 0 0.25rem;
}

.product-price {
    font-size: 0.9rem;
    color: #555;
}

.loading-state,
.error-state,
.empty-state,
.infinite-scroll-sentinel {
    text-align: center;
    padding: 1rem;
    color: #777;
}
</style>
