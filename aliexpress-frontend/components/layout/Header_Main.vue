<template>
    <div id="MainHeader" class="flex items-center w-full bg-white">
        <div class="flex lg:justify-start justify-between gap-10 max-w-[1150px] w-full px-3 py-5 mx-auto">

            <!-- Logo -->
            <NuxtLink to="/" class="min-w-[170px]">
                <img width="170" src="/AliExpress-logo.png" alt="Logo" />
            </NuxtLink>

            <!-- Search -->
            <div class="max-w-[700px] w-full md:block hidden">
                <div class="relative">
                    <div class="flex items-center border-2 border-[#FF4646] rounded-md w-full">
                        <input type="search" :value="query" @input="onInput"
                            class="w-full placeholder-gray-400 text-sm pl-3 focus:outline-none"
                            placeholder="kitchen accessories" aria-label="Search products" />

                        <span class="mr-2" v-if="loading && items.length === 0" aria-hidden>
                            <Icon name="eos-icons:loading" size="20" />
                        </span>

                        <button class="flex items-center h-[100%] p-1.5 px-2 bg-[#FF4646]" type="button"
                            aria-label="Search">
                            <Icon name="ph:magnifying-glass" size="20" color="#ffffff" />
                        </button>
                    </div>

                    <!-- Dropdown -->
                    <div v-if="showDropdown" key="search-dropdown"
                        class="absolute bg-white max-w-[700px] h-auto w-full z-50 border mt-1 rounded shadow"
                        role="listbox">
                        <!-- Initial loading -->
                        <div v-if="loading && items.length === 0" class="py-8 text-center" key="loading-initial">
                            Loading...
                        </div>

                        <!-- No results -->
                        <div v-else-if="!loading && items.length === 0 && !error" class="py-8 text-center"
                            key="no-results">
                            No results
                        </div>

                        <!-- Results -->
                        <transition-group name="fade" tag="div" class="divide-y" v-if="items.length"
                            :key="'results-' + items.length">
                            <div v-for="(item, index) in items" :key="item.id || `item-${index}`"
                                class="p-1">
                                <!-- With ID -->
                                <NuxtLink v-if="item.id" :to="{ name: 'product-id', params: { id: item.id } }"
                                    class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100"
                                    role="option">
                                    <div class="flex items-center">
                                        <img v-if="item.url" class="rounded-md" width="40" :src="item.url"
                                            :alt="item.title" />
                                        <div class="truncate ml-2">{{ item.title }}</div>
                                    </div>
                                    <div class="truncate">${{ formatPrice(item.price) }}</div>
                                </NuxtLink>

                                <!-- Without ID -->
                                <div v-else class="flex items-center justify-between w-full p-1">
                                    <div class="flex items-center">
                                        <img v-if="item.url" class="rounded-md" width="40" :src="item.url"
                                            :alt="item.title" />
                                        <div class="truncate ml-2">{{ item.title }}</div>
                                    </div>
                                    <div class="truncate">${{ formatPrice(item.price) }}</div>
                                </div>
                            </div>
                        </transition-group>

                        <!-- Loading more -->
                        <div v-if="loading && items.length > 0" class="py-4 text-center">Loading more…</div>

                        <!-- Scroll sentinel -->
                        <div ref="target" class="h-1" key="scroll-sentinel" aria-hidden></div>

                        <!-- Error -->
                        <div v-if="error" class="text-red-500 mt-4 p-2" key="dropdown-error">
                            {{ error.message ?? String(error) }}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Cart -->
            <NuxtLink to="/shoppingcart" class="flex items-center">
                <button class="relative md:block hidden" @mouseenter="isCartHover = true"
                    @mouseleave="isCartHover = false" type="button">
                    <span
                        class="absolute flex items-center justify-center -right-[3px] top-0 bg-[#FF4646] h-[17px] min-w-[17px] text-xs text-white px-0.5 rounded-full">
                        {{ userStore.cart.length }}
                    </span>
                    <div class="min-w-[40px]">
                        <Icon name="ph:shopping-cart-simple-light" size="33" :color="isCartHover ? '#FF4646' : ''" />
                    </div>
                </button>
            </NuxtLink>

            <!-- Mobile menu -->
            <button @click="userStore.isMenuOverlay = true"
                class="md:hidden block rounded-full p-1.5 -mt-[4px] hover:bg-gray-200" type="button">
                <Icon name="radix-icons:hamburger-menu" size="33" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, computed, watch } from 'vue'
import { useProductSearch } from '~/composables/search/useProductSearch'
import { useUserStore } from '~/stores/user'

const userStore = useUserStore()
const isCartHover = ref(false)

const {
    query,
    items,
    loading,
    error,
    hasNext,
    target,
    search,
    searchImmediate,
    loadMore,
    startObserver,
    stopObserver
} = useProductSearch({ pageSize: 10, debounceMs: 350, autoFetch: false })

// Remove null/invalid items
watch(items, (val) => {
    if (Array.isArray(val)) {
        items.value = val.filter(Boolean)
    }
}, { immediate: true })

const showDropdown = computed(() => {
    const q = (query && query.value) || ''
    return Boolean(q.trim()) || loading.value || items.value.length > 0 || Boolean(error.value)
})

onMounted(async () => {
    await nextTick()
    try {
        startObserver()
    } catch (err) {
        // optional: console.debug('[Header] startObserver failed', err)
    }
})

