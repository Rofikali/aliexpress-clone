<template>
    <div id="MainHeader" class="flex items-center w-full bg-white">
        <div class="flex lg:justify-start justify-between gap-10 max-w-[1150px] w-full px-3 py-5 mx-auto">


            <NuxtLink to="/" class="min-w-[170px]">
                <img width="170" src="/AliExpress-logo.png" />
            </NuxtLink>

            <NuxtLink :to="{ name: 'category'}" class="mx-auto">
                <strong>Categories</strong>
            </NuxtLink>

            <NuxtLink to="/products" class="max-auto">
                <strong>Products</strong>
            </NuxtLink>

            <div ref="searchWrapper" class="max-w-[700px] w-full md:block hidden relative">
                <div class="flex items-center border-2 border-[#FF4646] rounded-md w-full">
                    <input v-model="query" @focus="isOpen = true" type="search" placeholder="kitchen accessories"
                        class="w-full placeholder-gray-400 text-sm pl-3 focus:outline-none" />
                    <!-- <span class="mr-2" v-if="loading && items.length === 0" aria-hidden>
                        <Icon name="eos-icons:loading" size="20" />
                    </span> -->
                    <button class="flex items-center h-full p-1.5 px-2 bg-[#FF4646]">
                        <Icon name="ph:magnifying-glass" size="20" color="#ffffff" />
                    </button>
                </div>


                <div v-if="isOpen" ref="dropdown" :style="{ maxHeight: `${dropdownMaxHeight}px` }"
                    class="absolute bg-white max-w-[700px] w-full shadow-md mt-1 rounded-md z-50 overflow-y-auto"
                    @scroll="onScroll">

                    <div v-if="enableFuzzy && query" class="text-xs text-gray-500 px-2 py-1">
                        Showing approximate matches for "{{ query }}" in {{ fuzzyFields.join(', ') }}
                    </div>


                    <div v-else-if="!loading && items.length === 0" class="py-4 text-center">No results</div>


                    <div v-for="item in items" :key="item.id" class="p-1">
                        <NuxtLink :to="{ name: 'product-id', params: { id: item.id } }"
                            class="flex items-center justify-between w-full cursor-pointer hover:bg-gray-100">
                            <div class="flex items-center">
                                <img class="rounded-md" width="40" :src="item.image" />
                                <div class="truncate ml-2">{{ item.title }}</div>
                            </div>

                            <div class="truncate ml-2">{{ item.description }}</div>
                        </NuxtLink>
                    </div>


                    <div ref="sentinel" class="h-1"></div>


                    <div v-if="loading && items.length > 0" class="py-2 text-center">Loading more…</div>
                </div>
            </div>


            <NuxtLink to="/shoppingcart" class="flex items-center">
                <button class="relative md:block hidden" @mouseenter="isCartHover = true"
                    @mouseleave="isCartHover = false">
                    <span
                        class="absolute flex items-center justify-center -right-[3px] top-0 bg-[#FF4646] h-[17px] min-w-[17px] text-xs text-white px-0.5 rounded-full">
                        <!-- {{ userStore.cart.length }} -->
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
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useAuthStore } from '~/stores/modules/authStore'
import { useProductSearch } from '~/app/composables/search/useProductSearch'
// category related 
// import { useCategoryStore } from '~/stores/modules/categoryStore';
// const categoryStore = useCategoryStore()
// onMounted( async ()=> {
//     console.info("🚀 [Index] Fetching initial Categories")
//     await categoryStore.fetchCategories()
//     console.info("✅ [Index] Initial load complete")
// })
// categoy related end here 
const userStore = useAuthStore()
const searchWrapper = ref(null)
const dropdown = ref(null)
const sentinel = ref(null)
const isOpen = ref(false)
const isCartHover = ref(false)
const dropdownMaxHeight = ref(300)


const { query, items, loading, search, loadMore, hasNext, enableFuzzy, fuzzyFields } = useProductSearch({
    pageSize: 12,
    debounceMs: 350,
    autoFetch: false,
    autoStartObserver: false,
    enableFuzzy: true,
    fuzzyFields: ['title', 'description']
})


watch(query, (val) => search(val))


function onClickOutside(e) {
    if (searchWrapper.value && !searchWrapper.value.contains(e.target)) {
        isOpen.value = false
    }
}

function initObserver() {
    if (!sentinel.value) return
    observer = new IntersectionObserver(async ([entry]) => {
        if (entry.isIntersecting && hasNext.value && !loading.value) {
            await loadMore()
        }
    }, { threshold: 0.1 })
    observer.observe(sentinel.value)
}


async function autoFillDropdown() {
    if (!dropdown.value) return
    const maxLoops = 50
    let loops = 0
    while (hasNext.value && dropdown.value.scrollHeight <= dropdown.value.clientHeight && loops < maxLoops) {
        await loadMore()
        await nextTick()
        loops++
    }
}

function calculateDropdownHeight() {
    if (!dropdown.value) return
    const viewportHeight = window.innerHeight
    const dropdownTop = dropdown.value.getBoundingClientRect().top
    const maxHeight = viewportHeight - dropdownTop - 20
    dropdownMaxHeight.value = Math.min(maxHeight, 400)
}


function onScroll() {
    if (!dropdown.value || loading.value || !hasNext.value) return
    const { scrollTop, clientHeight, scrollHeight } = dropdown.value
    if (scrollTop + clientHeight >= scrollHeight - 10) {
        loadMore()
    }
}

onMounted(() => {
    document.addEventListener('click', onClickOutside)
    window.addEventListener('resize', calculateDropdownHeight)

    nextTick(async () => {
        calculateDropdownHeight()
        initObserver()
        await autoFillDropdown()
    })
})

onBeforeUnmount(() => {
    document.removeEventListener('click', onClickOutside)
    window.removeEventListener('resize', calculateDropdownHeight)
    if (observer) observer.disconnect()
})
</script>


<!-- <template>
    <div>
<h1>Header File</h1>
    </div>
</template>

<script setup>

</script>

<style lang="scss" scoped></style> -->