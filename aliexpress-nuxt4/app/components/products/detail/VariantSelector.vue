<!-- 
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

<!-- 
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

/**
 * Normalizers: backend and frontends sometimes use different keys.
 * These helpers make the rest of the logic key-agnostic.
 */
function attrName(a) {
  // possible shapes: { name }, { attribute_name }, { attribute: { name } }
  return a?.attribute_name ?? a?.name ?? a?.attribute?.name ?? ''
}
function attrValue(a) {
  // possible shapes: { value }, { val }, { attribute_value }
  return a?.value ?? a?.val ?? a?.attribute_value ?? ''
}
function attrValueId(a) {
  return a?.value_id ?? a?.id ?? ''
}

/**
 * Normalize variants into a form the component expects:
 * each variant.attributes will be [{ name, value, value_id }]
 */
const normalizedVariants = computed(() => {
  if (!variants?.value) return []
  return variants.value.map(v => {
    const attrs = (v.attributes || []).map(a => ({
      name: attrName(a),
      value: attrValue(a),
      value_id: attrValueId(a),
      raw: a
    }))
    return {
      ...v,
      attributes: attrs
    }
  })
})

// derive attributeGroups from normalizedVariants (preferred)
const attributeGroups = computed(() => {
  const vs = normalizedVariants.value
  if (!vs.length) {
    // fallback: use attributeStore data if provided
    if (attributes?.value?.length) {
      return attributes.value.map(a => ({
        name: a.name,
        values: (a.values || []).map(v => ({ value: v.value, id: v.id }))
      }))
    }
    return []
  }

  const groups = {}
  for (const v of vs) {
    for (const a of v.attributes) {
      if (!a.name) continue
      if (!groups[a.name]) groups[a.name] = new Map()
      // use value as display; also keep id
      groups[a.name].set(a.value, { value: a.value, id: a.value_id })
    }
  }

  return Object.keys(groups).map(name => ({
    name,
    values: Array.from(groups[name].values())
  }))
})

/**
 * findMatchingVariants: use normalizedVariants
 * attrsMap is { Color: 'Red', Size: 'M' } (by display value)
 */
function findMatchingVariants(attrsMap) {
  if (!normalizedVariants.value?.length) return []
  return normalizedVariants.value.filter(v => {
    const vm = {}
    for (const a of v.attributes) vm[a.name] = a.value
    for (const k of Object.keys(attrsMap)) {
      if (attrsMap[k] == null) continue
      if (vm[k] !== attrsMap[k]) return false
    }
    return true
  })
}

function isAvailable(groupName, value) {
  const trial = { ...selectedAttrs.value, [groupName]: value }
  const matches = findMatchingVariants(trial)
  return matches.length > 0
}

function isSelected(groupName, value) {
  return selectedAttrs.value[groupName] === value
}

async function onSelectValue(groupName, value) {
  // toggle selection
  if (selectedAttrs.value[groupName] === value) {
    selectedAttrs.value = { ...selectedAttrs.value, [groupName]: null }
  } else {
    selectedAttrs.value = { ...selectedAttrs.value, [groupName]: value }
  }

  const matches = findMatchingVariants(selectedAttrs.value)

  if (matches.length === 1) {
    await selectVariantById(matches[0].id)
  } else if (matches.length > 1) {
    selectedVariantLocal.value = matches[0]
    if (matches[0].image) emit('update-image', matches[0].image)
    availabilityWarning.value = null
  } else {
    selectedVariantLocal.value = null
    availabilityWarning.value = 'Selected combination is not available.'
  }
}

