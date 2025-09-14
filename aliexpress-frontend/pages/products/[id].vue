<!-- <template>
    <div id="ItemPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <ProductDetails :product="product" />
    </div>
</template>

<script setup>
definePageMeta({ layout: 'default' })

import axios from '~/plugins/axios'
const $api = axios().provide.axios
const { $api } = useNuxtApp()

const route = useRoute()
let product = ref(null)

onBeforeMount(async () => {
    try {
        const response = await $api.get(`/products/${route.params.id}/`) // check plural!
        product.value = response.data.product
        console.log('Product:', product.value)
    } catch (err) {
        console.error('Error fetching product:', err.response?.status, err.response?.data)
    }
})
</script>
 -->

 <script setup>
import { useProductStore } from "~/stores/modules/productStore"

const store = useProductStore()
const route = useRoute()

// Fetch product when entering detail page
onMounted(() => {
  store.fetchProductById(route.params.id)
})
</script>

<template>
  <div>
    <div v-if="store.productLoading">Loading product...</div>
    <div v-else-if="store.productError">❌ {{ store.productError.message }}</div>
    <div v-else-if="store.product">
      <h1>{{ store.product.name }}</h1>
      <p>{{ store.product.description }}</p>
    </div>
  </div>
</template>
