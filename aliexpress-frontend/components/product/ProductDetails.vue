<template>
    <div>
        <div v-if="product" class="md:flex gap-4 justify-between mx-auto w-full">
            <div class="md:w-[40%]">
                <ProductCard :product="product" />
            </div>
            <!-- Product Details -->
            <div class="md:w-[60%] bg-white p-3 rounded-lg">
                <div v-if="product">
                    <p class="mb-2 font-semibold">{{ product?.title }}</p>
                    <p class="font-light text-[12px] mb-2">{{ product?.description }}</p>
                </div>

                <!-- Stars -->
                <div class="flex items-center justify-start my-2">
                    <Icon v-for="i in 5" :key="i" name="ic:baseline-star" color="#FF5353" />
                    <span class="text-[13px] font-light ml-2">5 • 213 Reviews • 1,000+ orders</span>
                </div>

                <!-- Price -->
                <div class="flex items-center justify-start gap-2 my-2">
                    <div class="text-xl font-bold">$ {{ priceComputed }}</div>
                    <span class="bg-[#F5F5F5] border text-[#C08562] text-[9px] font-semibold px-1.5 rounded-sm">70%
                        off</span>
                </div>

                <!-- Shipping Info -->
                <p class="text-[#009A66] text-xs font-semibold pt-1">
                    Free 11-day delivery over ￡8.28
                </p>
                <p class="text-[#009A66] text-xs font-semibold pt-1">
                    Free Shipping
                </p>

                <!-- Add to Cart -->
                <div class="py-2" />
                <button @click="addToCart" :disabled="isInCart"
                    class="px-6 py-2 rounded-lg text-white text-lg font-semibold bg-gradient-to-r from-[#FF851A] to-[#FFAC2C]">
                    <span v-if="isInCart">Is Added</span>
                    <span v-else>Add to Cart</span>
                </button>
            </div>
        </div>
        <div v-else class="loading">Loading Products .......</div>
    </div>
</template>
<style scoped>
.main-image {
    width: 100%;
    max-width: 500px;
}

.thumbnail {
    width: 80px;
    height: 80px;
    object-fit: cover;
    cursor: pointer;
}
</style>

<script setup>
import { ref, watchEffect, computed } from 'vue'
// import { useUserStore } from '~/stores/user'
import { useAuthStore } from '~/stores/modules/authStore'

const props = defineProps({
    product: {
        type: Object,
        required: false, // true
        default: () => null
    }
})

const { product } = toRefs(props)

const userStore = useAuthStore()

// const isInCart = computed(() =>
//     userStore.cart.some(prod => prod.id === product.value?.id)
// )

const priceComputed = computed(() => {
    return product.value?.price ? (product.value.price / 100).toFixed(2) : '0.00'
})

const addToCart = () => {
    if (!isInCart.value) {
        userStore.cart.push(product.value)
    }
}
</script>
