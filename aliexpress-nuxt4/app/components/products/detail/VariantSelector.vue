<!-- 

components/products/detail/VariantSelector.vue
<template>
  <div class="variants">
    Loading state
    <div v-if="variantLoading">Loading variants...</div>

    Error state
    <div v-else-if="variantError" class="error">
      {{ variantError.message || "Failed to load variants" }}
    </div>

    Variants list
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


    No variants
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

local fetching state for single variant
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

Handle selection: fetch full variant detail
async function handleSelect(variant) {
  if (!props.productId || !variant?.id) return

  avoid duplicate request
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
  border: 1px solid #afaeae;
  background: #070707;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.variant-list button:hover {
  background: #030303;
}
.variant-list button.active {
  font-weight: bold;
  border: 2px solid #4af7a1;
  background: #706464;
}
.variant-list button.loading {
  opacity: 0.6;
  cursor: wait;
}
.error {
  color: red;
}
</style> -->

<template>
  <div class="variant-selector">
    <div v-if="variantLoading" class="loader">Loading variants...</div>
    <div v-else-if="variantError" class="error">{{ variantError.message || variantError }}</div>

    <div v-else-if="!attributeGroups.length" class="no-variants">
      <p>No variants or attributes available</p>
    </div>

    <div v-else>
      <div class="selected-summary" v-if="selectedVariantLocal">
        <div class="price">
          {{ formatPrice(selectedVariantLocal.price, selectedVariantLocal.currency || productCurrency) }}
        </div>
        <div class="sku-stock">
          <span class="sku">SKU: {{ selectedVariantLocal.sku }}</span>
          <span :class="{'out': !selectedVariantLocal.stock}"> • {{ selectedVariantLocal.stock ? 'In Stock' : 'Out of Stock' }}</span>
        </div>
      </div>

      <div class="attributes-grid">
        <div
          v-for="group in attributeGroups"
          :key="group.name"
          class="attribute-group"
        >
          <div class="group-title">{{ group.name }}</div>

          <div class="group-values">
            <button
              v-for="val in group.values"
              :key="val.value"
              :class="[
                'val-chip',
                { active: isSelected(group.name, val.value) },
                { disabled: !isAvailable(group.name, val.value) }
              ]"
              :disabled="!isAvailable(group.name, val.value) || isSelecting"
              @click="onSelectValue(group.name, val.value)"
              :title="val.value"
            >
              <span v-if="isColorGroup(group.name)" class="swatch" :style="{ background: val.value }"></span>
              <span class="val-label">{{ val.value }}</span>
            </button>
          </div>
        </div>
      </div>

      <div class="actions">
        <button class="add-to-cart" :disabled="!selectedVariantLocal || !selectedVariantLocal.stock" @click="addToCart">
          🛒 Add to Cart
        </button>
        <button class="buy-now" :disabled="!selectedVariantLocal || !selectedVariantLocal.stock" @click="buyNow">
          Buy Now
        </button>
      </div>

      <div v-if="availabilityWarning" class="warning">{{ availabilityWarning }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useVariantStore } from '~/stores/modules/product/variantStore'
import { useAttributeStore } from '~/stores/modules/product/attributeStore'
import { useProductStore } from '~/stores/modules/product/productStore'

// props
const props = defineProps({
  productId: { type: String, required: true }
})

// emits
const emit = defineEmits(['select', 'update-image', 'add-to-cart', 'buy-now'])

// stores
const variantStore = useVariantStore()
const attributeStore = useAttributeStore()
const productStore = useProductStore()

const { variants, selectedVariant, variantLoading, variantError, fetchVariants, fetchVariantById, setSelectedVariant } = variantStore
const { attributes, attributeLoading, attributeError, fetchAttributes } = attributeStore
const { product } = productStore

// local state
const isSelecting = ref(false)
const selectedAttrs = ref({}) // { Color: 'Red', Size: 'M' }
const selectedVariantLocal = ref(null)
const availabilityWarning = ref(null)

// product currency (fallback)
const productCurrency = computed(() => product?.value?.currency || 'USD')

// derive attributeGroups from variants (fallback) or attribute API
const attributeGroups = computed(() => {
  // prefer deriving from variants because that shows all possible combinations
  if (variants?.value?.length) {
    const groups = {}
    for (const v of variants.value) {
      const attrs = v.attributes || [] // expect array [{name, value}]
      for (const a of attrs) {
        if (!groups[a.name]) groups[a.name] = new Set()
        groups[a.name].add(a.value)
      }
    }
    return Object.keys(groups).map(name => ({
      name,
      values: Array.from(groups[name]).map(v => ({ value: v }))
    }))
  }

  // fallback: use attributeStore data (per-variant attributes)
  if (attributes?.value?.length) {
    return attributes.value.map(a => ({
      name: a.name,
      values: (a.values || []).map(v => ({ value: v.value }))
    }))
  }

  return []
})

// helper: determine color-like group (name heuristics)
function isColorGroup(name) {
  if (!name) return false
  const n = name.toLowerCase()
  return ['color', 'colour', 'shade'].includes(n)
}

// find matching variants by attributes map
function findMatchingVariants(attrsMap) {
  if (!variants?.value?.length) return []
  return variants.value.filter(v => {
    const av = v.attributes || []
    // build variant attribute map
    const vm = {}
    for (const a of av) vm[a.name] = a.value
    // every selected attr must match
    for (const k of Object.keys(attrsMap)) {
      if (attrsMap[k] == null) continue
      if (vm[k] !== attrsMap[k]) return false
    }
    return true
  })
}

