<template>
  <div class="product-detail-page">

    <div v-if="loading" class="loader">Loading product...</div>
    <div v-else-if="error" class="error">{{ error.message }}</div>

    <div v-else-if="product" class="product-layout">

      <div class="gallery">
        <LazyProductsDetailProductGallery :product_images="product" />
      </div>

      <div class="main-info">
        <ProductInfo :product="product" />
        <ProductActions
          :product="product"
          @add-to-cart="addToCart"
          @wishlist="addToWishlist"
        />
        <ProductMeta :product="product" />

        <!-- ✅ VariantSelector Component -->
        <LazyProductsDetailVariantSelector
          :product-id="id"
          @select="handleVariantSelect"
        />
      </div>
    </div>

    <ProductTabs>
      <template #description>
        <p v-html="product?.description"></p>
        <ProductSpecs :specs="product?.specs" />
      </template>

      <template #reviews>
        <ProductReviewList :productId="id" />
      </template>
    </ProductTabs>

    <ProductRelated :related="relatedProducts" />
  </div>
</template>

<script setup>
import { useRoute } from "vue-router"
import { onMounted, ref } from "vue"
import { useProductStore } from "~/stores/modules/product/productStore"
import { getProducts } from "~/services/api/products/product"

// Components
import ProductInfo from "~/components/products/detail/ProductInfo.vue"
import ProductActions from "~/components/products/detail/ProductActions.vue"
import ProductMeta from "~/components/products/detail/ProductMeta.vue"
import ProductTabs from "~/components/products/detail/ProductTabs.vue"
import ProductSpecs from "~/components/products/detail/ProductSpecs.vue"
import ProductReviewList from "~/components/products/detail/ProductReviewList.vue"
import ProductRelated from "~/components/products/detail/ProductRelated.vue"
// import VariantSelector from "~/components/products/detail/VariantSelector.vue"

const route = useRoute()
const id = route.params.id

const productStore = useProductStore()
const product = ref(null)
const relatedProducts = ref([])
const loading = ref(false)
const error = ref(null)

// ✅ Load product and related products
onMounted(async () => {
  loading.value = true
  try {
    const res = await productStore.fetchProductById(id)
    if (res.success) {
      product.value = res.data
    } else {
      error.value = res
    }

    // Related products
    if (product.value?.category) {
      const relatedRes = await getProducts({
        category: product.value.category,
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

// ✅ Handle variant selection emitted from VariantSelector
function handleVariantSelect(variant) {
  console.log("Selected variant:", variant)
  // Optional: do something with the selected variant in parent
}

// Cart & Wishlist
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
