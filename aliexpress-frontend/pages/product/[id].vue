<template>
    <div id="ItemPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <ProductDetails :product="product" />
    </div>
</template>

<script setup>
definePageMeta(
    { layout: 'default' }
)

import axios from '~/plugins/axios';

const $axios = axios().provide.axios

const route = useRoute()

let product = ref(null)

onBeforeMount(async () => {
    product.value = await $axios.get(`api/product/${route.params.id}/`)
    product = product.value.data.product
})

</script>
