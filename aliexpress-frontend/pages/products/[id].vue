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
<!--  above code working 100% fine -->


<!-- 
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


        <div v-if="variants.length" class="variants">
          <h4>Select Variant</h4>
          <div class="variant-list">
            <button
              v-for="v in variants"
              :key="v.id"
              @click="selectVariant(v)"
              :class="{ active: selectedVariant?.id === v.id }"
            >
              {{ v.sku }} — {{ v.price | currency }}
            </button>
          </div>
        </div>


        <div v-if="selectedVariant && attributes.length" class="attributes">
          <h4>Attributes</h4>
          <ul>
            <li v-for="a in attributes" :key="a.id">
              {{ a.name }}:
              <span v-for="val in a.values" :key="val.id">{{ val.value }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <ProductRelated :related="relatedProducts" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from "vue"
import { useRoute } from "vue-router"
import { storeToRefs } from "pinia"


import { useProductStore } from "~/stores/modules/product/productStore"
import { useVariantStore } from "~/stores/modules/product/variantStore"
import { useAttributeStore } from "~/stores/modules/product/attributeStore"



const route = useRoute()
const productId = route.params.id


const productStore = useProductStore()
const variantStore = useVariantStore()
const attributeStore = useAttributeStore()

const { product, productLoading, productError } = storeToRefs(productStore)
const { variants, fetchVariants, selectedVariant, setSelectedVariant } =
  variantStore
const { attributes, fetchAttributes } = attributeStore

const loading = ref(false)
const error = ref(null)
const relatedProducts = ref([])

async function loadProductAndVariants() {
  loading.value = true
  error.value = null

  try {
    // 1️⃣ Fetch Product
    const res = await productStore.fetchProductById(productId)
    if (!res.success) {
      error.value = res
      return
    }


    await fetchVariants(productId)
    if (variants.length) {
      selectVariant(variants[0]) // Select first variant by default
    }

    if (product.value?.category?.id) {
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
}

function selectVariant(variant) {
  setSelectedVariant(variant)
  if (variant?.id) {
    fetchAttributes(productId, variant.id)
  }
}

onMounted(() => {
  loadProductAndVariants()
})
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

.variants button.active {
  font-weight: bold;
  border: 2px solid #333;
}
</style> -->
