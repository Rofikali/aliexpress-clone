<!-- <template>
  <div class="product_images-gallery">
    <div class="main-image">
      <img :src="activeImage" alt="product_images Image" />
    </div>
    <div class="thumbnails">
      <product_imagesThumbnail
        v-for="(img, idx) in images"
        :key="idx"
        :src="img"
        :active="img === activeImage"
        @click="activeImage = img"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue"
import product_imagesThumbnail from "./product_imagesThumbnail.vue"

const props = defineProps({
  images: { type: Array, default: () => [] }
})

const activeImage = ref(props.images[0] || "")

watch(
  () => props.images,
  (newVal) => {
    if (newVal?.length) activeImage.value = newVal[0]
  }
)
</script> -->


<template>
    <div>
        <div v-if="product_images">
            <NuxtImg v-if="currentImage" class="rounded-lg object-contain" :src="currentImage"
                :alt="product_images.value?.title || 'product_images Image'" loading="lazy" />
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
    product_images: {
        type: Object,
        required: false,
        default: () => null
    }
})

// console.log('product_images value title', product_images.value.title);

const { product_images } = toRefs(props)
const userStore = useAuthStore()

const currentImage = ref(null)
const images = ref([])

watchEffect(() => {
    if (product_images.value) {
        // set default image
        currentImage.value = product_images.value.image

        // combine main image + gallery images from API
        images.value = [
            product_images.value.image,
            ...(product_images.value.images?.map(img => img.image) || [])
        ]

        // userStore.isLoading = false
        userStore.loading = false
    }
})
</script>