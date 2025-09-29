<template>
    <div>
all category
 <div id="IndexPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <div class="grid xl:grid-cols-6 lg:grid-cols-5 md:grid-cols-4 sm:grid-cols-3 grid-cols-2 gap-4">
            <div v-if="categories">
                 <lazy-products-categories :categories="categories" />
            </div>

            <!-- 👇 sentinel controlled by useInfiniteScroll -->
            <div ref="sentinelRef" class="h-1"></div>

            <div v-if="loading" class="loading">Loading more...</div>
            <div v-if="error" class="error">{{ error.message }}</div>
        </div>
    </div>
    </div>
</template>

<script setup>
import { storeToRefs } from 'pinia';
import {  useCategoryStore } from '~/stores/modules/category/categoryStore'
import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

const categoryStore = useCategoryStore()

const { categories, loading, hasNext, error } = storeToRefs(categoryStore)
const { fetchCategories, loadMore } = categoryStore


// ✅ Hook up useInfiniteScroll
const { sentinelRef, bindSentinel } = useInfiniteScroll({
    loadMore,
    hasNext,
    loading,
    prefetch: true, // auto load when visible
    debug: true,    // optional logging
})

// Initial load
onMounted(async ()=> {
    console.info("🚀 [Index] Fetching initial products…")
    await fetchCategories()
    console.info("✅ [Index] Initial load complete")

    // bind sentinel AFTER initial load
    bindSentinel(sentinelRef)
})



</script>

<style  scoped>

</style>