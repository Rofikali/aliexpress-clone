<template>
    <div id="ItemPage" class="mt-4 max-w-[1200px] mx-auto px-2">
        <ProductDetails :product="product" />
    </div>
</template>

<script setup>
definePageMeta({ layout: 'default' })

import axios from '~/plugins/core/axios'
const $axios = axios().provide.axios

const route = useRoute()
let product = ref(null)

onBeforeMount(async () => {
    try {
        const response = await $axios.get(`/products/${route.params.id}/`) // check plural!
        product.value = response.data.product
        console.log('Product:', product.value)
    } catch (err) {
        console.error('Error fetching product:', err.response?.status, err.response?.data)
    }
})
</script>



<!-- <script setup>
definePageMeta(
    { layout: 'default' }
)

import axios from '~/plugins/axios';

const $axios = axios().provide.axios

const route = useRoute()
console.log('what is inside params-id ', route.params);
console.log('what is inside params-id ', route.params.id);

let product = ref(null)

onBeforeMount(async () => {
    product.value = await $axios.get(`/product/${route.params.id}/`)
    product = product.value.data.product
    console.log('what is inside produt ', product);
    console.log('what is inside produt ', product.value);
})

</script> -->
