<template>
    <div>
        <div v-if="product">
            <NuxtImg v-if="currentImage" class="rounded-lg object-contain" :src="currentImage"
                :alt="product.value?.title || 'Product Image'" loading="lazy" />
            <div v-if="images.length" class="flex items-center justify-center mt-2 gap-2">
                <NuxtImg v-for="(image, idx) in images" :key="idx" @mouseover="currentImage = image"
                    @click="currentImage = image" width="70"
                    class="rounded-md object-cover border-[3px] cursor-pointer transition"
                    :class="currentImage === image ? 'border-[#FF5353]' : 'border-transparent'" :src="image"
                    :alt="`Thumbnail ${idx + 1}`" loading="lazy" />
            </div>
        </div>
        <div v-else class="loading">
            Loading Images ...........
        </div>
    </div>
</template>

<script setup>
import { ref, watchEffect, toRefs } from 'vue'
import { useAuthStore } from '~/stores/modules/authStore'

const props = defineProps({
    product: {
        type: Object,
        required: false,
        default: () => null
    }
})

// console.log('product value title', product.value.title);

const { product } = toRefs(props)
const userStore = useAuthStore()

const currentImage = ref(null)
const images = ref([])

watchEffect(() => {
    if (product.value) {
        // set default image
        currentImage.value = product.value.image

        // combine main image + gallery images from API
        images.value = [
            product.value.image,
            ...(product.value.images?.map(img => img.image) || [])
        ]

        userStore.isLoading = false
    }
})
</script>


<!-- <script setup>
import { ref, watchEffect, computed } from 'vue'
import { useUserStore } from '~/stores/user'

const props = defineProps({
    product: {
        type: Object,
        required: false,
        default: () => null
    }
})

const { product } = toRefs(props)
console.log('product Card Page', product);
const userStore = useUserStore()
const currentImage = ref(null)
const images = ref([])

watchEffect(() => {
    if (product.value?.image) {
        currentImage.value = product.value.image
        images.value = [
            product.value.image,
            '/visa.png',
            '/github-logo.png',
            '/google-logo.png',
            '/paypal.png',
            '/mastercard.png'
        ]
        userStore.isLoading = false
    }
})

</script>

<style scoped></style> -->