// compute whether an option is available given current partial selection
function isAvailable(groupName, value) {
  // simulate selection for groupName=value while keeping other selectedAttrs
  const trial = { ...selectedAttrs.value, [groupName]: value }
  const matches = findMatchingVariants(trial)
  return matches.length > 0
}

// isSelected
function isSelected(groupName, value) {
  return selectedAttrs.value[groupName] === value
}

// when user clicks a value
async function onSelectValue(groupName, value) {
  // toggle if already selected
  if (selectedAttrs.value[groupName] === value) {
    // deselect
    selectedAttrs.value = { ...selectedAttrs.value, [groupName]: null }
  } else {
    selectedAttrs.value = { ...selectedAttrs.value, [groupName]: value }
  }

  // find matching variants
  const matches = findMatchingVariants(selectedAttrs.value)

  if (matches.length === 1) {
    // unique variant found -> select it
    await selectVariantById(matches[0].id)
  } else if (matches.length > 1) {
    // partial selection; pick first match as preview (do NOT finalize)
    // set local selectedVariant to show price/sku preview but do not emit final select yet
    selectedVariantLocal.value = matches[0]
    // also emit update-image to help parent show preview image
    if (matches[0].image) emit('update-image', matches[0].image)
    availabilityWarning.value = null
  } else {
    // no match -> show warning
    selectedVariantLocal.value = null
    availabilityWarning.value = 'Selected combination is not available.'
  }
}

// select variant by id: fetch full variant detail, update store and emit
async function selectVariantById(variantId) {
  if (!props.productId || !variantId) return
  isSelecting.value = true
  availabilityWarning.value = null
  try {
    const res = await fetchVariantById(props.productId, variantId)
    if (res && res.success) {
      selectedVariantLocal.value = res.data
      // set global selected variant in store
      setSelectedVariant(res.data)
      // emit full variant to parent
      emit('select', res.data)
      // if variant has image, update gallery in parent
      if (res.data.image) emit('update-image', res.data.image)
    } else {
      // fallback: find in local variants
      const local = variants.value.find(v => v.id === variantId)
      if (local) {
        selectedVariantLocal.value = local
        setSelectedVariant(local)
        emit('select', local)
        if (local.image) emit('update-image', local.image)
      }
    }
  } catch (err) {
    console.error('selectVariantById error', err)
  } finally {
    isSelecting.value = false
  }
}

// initial load: fetch variants and preselect best option
onMounted(async () => {
  if (!props.productId) return
  await fetchVariants(props.productId)
  // default select first variant if exists
  if (variants.value?.length) {
    // auto-populate selectedAttrs from selectedVariant in store or first variant
    const base = selectedVariant.value || variants.value[0]
    if (base && base.attributes) {
      const map = {}
      for (const a of base.attributes) map[a.name] = a.value
      selectedAttrs.value = map
      // fetch full details of base
      await selectVariantById(base.id)
      // fetch attributes for the selected variant (detail endpoint)
      await fetchAttributes(props.productId, base.id)
    }
  }
})

// watch when variants change (product switch)
watch(() => variants.value, (nv) => {
  // reset selections when variants update
  if (!nv || nv.length === 0) {
    selectedAttrs.value = {}
    selectedVariantLocal.value = null
  }
})

// actions for Add to Cart and Buy Now
function addToCart() {
  if (!selectedVariantLocal.value) return
  emit('add-to-cart', selectedVariantLocal.value)
}
function buyNow() {
  if (!selectedVariantLocal.value) return
  emit('buy-now', selectedVariantLocal.value)
}

// helper: nice price formatting
function formatPrice(price, currency = 'USD') {
  if (price == null) return ''
  try {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency }).format(price)
  } catch (e) {
    return `${currency} ${price}`
  }
}
</script>

<style scoped>
.variant-selector {
  background: #0b0b0b;
  color: #e6e6e6;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 6px 18px rgba(0,0,0,0.5);
}

/* summary */
.selected-summary {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}
.price {
  font-size: 1.25rem;
  font-weight: 700;
  color: #fff;
}
.sku-stock { color: #bdbdbd; }
.sku-stock .out { color: #ff6b6b; }

/* attribute groups */
.attributes-grid { display: grid; gap: 0.75rem; }
.attribute-group { display: flex; flex-direction: column; gap: 0.5rem; }
.group-title { font-weight: 600; color: #cfcfcf; text-transform: capitalize; }

/* values */
.group-values { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.val-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.6rem;
  border-radius: 8px;
  background: #161616;
  color: #e6e6e6;
  border: 1px solid #2a2a2a;
  cursor: pointer;
  transition: transform .08s ease;
}
.val-chip:hover { transform: translateY(-1px); }
.val-chip.disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.val-chip.active {
  border: 2px solid #4af7a1;
  background: linear-gradient(180deg, #222 0%, #141414 100%);
  box-shadow: 0 6px 18px rgba(74,247,161,0.08);
}

/* swatch for color-like values */
.swatch {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 1px solid rgba(0,0,0,0.4);
  display: inline-block;
}

/* action buttons */
.actions { margin-top: 1rem; display:flex; gap: 0.5rem; }
.add-to-cart, .buy-now {
  padding: 0.6rem 1rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}
.add-to-cart {
  background: #0f0f0f;
  color: #fff;
  border: 1px solid #2b2b2b;
}
.buy-now {
  background: #4af7a1;
  color: #08120b;
}

/* utility */
.loader { color: #cfcfcf; }
.error { color: #ff6b6b; }
.warning { color: #ffd166; margin-top: 0.5rem; }
.no-variants { color: #bdbdbd; }
</style>
