<template>
    <div id="MainHeader" class="flex items-center w-full bg-white">
        <div class="flex lg:justify-start justify-between gap-10 max-w-[1150px] w-full px-3 py-5 mx-auto">

            <!-- Logo -->
            <NuxtLink to="/" class="min-w-[170px]">
                <img width="170" src="/AliExpress-logo.png" />
            </NuxtLink>

            <!-- Search -->
            <div ref="searchWrapper" class="relative max-w-[700px] w-full md:block hidden">
                <div class="flex items-center border-2 border-[#FF4646] rounded-md w-full">
                    <input v-model="query" @focus="isOpen = true" @input="onSearchInput" type="search"
                        placeholder="kitchen accessories"
                        class="w-full placeholder-gray-400 text-sm pl-3 focus:outline-none" />
                    <Icon v-if="loading && items.length === 0" name="eos-icons:loading" size="25" class="mr-2" />
                    <button class="flex items-center h-[100%] p-1.5 px-2 bg-[#FF4646]">
                        <Icon name="ph:magnifying-glass" size="20" color="#ffffff" />
                    </button>
                </div>

                <!-- Dropdown -->
                <div v-if="isOpen && (loading || items.length)"
                    class="absolute bg-white max-w-[700px] h-auto w-full shadow-lg mt-1 rounded-md z-50">
                    <div v-if="loading && items.length === 0" class="py-8 text-center">Loading...</div>
                    <div v-else-if="!loading && items.length === 0" class="py-8 text-center">No results</div>

                    <!-- <div v-for="item in items" :key="item.id" class="p-1"> -->
                    <div v-for="item in items" :key="item.id ?? item.tempId" class="p-1">

                        <NuxtLink :to="{ name: 'product-id', params: { id: item.id } }"
                            class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100">
                            <div class="flex items-center">
                                <img class="rounded-md" width="40" :src="item.url" />
                                <div class="truncate ml-2">{{ item.title }}</div>
                            </div>
                            <div class="truncate">${{ item.price / 100 }}</div>
                        </NuxtLink>
                    </div>

                    <div v-if="loading && items.length > 0" class="py-4 text-center">Loading more…</div>

                    <!-- Sentinel for infinite scroll -->
                    <div ref="target" class="h-1"></div>
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
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useUserStore } from '~/stores/user'
import { useProductSearch } from '~/composables/search/useProductSearch'

const userStore = useUserStore()
const { query, items, loading, error, hasNext, target, search, searchImmediate, loadMore, startObserver } =
    useProductSearch({ pageSize: 10, debounceMs: 300, autoFetch: false })

// Reactive for dropdown open/close
const isOpen = ref(false)
const searchWrapper = ref(null)

// Dropdown closes on outside click
function onClickOutside(e) {
    if (searchWrapper.value && !searchWrapper.value.contains(e.target)) {
        isOpen.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', onClickOutside)
    startObserver()
})

onBeforeUnmount(() => {
    document.removeEventListener('click', onClickOutside)
})

// Input handler
function onSearchInput() {
    search(query.value) // debounced search
}

// Cart hover
const isCartHover = ref(false)
</script>
<!-- 

<script setup>
import { ref, onMounted } from 'vue'
import { useProductSearch } from '~/composables/search/useProductSearch'
import { useUserStore } from '~/stores/user'

const userStore = useUserStore()
const isCartHover = ref(false)

// Use cached product search composable
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
    startObserver
} = useProductSearch({ pageSize: 10, debounceMs: 350, autoFetch: false })

onMounted(() => {
    if (target.value) startObserver()
})

// Debounced input handler
function onInput(e) {
    search(e.target.value)
}

// Clear search
function onClear() {
    searchImmediate('')
}
</script> -->
