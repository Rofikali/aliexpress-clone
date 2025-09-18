<!-- 
<script setup>
import { useProductStore } from "~/stores/modules/productStore"

const store = useProductStore()
const route = useRoute()

onMounted(() => {
  store.fetchProductById(route.params.id)
})
</script>

<template>
  <div>
    <div v-if="store.productLoading">Loading product...</div>
    <div v-else-if="store.productError">❌ {{ store.productError.message }}</div>
    <div v-else-if="store.product">
       <lazy-product-details :product="store.product" />
    </div>
  </div>
</template> -->


<template>
  <div class="product-detail-page">
    <!-- 🔄 Loading / Error states -->
    <div v-if="loading" class="loader">Loading product...</div>
    <div v-else-if="error" class="error">{{ error.message }}</div>

    <!-- ✅ Product content -->
    <div v-else-if="product" class="product-layout">
      <!-- LEFT: Gallery -->
      <div class="gallery">
        <LazyProductsDetailProductGallery :product_images="product" />
      </div>

      <!-- RIGHT: Info + Actions -->
      <div class="main-info">
        <ProductInfo :product="product" />
        <ProductActions :product="product" @add-to-cart="addToCart" @wishlist="addToWishlist" />
        <ProductMeta :product="product" />
      </div>
    </div>

    <!-- 📑 Tabs: Description + Reviews -->
    <ProductTabs>
      <template #description>
        <p v-html="product?.description"></p>
        <ProductSpecs :specs="product?.specs" />
      </template>

      <template #reviews>
        <ProductReviewList :productId="id" />
      </template>
    </ProductTabs>

    <!-- 🔗 Related products -->
    <ProductRelated :related="relatedProducts" />
  </div>
</template>

<script setup>
import { useRoute } from "vue-router"
import { onMounted, ref } from "vue"

// 🛠 Store & Service
import { useProductStore } from "~/stores/modules/productStore"
import { getProducts } from "~/services/api/products"


import ProductInfo from "~/components/products/detail/ProductInfo.vue"
import ProductActions from "~/components/products/detail/ProductActions.vue"
import ProductMeta from "~/components/products/detail/ProductMeta.vue"
import ProductTabs from "~/components/products/detail/ProductTabs.vue"
import ProductSpecs from "~/components/products/detail/ProductSpecs.vue"
import ProductReviewList from "~/components/products/detail/ProductReviewList.vue"
import ProductRelated from "~/components/products/detail/ProductRelated.vue"


const route = useRoute()
const id = route.params.id

const productStore = useProductStore()
const product = ref(null)
const relatedProducts = ref([])

const loading = ref(false)
const error = ref(null)

onMounted(async () => {
  loading.value = true
  try {
    // 🟢 Load product details
    const res = await productStore.fetchProductById(id)
    if (res.success) {
      product.value = res.data
    } else {
      error.value = res
    }

    // 🔗 Load related products (example: same category)
    if (product.value?.category?.id) {
      console.log(
        'related products category ', product.value.category.id
      );
      const relatedRes = await getProducts({
        category: product.value.category.id,
        page_size: 4,
      })
      if (relatedRes.success) {
        relatedProducts.value = relatedRes.data
      }
    }
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
})

// 🛒 Actions
function addToCart(product) {
  console.info("[ProductPage] Add to cart:", product)
}
function addToWishlist(product) {
  console.info("[ProductPage] Add to wishlist:", product)
}
</script>

<style scoped>
.product-detail-page {
  max-width: 1200px;
  margin: auto;
  padding: 2rem;
}

.product-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.loader {
  text-align: center;
  padding: 2rem;
}

.error {
  color: red;
  text-align: center;
}
</style>
