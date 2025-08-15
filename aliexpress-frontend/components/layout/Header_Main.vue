<template>
    <div id="MainHeader" class="flex items-center w-full bg-white">
        <div class="flex lg:justify-start justify-between gap-10 max-w-[1150px] w-full px-3 py-5 mx-auto">

            <NuxtLink to="/" class="min-w-[170px]">
                <img width="170" src="/AliExpress-logo.png" />
            </NuxtLink>

            <div ref="searchWrapper" class="max-w-[700px] w-full md:block hidden relative">
                <div class="flex items-center border-2 border-[#FF4646] rounded-md w-full">
                    <input v-model="query" @focus="isOpen = true" type="search" placeholder="kitchen accessories"
                        class="w-full placeholder-gray-400 text-sm pl-3 focus:outline-none" />
                    <button class="flex items-center h-full p-1.5 px-2 bg-[#FF4646]">
                        <Icon name="ph:magnifying-glass" size="20" color="#ffffff" />
                    </button>
                </div>

                <div v-if="isOpen" class="absolute bg-white max-w-[700px] w-full shadow-md mt-1 rounded-md z-50">
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

                    <div ref="target" class="h-1"></div>
                </div>
            </div>

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
const searchWrapper = ref(null)
const isOpen = ref(false)
const isCartHover = ref(false)

const { query, items, loading, search } = useProductSearch({ pageSize: 10, debounceMs: 350 })

// Watch query for debounced search
watch(query, (val) => {
    search(val)
})

// Click outside to close dropdown
function onClickOutside(e) {
    if (searchWrapper.value && !searchWrapper.value.contains(e.target)) {
        isOpen.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', onClickOutside)
})

onBeforeUnmount(() => {
    document.removeEventListener('click', onClickOutside)
})
</script>