async function selectVariantById(variantId) {
  if (!props.productId || !variantId) return
  isSelecting.value = true
  availabilityWarning.value = null
  try {
    const res = await fetchVariantById(props.productId, variantId)
    if (res && res.success) {
      // normalize fetched variant as well (in case API uses different keys)
      const norm = {
        ...res.data,
        attributes: (res.data.attributes || []).map(a => ({
          name: attrName(a),
          value: attrValue(a),
          value_id: attrValueId(a),
          raw: a
        }))
      }
      selectedVariantLocal.value = norm
      setSelectedVariant(norm)
      emit('select', norm)
      if (norm.image) emit('update-image', norm.image)
    } else {
      // fallback: check local normalizedVariants
      const local = normalizedVariants.value.find(v => v.id === variantId)
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

// initial load
onMounted(async () => {
  if (!props.productId) return
  await fetchVariants(props.productId)

  if (normalizedVariants.value?.length) {
    const base = selectedVariant.value || normalizedVariants.value[0]
    if (base && base.attributes) {
      const map = {}
      for (const a of base.attributes) map[a.name] = a.value
      selectedAttrs.value = map
      await selectVariantById(base.id)
      await fetchAttributes(props.productId, base.id)
    }
  }
})

// watch variants update => reset
watch(() => variants.value, (nv) => {
  if (!nv || nv.length === 0) {
    selectedAttrs.value = {}
    selectedVariantLocal.value = null
  }
})

function addToCart() {
  if (!selectedVariantLocal.value) return
  emit('add-to-cart', selectedVariantLocal.value)
}
function buyNow() {
  if (!selectedVariantLocal.value) return
  emit('buy-now', selectedVariantLocal.value)
}

function formatPrice(price, currency = 'USD') {
  if (price == null) return ''
  try {
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency }).format(price)
  } catch (e) {
    return `${currency} ${price}`
  }
}
</script> -->

<!-- 
<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useVariantStore } from '~/stores/modules/product/variantStore'
// import { UCheckboxGroup, UCheckbox } from '@nuxt/ui'

interface AttributeValue {
  id: string
  value: string
}

interface AttributeGroup {
  id: string
  name: string
  values: AttributeValue[]
  isColor: boolean
}

// props
const props = defineProps({
  productId: { type: String, required: true }
})

// emits
const emit = defineEmits(['select', 'update-image'])

// store
const variantStore = useVariantStore()

// local state
const loading = ref(true)
const error = ref(null)
const selectedAttrs = ref<Record<string, string>>({})
const previewVariant = ref(null)
const availabilityWarning = ref(null)

// predefined color map (name → hex)
const COLOR_MAP: Record<string, string> = {
  red: '#ef4444',
  green: '#10b981',
  blue: '#3b82f6',
  black: '#111827',
  white: '#ffffff',
  yellow: '#facc15',
  purple: '#8b5cf6',
  pink: '#ec4899',
  gray: '#6b7280'
}

// helpers
function isColorGroup(name: string) {
  if (!name) return false
  return ['color', 'colour', 'shade'].some(x => name.toLowerCase().includes(x))
}

function findMatchingVariants(attrsMap: Record<string, string>) {
  return variantStore.variants.filter(v => {
    const av = v.attributes || []
    const variantMap: Record<string, string> = {}
    for (const a of av) {
      variantMap[a.attribute_id] = a.value_id
    }
    return Object.keys(attrsMap).every(k => !attrsMap[k] || variantMap[k] === attrsMap[k])
  })
}

function isDisabled(attributeId: string, valueId: string) {
  const trial = { ...selectedAttrs.value, [attributeId]: valueId }
  return findMatchingVariants(trial).length === 0
}

function onSelectValue(attributeId: string, valueId: string) {
  selectedAttrs.value[attributeId] = valueId
  const matches = findMatchingVariants(selectedAttrs.value)
  if (matches.length === 1) {
    previewVariant.value = matches[0]
    variantStore.setSelectedVariant(previewVariant.value)
    emit('select', previewVariant.value)
    emit('update-image', previewVariant.value.image)
    availabilityWarning.value = null
  } else if (matches.length > 1) {
    previewVariant.value = matches[0]
    emit('update-image', previewVariant.value.image)
    availabilityWarning.value = null
  } else {
    previewVariant.value = null
    availabilityWarning.value = 'Selected combination not available'
  }
}

// computed groups
const attributeGroups = computed<AttributeGroup[]>(() => {
  const aa = variantStore.available_attributes || {}
  return Object.keys(aa).map(id => {
    const group = aa[id]
    return {
      id,
      name: group.name,
      values: group.values || [],
      isColor: isColorGroup(group.name)
    }
  })
})

