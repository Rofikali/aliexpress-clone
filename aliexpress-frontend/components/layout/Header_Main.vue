<template>
    <div id="MainHeader" class="flex items-center w-full bg-white">
        <div class="flex lg:justify-start justify-between gap-10 max-w-[1150px] w-full px-3 py-5 mx-auto">


            <NuxtLink to="/" class="min-w-[170px]">
                <img width="170" src="/AliExpress-logo.png" alt="Logo" />
            </NuxtLink>


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


                    <div v-if="showDropdown" key="search-dropdown"
                        class="absolute bg-white max-w-[700px] h-auto w-full z-50 border mt-1 rounded shadow"
                        role="listbox">
                        <!-- Initial loading -->
                        <div v-if="loading && items.length === 0" class="py-8 text-center" key="loading-initial">
                            Loading...
                        </div>


                        <div v-else-if="!loading && items.length === 0 && !error" class="py-8 text-center"
                            key="no-results">
                            No results
                        </div>


                        <transition-group name="fade" tag="div" class="divide-y" v-if="items.length"
                            :key="'results-' + items.length">
                            <div v-for="item in items" :key="item.id" class="p-1">

                                <NuxtLink v-if="item?.id" :to="{ name: 'product-id', params: { id: item.id } }"
                                    class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100"
                                    role="option">
                                    <div class="flex items-center">
                                        <img v-if="item.url" class="rounded-md" width="40" :src="item.url"
                                            :alt="item.title" />
                                        <div class="truncate ml-2">{{ item.title }}</div>
                                    </div>
                                    <div class="truncate">${{ formatPrice(item.price) }}</div>
                                </NuxtLink>


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


                        <div v-if="loading && items.length > 0" class="py-4 text-center">Loading more…</div>


                        <div ref="target" class="h-1" key="scroll-sentinel" aria-hidden></div>

                        <div v-if="error" class="text-red-500 mt-4 p-2" key="dropdown-error">
                            {{ error.message ?? String(error) }}
                        </div>
                    </div>
                </div>
            </div>


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


            <button @click="userStore.isMenuOverlay = true"
                class="md:hidden block rounded-full p-1.5 -mt-[4px] hover:bg-gray-200" type="button">
                <Icon name="radix-icons:hamburger-menu" size="33" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useProductSearch } from '~/composables/search/useProductSearch'
import { useUserStore } from '~/stores/user'
// import Icon from '#components/Icon' // adjust if your Icon component is globally available

// Pinia store for cart / UI
const userStore = useUserStore()

// local reactive state
const isCartHover = ref(false)

// use product search composable (production-ready)
const {
    query,
    items,
    loading,
    error,
    hasNext,
    target, // ref from composable — this will be bound to the sentinel
    search,
    searchImmediate,
    loadMore,
    startObserver,
    stopObserver
} = useProductSearch({ pageSize: 10, debounceMs: 350, autoFetch: false })

// Derived flag that controls dropdown rendering:
// show when user has typed a query OR we have loading/results/error
const showDropdown = computed(() => {
    // only show dropdown when query exists OR during active states
    const q = (query && query.value) || ''
    return Boolean(q.trim()) || loading.value || items.value.length > 0 || Boolean(error.value)
})

// Ensure observer starts only after DOM is ready (target ref exists)
onMounted(async () => {
    await nextTick()
    // start observer only if target is available
    try {
        if (target && target.value) {
            startObserver()
        } else {
            // composable's startObserver is safe-guarded but being defensive is good
            startObserver()
        }
    } catch (err) {
        // swallow observer start errors; keep header usable
        // optional: console.debug('[Header] startObserver failed', err)
    }
})

// Clean up observer on unmount to avoid callbacks touching removed DOM
onBeforeUnmount(() => {
    try {
        stopObserver()
    } catch (e) {
        /* noop */
    }
})

// Input handlers
function onInput(e) {
    search(e.target.value)
}

function onClear() {
    searchImmediate('')
}

// small helper to format price safely
function formatPrice(price) {
    if (price == null) return '0.00'
    // if price stored in cents: divide by 100
    const val = Number(price) / 100
    if (Number.isNaN(val)) return '0.00'
    return val.toFixed(2)
}
</script>

<style scoped>
/* small fade transition for results (optional) */
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