onBeforeUnmount(() => {
    try {
        stopObserver()
    } catch (e) { }
})

function onInput(e) {
    search(e.target.value)
}

function onClear() {
    searchImmediate('')
}

function formatPrice(price) {
    if (price == null) return '0.00'
    const val = Number(price) / 100
    if (Number.isNaN(val)) return '0.00'
    return val.toFixed(2)
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: all 160ms ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(6px);
}
</style>


<!-- *** Notes  -->
<!-- below code also working fine  -->

<template>
    <div id="MainHeader" class="flex items-center w-full bg-white">
        <div class="flex lg:justify-start justify-between gap-10 max-w-[1150px] w-full px-3 py-5 mx-auto">

            <!-- Logo -->
            <NuxtLink to="/" class="min-w-[170px]">
                <img width="170" src="/AliExpress-logo.png" />
            </NuxtLink>

            <!-- Search -->
            <div ref="searchWrapper" class="max-w-[700px] w-full md:block hidden relative">
                <div class="flex items-center border-2 border-[#FF4646] rounded-md w-full">
                    <input v-model="query" @focus="isOpen = true" type="search" placeholder="kitchen accessories"
                        class="w-full placeholder-gray-400 text-sm pl-3 focus:outline-none" />
                    <button class="flex items-center h-full p-1.5 px-2 bg-[#FF4646]">
                        <Icon name="ph:magnifying-glass" size="20" color="#ffffff" />
                    </button>
                </div>

                <!-- Dropdown -->
                <div v-if="isOpen" ref="dropdown"
                    class="absolute bg-white max-w-[700px] w-full shadow-md mt-1 rounded-md z-50 overflow-y-auto max-h-64"
                    @scroll="onScroll">

                    <!-- Fuzzy search hint -->
                    <div v-if="enableFuzzy && query " class="text-xs text-gray-500 px-2 py-1">
                        Showing approximate matches for "{{ query }}" in {{ fuzzyFields.join(', ') }}
                    </div>

                    <div v-if="loading && items.length === 0" class="py-4 text-center">Loading...</div>
                    <div v-else-if="!loading && items.length === 0" class="py-4 text-center">No results</div>

                    <div v-for="item in items" :key="item.id" class="p-1">
                        <NuxtLink :to="{ name: 'product-id', params: { id: item.id } }"
                            class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100">
                            <div class="flex items-center">
                                <img class="rounded-md" width="40" :src="item.url" />
                                <div class="truncate ml-2">{{ item.title }}</div>
                            </div>
                            <div class="truncate">${{ item.price / 100 }}</div>
                        </NuxtLink>
                    </div>

                    <div v-if="loading && items.length > 0" class="py-2 text-center">Loading more…</div>

                </div>
            </div>

            <!-- Cart -->
            <NuxtLink to="/shoppingcart" class="flex items-center">
                <button class="relative md:block hidden" @mouseenter="isCartHover = true"
                    @mouseleave="isCartHover = false">
                    <span
                        class="absolute flex items-center justify-center -right-[3px] top-0 bg-[#FF4646] h-[17px] min-w-[17px] text-xs text-white px-0.5 rounded-full">
                        {{ userStore.cart.length }}
                    </span>
                    <div class="min-w-[40px]">
                        <Icon name="ph:shopping-cart-simple-light" size="33" :color="isCartHover ? '#FF4646' : ''" />
                    </div>
                </button>
            </NuxtLink>

            <!-- Mobile menu -->
            <button @click="userStore.isMenuOverlay = true"
                class="md:hidden block rounded-full p-1.5 -mt-[4px] hover:bg-gray-200">
                <Icon name="radix-icons:hamburger-menu" size="33" />
            </button>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useUserStore } from '~/stores/user'
import { useProductSearch } from '~/composables/search/useProductSearch'

const userStore = useUserStore()
const searchWrapper = ref(null)
const dropdown = ref(null)
const isOpen = ref(false)
const isCartHover = ref(false)

// --- Product search composable ---
const { query, items, loading, search, loadMore, hasNext } = useProductSearch({
    pageSize: 10,
    debounceMs: 350,
    autoFetch: false,
    autoStartObserver: false,
    enableFuzzy: true,
    fuzzyFields: ['title', 'description']
})

// --- Debounced search ---
watch(query, (val) => {
    search(val)
})

// --- Click outside ---
function onClickOutside(e) {
    if (searchWrapper.value && !searchWrapper.value.contains(e.target)) {
        isOpen.value = false
    }
}

// --- Infinite scroll on dropdown ---
function onScroll() {
    if (!dropdown.value || loading.value || !hasNext.value) return
    const { scrollTop, clientHeight, scrollHeight } = dropdown.value
    if (scrollTop + clientHeight >= scrollHeight - 10) {
        loadMore()
    }
}

// --- Adaptive auto-fill ---
async function autoFillDropdown() {
    if (!dropdown.value) return
    const maxLoops = 10
    let loops = 0
    while (hasNext.value && dropdown.value.scrollHeight <= dropdown.value.clientHeight && loops < maxLoops) {
        await loadMore()
        await nextTick()
        loops++
    }
}

onMounted(() => {
    document.addEventListener('click', onClickOutside)
    nextTick(() => autoFillDropdown())
})

onBeforeUnmount(() => {
    document.removeEventListener('click', onClickOutside)
})
</script>
