<!-- components/products/detail/VariantSelector.vue -->

<!-- <template>
  <div v-if="variantLoading" class="variants">
    Loading variants...
  </div>

  <div v-else-if="variantError" class="variants error">
    {{ variantError.message || "Failed to load variants" }}
  </div>

  <div v-else-if="variants?.length" class="variants">
    <h4 class="variants-title">Select Variant</h4>
    <div class="variant-list">
      <button
        v-for="v in variants"
        :key="v.id"
        @click="handleSelect(v)"
        :class="{ active: selectedVariant?.id === v.id }"
      >
        {{ v.sku }} — {{ formatPrice(v.price, v.currency) }}
      </button>
    </div>
  </div>

  <div v-else class="variants">
    No variants available
  </div>
</template>

<script setup>
import { onMounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useVariantStore } from "~/stores/modules/product/variantStore"

const props = defineProps({
  productId: { type: String, required: true }
})

const emit = defineEmits(["select"])

const variantStore = useVariantStore()
const { variants, selectedVariant, variantLoading, variantError } = storeToRefs(variantStore)


onMounted(async () => {
  if (props.productId) {
    await variantStore.fetchVariants(props.productId)
  }
})


watch(() => props.productId, async (newId) => {
  if (newId) {
    await variantStore.fetchVariants(newId)
  }
})


function handleSelect(variant) {
  variantStore.setSelectedVariant(variant)
  emit("select", variant)  // notify parent component
}


function formatPrice(price, currency = "USD") {
  if (typeof price !== "number") return price
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
  }).format(price)
}
</script>

<style scoped>
.variants {
  margin-top: 1rem;
}
.variants-title {
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.variant-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.variant-list button {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.variant-list button:hover {
  background: #f5f5f5;
}
.variant-list button.active {
  font-weight: bold;
  border: 2px solid #333;
  background: #fafafa;
}
.error {
  color: red;
}
</style> -->


<!-- components/products/detail/VariantSelector.vue -->
<template>
  <div class="variants">
    <!-- Loading state -->
    <div v-if="variantLoading">Loading variants...</div>

    <!-- Error state -->
    <div v-else-if="variantError" class="error">
      {{ variantError.message || "Failed to load variants" }}
    </div>

    <!-- Variants list -->
    <div v-else-if="variants?.length">
      <h4 class="variants-title">Select Variant</h4>
      <div class="variant-list">
        <button
          v-for="v in variants"
          :key="v.id"
          @click="handleSelect(v)"
          :disabled="isFetching && v.id === fetchingVariantId"
          :class="{
            active: selectedVariant?.id === v.id,
            loading: isFetching && v.id === fetchingVariantId
          }"
        >
          <span v-if="isFetching && v.id === fetchingVariantId">
            Fetching details...
          </span>
          <span v-else>
            {{ v.sku }} — {{ formatPrice(v.price, v.currency) }}
          </span>
        </button>
      </div>
    </div>

    <LazyProductsDetailVariantAttributes v-if="selectedVariant?.id"
      :productId="productId"
      :variantId="selectedVariant.id"
    />


    <!-- No variants -->
    <div v-else>No variants available</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useVariantStore } from "~/stores/modules/product/variantStore"
import { LazyProductsDetailVariantAttributes } from "#components"

const props = defineProps({
  productId: { type: String, required: true }
})

const emit = defineEmits(["select"])

const variantStore = useVariantStore()
const { variants, selectedVariant, variantLoading, variantError } = storeToRefs(variantStore)

// local fetching state for single variant
const isFetching = ref(false)
const fetchingVariantId = ref(null)

onMounted(async () => {
  if (props.productId) {
    await variantStore.fetchVariants(props.productId)
  }
})

watch(
  () => props.productId,
  async (newId) => {
    if (newId) {
      await variantStore.fetchVariants(newId)
    }
  }
)

// Handle selection: fetch full variant detail
async function handleSelect(variant) {
  if (!props.productId || !variant?.id) return

  // avoid duplicate request
  if (selectedVariant.value?.id === variant.id) {
    emit("select", selectedVariant.value)
    return
  }

  isFetching.value = true
  fetchingVariantId.value = variant.id

  try {
    const fullVariant = await variantStore.fetchVariantById(
      props.productId,
      variant.id
    )
    if (fullVariant?.success) {
      emit("select", fullVariant.data)
    } else {
      console.warn("Failed to fetch variant details", fullVariant)
    }
  } catch (err) {
    console.error("Error fetching variant details", err)
  } finally {
    isFetching.value = false
    fetchingVariantId.value = null
  }
}

function formatPrice(price, currency = "USD") {
  if (typeof price !== "number") return price
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency
  }).format(price)
}
</script>

<style scoped>
.variants {
  margin-top: 1rem;
}
.variants-title {
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.variant-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.variant-list button {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  background: #fff;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.variant-list button:hover {
  background: #f5f5f5;
}
.variant-list button.active {
  font-weight: bold;
  border: 2px solid #333;
  background: #fafafa;
}
.variant-list button.loading {
  opacity: 0.6;
  cursor: wait;
}
.error {
  color: red;
}
</style>
