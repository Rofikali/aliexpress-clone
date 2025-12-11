<!-- <template>
    <div class="absolute bg-white max-w-[700px] h-auto w-full">
        <div v-if="items && items.data" v-for="item in items.data" :key="item.id" class="p-1">
            <NuxtLink :to="`/item/${item.id}`"
                class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100">
                <div class="flex items-center">
                    <img class="rounded-md" width="40" :src="item.url">
                    <div class="truncate ml-2">{{ item.title }}</div>
                </div>
                <div class="truncate">${{ item.price / 100 }}</div>
            </NuxtLink>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    Items: {
        type: String,
        required: false, // true
        default: () => null
    }
})

</script>

<style scoped></style> -->

<template>
  <div class="w-full">
    <!-- Search input (controlled by useInfiniteSearch) -->
    <SearchQuery v-model="searchQuery" :placeholder="placeholder" :aria-label="ariaLabel">
      <template #icon>
        <Icon name="ph:magnifying-glass" size="20" />
      </template>
    </SearchQuery>

    <div class="absolute bg-white max-w-[700px] h-auto w-full">
      <div v-if="products.length" v-for="(item, idx) in products" :key="item[dedupeKey] ?? idx" :item="item"
        :index="idx" class="p-1">
        <NuxtLink :to="{ name: 'product-id', params: { id: 100 } }"
          class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100">
          <div class="flex items-center">
            <img class="rounded-md" width="40" :src="item.url">
            <div class="truncate ml-2">{{ item.title }}</div>
          </div>
          <div class="truncate">${{ item.price / 100 }}</div>
        </NuxtLink>
      </div>
    <!-- </div> -->

    <!-- Results container -->
    <!-- <div class="relative w-full" :class="resultsWrapperClass" role="list" aria-live="polite">
      List
      <div v-if="products.length" :class="listClass">
        <slot name="item" v-for="(item, idx) in products" :key="item[dedupeKey] ?? idx" :item="item" :index="idx">
          Default item rendering (fallback)
          <div class="p-2 border rounded-md">
            <pre class="text-xs whitespace-pre-wrap">{{ item }}</pre>
          </div>
        </slot>
      </div> -->

      <!-- Empty state -->
      <div v-else-if="!isLoading" class="text-center text-sm text-gray-500 py-4">
        <slot name="empty">No results found.</slot>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="text-center text-sm text-gray-500 py-3">
        <slot name="loading">Loading…</slot>
      </div>

      <!-- Error -->
      <div v-if="error" class="text-center text-sm text-red-600 py-3">
        <slot name="error">Error - {{ friendlyError }}</slot>
      </div>

      <!-- Infinite scroll sentinel -->
      <div ref="sentinelRef" class="h-[1px] w-full"></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import SearchQuery from './SearchQuery.vue'
import { useInfiniteSearch } from '~/app/composables/search/useProductSearch'

const props = defineProps({
  baseUrl: { type: String, required: true },
  queryParam: { type: String, default: 'q' },
  debounceMs: { type: Number, default: 350 },
  dedupeKey: { type: String, default: 'id' },

  // response shape plumbing (forwarded to usePagination)
  itemsPath: { type: [String, Array], default: undefined },
  nextCursorPath: { type: String, default: undefined },
  hasNextPath: { type: String, default: undefined },

  // optional initial params (e.g. filters)
  params: { type: Object, default: () => ({}) },

  // UI classes
  placeholder: { type: String, default: 'Search…' },
  ariaLabel: { type: String, default: 'Search' },
  resultsWrapperClass: { type: String, default: '' },
  listClass: { type: String, default: 'grid gap-2' },
})

const {
  searchQuery,
  products,
  isLoading,
  error,
  sentinelRef,
} = useInfiniteSearch(props.baseUrl,
  {
    queryParam: props.queryParam,
    debounceMs: props.debounceMs,
    params: props.params,
    dedupeKey: props.dedupeKey,

    // shape config
    itemsPath: props.itemsPath,
    nextCursorPath: props.nextCursorPath,
    hasNextPath: props.hasNextPath,

    // performance
    prefetch: true,
    maxFillLoops: 15,
    debug: false,
  })

const friendlyError = computed(() => {
  if (!error || !error.message) return 'Something went wrong.'
  return error.message
})
</script>

<style scoped>
/* keep styling minimal; pass Tailwind classes via props when you embed the component */
</style>