// load variants
async function load() {
  try {
    loading.value = true
    const res = await variantStore.fetchVariants(props.productId)
    if (res.success) {
      // preselect default
      const defaultVar = res.default_variant
      if (defaultVar) {
        const map: Record<string, string> = {}
        for (const a of defaultVar.attributes) {
          map[a.attribute_id] = a.value_id
        }
        selectedAttrs.value = map
        previewVariant.value = defaultVar
        emit('select', defaultVar)
        emit('update-image', defaultVar.image)
      }
    }
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

onMounted(() => load())

// watch store selectedVariant for external changes
watch(() => variantStore.selectedVariant, (nv) => {
  if (!nv) return
  const map: Record<string, string> = {}
  for (const a of nv.attributes) map[a.attribute_id] = a.value_id
  selectedAttrs.value = map
  previewVariant.value = nv
  emit('select', nv)
  emit('update-image', nv.image)
})
</script>

<template>
  <div class="variant-selector">
    <div v-if="loading">Loading options...</div>
    <div v-else-if="error" class="text-red-600">Failed to load variants</div>
    <div v-else>
      <div v-for="group in attributeGroups" :key="group.id" class="mb-4">
        <div class="font-semibold mb-2">{{ group.name }}</div>

        <!-- Color swatches using NuxtUI checkbox group -->
        <!-- <UCheckboxGroup v-if="group.isColor" v-model="selectedAttrs[group.id]">
          <UCheckbox
            v-for="val in group.values"
            :key="val.id"
            :value="val.id"
            :disabled="isDisabled(group.id, val.id)"
          >
            <span
              class="w-8 h-8 inline-block rounded-full border"
              :style="{ backgroundColor: COLOR_MAP[val.value.toLowerCase()] || val.value }"
            ></span>
          </UCheckbox>
        </UCheckboxGroup>
        <UCheckboxGroup v-if="group.isColor" v-model="selectedAttrs[group.id]">
          <UCheckbox
            v-for="val in group.values"
            :key="val.id"
            :value="val.id"
            :disabled="isDisabled(group.id, val.id)"
          >
            <span
              class="w-8 h-8 inline-block rounded-full border"
              :style="{ backgroundColor: COLOR_MAP[val.value.toLowerCase()] || val.value }"
            ></span>
          </UCheckbox>
        </UCheckboxGroup>


        <!-- regular options for other attributes
        <div v-else class="flex gap-2 flex-wrap">
          <button
            v-for="val in group.values"
            :key="val.id"
            class="px-3 py-1 rounded border"
            :class="{ 'bg-black text-white': selectedAttrs[group.id] === val.id, 'opacity-50 cursor-not-allowed': isDisabled(group.id, val.id) }"
            :disabled="isDisabled(group.id, val.id)"
            @click="onSelectValue(group.id, val.id)"
          >
            {{ val.value }}
          </button>
        </div>
      </div>

      <!-- Preview 
      <div v-if="previewVariant" class="mt-4 flex items-center gap-4 border-t pt-4">
        <img :src="previewVariant.image" class="w-24 h-24 object-cover rounded" />
        <div>
          <div class="font-bold">
            {{ previewVariant.currency }} {{ previewVariant.discount_price }}
            <span class="line-through text-gray-400 ml-2">{{ previewVariant.currency }} {{ previewVariant.price }}</span>
          </div>
          <div class="text-gray-500 mt-1">SKU: {{ previewVariant.sku }}</div>
          <div :class="previewVariant.stock > 0 ? 'text-green-600' : 'text-red-600'">
            {{ previewVariant.stock > 0 ? 'In Stock' : 'Out of Stock' }}
          </div>
        </div>
      </div>

      <div v-if="availabilityWarning" class="text-yellow-600 mt-2">{{ availabilityWarning }}</div>
    </div>
  </div>
</template>

<style scoped>
.variant-selector { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
</style>

 -->
<!-- ********************* WORKING FINE BELOW CODE ***************** -->
 <!-- <script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useVariantStore } from '~/stores/modules/product/variantStore'

// props
const props = defineProps({
  productId: { type: String, required: true }
})

// emits
const emit = defineEmits(['select', 'update-image'])

// store
const variantStore = useVariantStore()

// local UI state
const loading = ref(true)
const error = ref(null)

const selectedAttrs = ref({}) // { attribute_id: value_id }
const previewVariant = ref(null) // shown when partial selection
const availabilityWarning = ref(null)

// helpers to access store reactive values
const storeVariants = computed(() => variantStore.variants) // array
const storeAvailableAttributes = computed(() => variantStore.available_attributes) // object
const storeCombinationMap = computed(() => variantStore.combination_map) // object
const storeSelectedVariant = computed(() => variantStore.selectedVariant)

function isColorGroup(name, sampleValue) {
  if (!name && !sampleValue) return false
  const n = (name || '').toLowerCase()
  if (['color', 'colour', 'shade'].some(x => n.includes(x))) return true
  // value looks like hex color?
  const val = (sampleValue || '').toString().trim()
  return /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(val)
}

// Build a sorted key like "attrId:valId|attrId:valId"
function buildKeyFromMap(map) {
  return Object.keys(map)
    .filter(k => map[k] != null)
    .map(k => `${k}:${map[k]}`)
    .sort()
    .join('|')
}

// find variants that match a partial/full selection (selectedAttrs uses value_id)
function findMatchingVariants(attrsMap) {
  if (!storeVariants.value?.length) return []
  return storeVariants.value.filter(v => {
    const av = v.attributes || [] // each has attribute_id and value_id
    const variantMap = {}
    for (const a of av) {
      if (a.attribute_id) variantMap[a.attribute_id] = a.value_id
    }
    for (const k of Object.keys(attrsMap)) {
      // if user hasn't selected this attr, skip
      if (attrsMap[k] == null) continue
      if (variantMap[k] !== attrsMap[k]) return false
    }
    return true
  })
}

// determine if an option is available given current partial selection
function isAvailable(attributeId, valueId) {
  const trial = { ...selectedAttrs.value, [attributeId]: valueId }
  const matches = findMatchingVariants(trial)
  return matches.length > 0
}

// check disabled state for UI (same as !isAvailable)
function isDisabled(attributeId, valueId) {
  return !isAvailable(attributeId, valueId)
}

// when user clicks value
async function onSelectValue(attributeId, valueId) {
  // toggle selection
  if (selectedAttrs.value[attributeId] === valueId) {
    selectedAttrs.value = { ...selectedAttrs.value, [attributeId]: null }
  } else {
    selectedAttrs.value = { ...selectedAttrs.value, [attributeId]: valueId }
  }
  availabilityWarning.value = null

  const matches = findMatchingVariants(selectedAttrs.value)

  if (matches.length === 1) {
    // unique variant — finalize selection
    const variant = matches[0]
    // update store selected variant (do not call remote unless you want detail)
    variantStore.setSelectedVariant(variant)
    previewVariant.value = variant
    emit('select', variant)
    if (variant.image) emit('update-image', variant.image)
  } else if (matches.length > 1) {
    // multiple possible variants → preview the first match
    previewVariant.value = matches[0]
    if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
  } else {
    // no match
    previewVariant.value = null
    availabilityWarning.value = 'Selected combination is not available.'
  }
}

// load and initialize
async function load() {
  try {
    loading.value = true
    error.value = null
    const res = await variantStore.fetchVariants(props.productId)

    if (!res || res.success === false) {
      throw res || new Error('Failed to load variants')
    }

    // if backend returned default or store already set selectedVariant, use it to set selectedAttrs
    // prefer storeSelectedVariant if available
    const seeded = storeSelectedVariant.value || res.default_variant || null

    if (seeded && seeded.attributes) {
      const map = {}
      for (const a of seeded.attributes) {
        // backend attributes: { attribute_id, value_id, ... }
        if (a.attribute_id && a.value_id) map[a.attribute_id] = a.value_id
      }
      selectedAttrs.value = map
      // set preview or selectedVariant in component
      // use storeSelectedVariant if available (store already set it)
      if (storeSelectedVariant.value) {
        previewVariant.value = storeSelectedVariant.value
        if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
        emit('select', previewVariant.value)
      } else {
        // try to find matching variant in variants list
        const matches = findMatchingVariants(selectedAttrs.value)
        if (matches.length >= 1) {
          previewVariant.value = matches[0]
          variantStore.setSelectedVariant(previewVariant.value)
          if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
          emit('select', previewVariant.value)
        }
      }
    } else {
      // if no seeded default, auto-select best available (store did auto-select selectedVariant)
      if (storeSelectedVariant.value) {
        const sv = storeSelectedVariant.value
        // build selectedAttrs from storeSelectedVariant.attributes
        const map = {}
        for (const a of sv.attributes || []) {
          if (a.attribute_id && a.value_id) map[a.attribute_id] = a.value_id
        }
        selectedAttrs.value = map
        previewVariant.value = sv
        if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
        emit('select', previewVariant.value)
      }
    }
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  load()
})

// watch for external changes to storeSelectedVariant (if other parts set it)
watch(storeSelectedVariant, (nv) => {
  if (!nv) return
  // reflect in UI selections
  const map = {}
  for (const a of nv.attributes || []) {
    if (a.attribute_id && a.value_id) map[a.attribute_id] = a.value_id
  }
  selectedAttrs.value = map
  previewVariant.value = nv
  if (nv.image) emit('update-image', nv.image)
  emit('select', nv)
})

// computed attribute groups (keeps order of available_attributes keys)
const attributeGroups = computed(() => {
  const aa = storeAvailableAttributes.value || {}
  // convert to array of { id, name, values: [ { id, value } ] }
  return Object.keys(aa).map(id => {
    const group = aa[id]
    // pick sample value to detect colors
    const sample = (group.values && group.values[0] && group.values[0].value) || null
    return {
      id,
      name: group.name,
      values: group.values || [],
      isColor: isColorGroup(group.name, sample)
    }
  })
})

// helper: show label for value; for color swatches avoid long text inside swatch
function valueLabel(v) {
  return v?.value ?? v?.name ?? String(v)
}
</script>

<template>
  <div class="variant-selector-root">
    <div v-if="loading" class="loader">Loading options...</div>
    <div v-else-if="error" class="error">Failed to load variants</div>
    <div v-else>
      <div v-if="attributeGroups.length === 0" class="no-attrs">No variants or attributes available</div>

      <div v-else class="groups space-y-4">
        <div v-for="group in attributeGroups" :key="group.id" class="group">
          <div class="group-title">{{ group.name }}</div>

          <div v-if="group.isColor" class="swatches">
            <button
              v-for="val in group.values"
              :key="val.id"
              class="swatch-btn"
              :class="{ selected: selectedAttrs[group.id] === val.id, disabled: isDisabled(group.id, val.id) }"
              :disabled="isDisabled(group.id, val.id)"
              @click="onSelectValue(group.id, val.id)"
              :aria-pressed="selectedAttrs[group.id] === val.id"
              :title="valueLabel(val)"
            >
              <span
                class="swatch-circle"
                :style="{
                  background: ( /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(val.value) ? val.value : 'transparent' ),
                  border: ( /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(val.value) ? '1px solid rgba(0,0,0,0.15)' : '1px solid #ddd' )
                }"
              >
              </span>
              <span v-if="!(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(val.value))" class="swatch-label">{{ valueLabel(val) }}</span>
            </button>
          </div>

          <div v-else class="option-buttons">
            <button
              v-for="val in group.values"
              :key="val.id"
              class="opt-btn"
              :class="{ selected: selectedAttrs[group.id] === val.id, disabled: isDisabled(group.id, val.id) }"
              :disabled="isDisabled(group.id, val.id)"
              @click="onSelectValue(group.id, val.id)"
            >
              {{ valueLabel(val) }}
            </button>
          </div>
        </div>

        <!-- preview / selected summary
        <div v-if="previewVariant" class="preview border p-3 rounded mt-2">
          <div class="preview-grid" style="display:flex; gap:1rem; align-items:center;">
            <img :src="previewVariant.image" alt="variant image" style="width:96px; height:96px; object-fit:cover; border-radius:6px;" />
            <div>
              <div style="font-weight:700;">
                {{ previewVariant.currency }} {{ previewVariant.discount_price }}
                <span style="text-decoration:line-through; color:#999; margin-left:8px;">{{ previewVariant.currency }} {{ previewVariant.price }}</span>
              </div>
              <div style="color: #6b7280; margin-top:4px;">SKU: {{ previewVariant.sku }}</div>
              <div :style="{ color: previewVariant.stock > 0 ? '#059669' : '#dc2626', marginTop: '6px' }">
                {{ previewVariant.stock > 0 ? 'In stock' : 'Out of stock' }}
              </div>
            </div>
          </div>
        </div>

        <div v-if="availabilityWarning" class="warning" style="color:#b45309; margin-top:8px;">
          {{ availabilityWarning }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.variant-selector-root { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
.loader { color: #6b7280; }
.error { color: #dc2626; }
.no-attrs { color: #6b7280; }

.group { margin-bottom: 0.75rem; }
.group-title { font-weight: 600; margin-bottom: 0.5rem; color:#111827; }

.swatches { display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center; }
.swatch-btn { display:flex; align-items:center; gap:0.5rem; padding:6px 8px; border-radius:8px; background:transparent; border: none; cursor:pointer; }
.swatch-btn.disabled { opacity:0.4; cursor:not-allowed; }
.swatch-circle { width:32px; height:32px; border-radius:50%; display:inline-block; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.swatch-label { font-size:0.85rem; color:#374151; margin-left:4px; }

.option-buttons { display:flex; gap:0.5rem; flex-wrap:wrap; }
.opt-btn { padding:6px 10px; border-radius:8px; border:1px solid #e5e7eb; background:#f9fafb; cursor:pointer; }
.opt-btn.selected { background:#111827; color:#fff; border-color:transparent; }
.opt-btn.disabled { opacity:0.45; cursor:not-allowed; }

.swatch-btn.selected .swatch-circle { outline: 2px solid #10b981; transform: scale(1.03); }
.preview { background:#fff; }

.warning { font-size:0.95rem; }
</style> -->


<template>
  <div class="variant-selector-root">
    <div v-if="loading" class="loader">Loading options...</div>
    <div v-else-if="error" class="error">Failed to load variants</div>

    <div v-else>
      <div v-if="attributeGroups.length === 0" class="no-attrs">
        No variants or attributes available
      </div>

      <div v-else>
        <!-- Attribute groups -->
        <div v-for="group in attributeGroups" :key="group.id" class="group">
          <div class="group-title">{{ group.name }}</div>

          <!-- color swatches -->
          <div v-if="group.isColor" class="swatches">
            <button
              v-for="val in group.values"
              :key="val.id"
              class="swatch-btn"
              :class="{
                selected: selectedAttrs[group.id] === val.id,
                disabled: isDisabled(group.id, val.id)
              }"
              :disabled="isDisabled(group.id, val.id)"
              @click="onSelectValue(group.id, val.id)"
              :aria-pressed="selectedAttrs[group.id] === val.id"
              :title="valueLabel(val)"
            >
              <span
                class="swatch-circle"
                :style="swatchStyle(val)"
              ></span>
              <span v-if="!isHex(val.value)" class="swatch-label">{{ valueLabel(val) }}</span>
            </button>
          </div>

          <!-- normal option buttons -->
          <div v-else class="option-buttons">
            <button
              v-for="val in group.values"
              :key="val.id"
              class="opt-btn"
              :class="{ selected: selectedAttrs[group.id] === val.id, disabled: isDisabled(group.id, val.id) }"
              :disabled="isDisabled(group.id, val.id)"
              @click="onSelectValue(group.id, val.id)"
            >
              {{ valueLabel(val) }}
            </button>
          </div>
        </div>

        <!-- preview / selected summary -->
        <div v-if="previewVariant" class="preview">
          <div class="preview-grid">
            <img :src="previewVariant.image" alt="variant image" class="preview-img" />
            <div>
              <div class="price">
                {{ previewVariant.currency }} {{ previewVariant.discount_price }}
                <span class="old-price">{{ previewVariant.currency }} {{ previewVariant.price }}</span>
              </div>
              <div class="sku">SKU: {{ previewVariant.sku }}</div>
              <div :class="previewVariant.stock > 0 ? 'in-stock' : 'out-stock'">
                {{ previewVariant.stock > 0 ? 'In stock' : 'Out of stock' }}
              </div>
            </div>
          </div>
        </div>

        <!-- controls -->
        <div class="controls">
          <button @click="resetSelection" class="reset-btn">Reset</button>
          <button @click="addToCart" :disabled="!finalVariant || finalVariant.stock <= 0" class="add-cart">
            Add to cart
          </button>
        </div>

        <div v-if="availabilityWarning" class="warning">{{ availabilityWarning }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
/* eslint-disable no-unused-vars */
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useVariantStore } from '~/stores/modules/product/variantStore'

// ------------------------------
// Props & Emits
// ------------------------------
const props = defineProps({
  productId: { type: String, required: true }
})
const emit = defineEmits(['select', 'update-image', 'update-price', 'update-stock'])

// ------------------------------
// Store & local reactive state
// ------------------------------
const variantStore = useVariantStore()

const loading = ref(true)
const error = ref(null)

const selectedAttrs = ref({})    // { attribute_id: value_id }
const previewVariant = ref(null) // preview for partial or full match
const availabilityWarning = ref(null)

// router (URL sync)
const router = useRouter()
const route = useRoute()

// store accessors
const storeVariants = computed(() => variantStore.variants || [])
const storeAvailableAttributes = computed(() => variantStore.available_attributes || {})
const storeCombinationMap = computed(() => variantStore.combination_map || {})
const storeSelectedVariant = computed(() => variantStore.selectedVariant || null)

// ------------------------------
// Utility helpers
// ------------------------------
function isHex(v) {
  return /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test((v || '').toString().trim())
}
function valueLabel(v) {
  return v?.value ?? v?.name ?? String(v)
}
function swatchStyle(val) {
  const color = isHex(val.value) ? val.value : '#fff'
  const border = isHex(val.value) ? '1px solid rgba(0,0,0,0.12)' : '1px solid #e5e7eb'
  return { background: color, border }
}
function isColorGroup(name, sampleValue) {
  if (!name && !sampleValue) return false
  const n = (name || '').toLowerCase()
  if (['color', 'colour', 'shade'].some(x => n.includes(x))) return true
  return isHex(sampleValue)
}
function buildKey(map) {
  return Object.keys(map)
    .filter(k => map[k] != null)
    .map(k => `${k}:${map[k]}`)
    .sort()
    .join('|')
}

// ------------------------------
// Derived data (attribute groups)
// ------------------------------
const attributeGroups = computed(() => {
  const aa = storeAvailableAttributes.value || {}
  return Object.keys(aa).map(id => {
    const group = aa[id]
    const sample = (group.values && group.values[0] && group.values[0].value) || null
    return {
      id,
      name: group.name,
      values: group.values || [],
      isColor: isColorGroup(group.name, sample)
    }
  })
})

// ------------------------------
// Variant lookup helpers
// ------------------------------
const variantLookup = computed(() => {
  // Build a map key -> variant object for O(1) exact lookups
  const map = {}
  for (const v of storeVariants.value || []) {
    const key = (v.attributes || []).map(a => `${a.attribute_id}:${a.value_id}`).sort().join('|')
    map[key] = v
  }
  return map
})

function findMatchingVariants(attrsMap) {
  if (!storeVariants.value?.length) return []
  // Return variants that match all selected keys in attrsMap
  return storeVariants.value.filter(v => {
    const vm = {}
    for (const a of v.attributes || []) vm[a.attribute_id] = a.value_id
    for (const k of Object.keys(attrsMap)) {
      if (attrsMap[k] == null) continue
      if (vm[k] !== attrsMap[k]) return false
    }
    return true
  })
}

// is option available given current partial selection
function isAvailable(attrId, valId) {
  const trial = { ...selectedAttrs.value, [attrId]: valId }
  const matches = findMatchingVariants(trial)
  return matches.length > 0
}
function isDisabled(attrId, valId) { return !isAvailable(attrId, valId) }

// ------------------------------
// Selection logic
// ------------------------------
function selectAttrsFromVariant(variant) {
  const map = {}
  for (const a of variant.attributes || []) {
    if (a.attribute_id && a.value_id) map[a.attribute_id] = a.value_id
  }
  selectedAttrs.value = map
}

function applyFinalVariant(variant) {
  previewVariant.value = variant
  variantStore.setSelectedVariant(variant)
  emit('select', variant)
  if (variant.image) emit('update-image', variant.image)
  if (variant.discount_price) emit('update-price', variant.discount_price)
  if (variant.stock !== undefined) emit('update-stock', variant.stock)
}

// User clicks an option
function onSelectValue(attrId, valId) {
  // toggle selection
  if (selectedAttrs.value[attrId] === valId) {
    selectedAttrs.value = { ...selectedAttrs.value, [attrId]: null }
  } else {
    selectedAttrs.value = { ...selectedAttrs.value, [attrId]: valId }
  }
  availabilityWarning.value = null

  // find matches for current partial selection
  const matches = findMatchingVariants(selectedAttrs.value)

  if (matches.length === 1) {
    applyFinalVariant(matches[0])
  } else if (matches.length > 1) {
    // preview first match
    previewVariant.value = matches[0]
    if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
  } else {
    previewVariant.value = null
    availabilityWarning.value = 'This combination is not available.'
  }

  // update URL query param if exact key maps to variant id (combination_map preferred)
  const key = buildKey(selectedAttrs.value)
  const mappedId = storeCombinationMap.value?.[key] || null
  if (mappedId) {
    router.replace({ query: { ...route.query, variant: mappedId } }).catch(() => {})
  } else {
    const q = { ...route.query }; delete q.variant
    router.replace({ query: q }).catch(() => {})
  }
}

// reset selection
function resetSelection() {
  selectedAttrs.value = {}
  previewVariant.value = variantStore.selectedVariant || null
  availabilityWarning.value = null
  const q = { ...route.query }; delete q.variant
  router.replace({ query: q }).catch(() => {})
}

// Add to cart (emit selected preview / final)
function addToCart() {
  const target = previewVariant.value || variantStore.selectedVariant
  if (!target) return
  emit('select', target)
}

// computed finalVariant if selection matches exactly
const finalVariant = computed(() => {
  const key = buildKey(selectedAttrs.value)
  const id = storeCombinationMap.value?.[key]
  if (!id) return null
  return storeVariants.value.find(v => v.id === id) || (variantLookup.value && variantLookup.value[key]) || null
})

// ------------------------------
// Load & init
// ------------------------------
async function load() {
  try {
    loading.value = true
    error.value = null

    const res = await variantStore.fetchVariants(props.productId)

    if (!res || res.success === false) {
      throw res || new Error('Failed to load variants')
    }

    // URL variant override
    const urlVariantId = route.query.variant
    if (urlVariantId) {
      const found = storeVariants.value.find(v => v.id === urlVariantId)
      if (found) {
        selectAttrsFromVariant(found)
        applyFinalVariant(found)
        return
      }
    }

    // default: use storeSelectedVariant (store auto-selected one)
    if (storeSelectedVariant.value) {
      selectAttrsFromVariant(storeSelectedVariant.value)
      previewVariant.value = storeSelectedVariant.value
      if (previewVariant.value?.image) emit('update-image', previewVariant.value.image)
      emit('select', storeSelectedVariant.value)
    } else if (storeVariants.value.length) {
      // fallback pick first or first in-stock
      const pick = storeVariants.value.find(v => v.stock > 0) || storeVariants.value[0]
      if (pick) {
        selectAttrsFromVariant(pick)
        applyFinalVariant(pick)
      }
    }
  } catch (e) {
    error.value = e
  } finally {
    loading.value = false
  }
}

onMounted(load)

// react to external store selectedVariant changes
watch(storeSelectedVariant, (nv) => {
  if (!nv) return
  selectAttrsFromVariant(nv)
  previewVariant.value = nv
  emit('select', nv)
  if (nv.image) emit('update-image', nv.image)
})
</script>

<style scoped>
.variant-selector-root { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }
.loader { color: #6b7280; }
.error { color: #dc2626; }
.no-attrs { color: #6b7280; }

.group { margin-bottom: 0.75rem; }
.group-title { font-weight: 600; margin-bottom: 0.5rem; color:#111827; }

.swatches { display:flex; gap:0.5rem; flex-wrap:wrap; align-items:center; }
.swatch-btn { display:flex; align-items:center; gap:0.5rem; padding:6px 8px; border-radius:8px; background:transparent; border: none; cursor:pointer; }
.swatch-btn.disabled { opacity:0.4; cursor:not-allowed; }
.swatch-circle { width:32px; height:32px; border-radius:50%; display:inline-block; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.swatch-label { font-size:0.85rem; color:#374151; margin-left:4px; }

.option-buttons { display:flex; gap:0.5rem; flex-wrap:wrap; }
.opt-btn { padding:6px 10px; border-radius:8px; border:1px solid #e5e7eb; background:#f9fafb; cursor:pointer; }
.opt-btn.selected { background:#111827; color:#fff; border-color:transparent; }
.opt-btn.disabled { opacity:0.45; cursor:not-allowed; }

.swatch-btn.selected .swatch-circle { outline: 2px solid #10b981; transform: scale(1.03); }

.preview { background:#fff; margin-top:10px; border:1px solid #eee; padding:12px; border-radius:8px; }
.preview-grid { display:flex; gap:1rem; align-items:center; }
.preview-img { width:96px; height:96px; object-fit:cover; border-radius:6px; }

.controls { display:flex; gap:10px; margin-top:10px; }
.reset-btn { background:#fff; padding:8px 12px; border:1px solid #e5e7eb; border-radius:6px; cursor:pointer; }
.add-cart { background:#111827; color:#fff; padding:8px 12px; border-radius:6px; border:none; cursor:pointer; }
.warning { color:#b45309; margin-top:8px; }
.in-stock { color:#059669; margin-top:6px; }
.out-stock { color:#dc2626; margin-top:6px; }
</style>
