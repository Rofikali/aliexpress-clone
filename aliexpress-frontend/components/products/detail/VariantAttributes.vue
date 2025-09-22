<!-- ~/components/products/detail/VariantAttributes.vue -->

<!-- <template>
  <div class="attributes">
    <div v-if="attributeLoading">Loading attributes...</div>
    <div v-else-if="attributeError" class="error">
      {{ attributeError.message || "Failed to load attributes" }}
    </div>
    <div v-else-if="attributes?.length">
      <h4 class="attributes-title">Attributes</h4>
      <ul class="attribute-list">
        <li v-for="attr in attributes" :key="attr.id">
          <strong>{{ attr.name }}</strong>:
          <span v-for="val in attr.values" :key="val.id">{{ val.value }}</span>
        </li>
      </ul>
    </div>
    <div v-else>No attributes available</div>
  </div>
</template>

<script setup>
import { onMounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useAttributeStore } from "~/stores/modules/product/attributeStore"

const props = defineProps({
  productId: { type: String, required: true },
  variantId: { type: String, required: true },
})

const attributeStore = useAttributeStore()
const { attributes, attributeLoading, attributeError } = storeToRefs(attributeStore)

onMounted(() => {
  if (props.productId && props.variantId) {
    attributeStore.fetchAttributes(props.productId, props.variantId)
  }
})

watch(
  () => props.variantId,
  (newId) => {
    if (props.productId && newId) {
      attributeStore.fetchAttributes(props.productId, newId)
    }
  }
)
</script>

<style scoped>
.attributes {
  margin-top: 1rem;
}
.attributes-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.attribute-list {
  list-style: none;
  padding: 0;
}
.attribute-list li {
  margin-bottom: 0.25rem;
}
.error {
  color: red;
}
</style> -->



<!-- <template>
  <div class="attributes">

    <div v-if="attributeLoading">Loading attributes...</div>
    <div v-else-if="attributeError" class="error">
      {{ attributeError.message || "Failed to load attributes" }}
    </div>


    <div v-else-if="attributes?.length">
      <h4 class="attributes-title">Attributes</h4>
      <ul class="attribute-list">
        <li v-for="attr in attributes" :key="attr.id">
          <div class="attribute-header" @click="toggleExpand(attr)">
            <strong>{{ attr.name }}</strong>
            <span>{{ expandedAttribute?.id === attr.id ? "-" : "+" }}</span>
          </div>


          <div v-if="expandedAttribute?.id === attr.id" class="attribute-detail">
            <div v-if="detailLoading">Loading details...</div>
            <div v-else-if="detailError" class="error">
              {{ detailError.message || "Failed to load detail" }}
            </div>
            <pre v-else>{{ attributeDetail }}</pre>
          </div>
        </li>
      </ul>
    </div>


    <div v-else>No attributes available</div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue"
import { useAttributeStore } from "~/stores/modules/product/attributeStore"

const props = defineProps({
  productId: { type: String, required: true },
  variantId: { type: String, required: true },
})

const attributeStore = useAttributeStore()


const attributes = ref([])
const attributeLoading = ref(false)
const attributeError = ref(null)


const expandedAttribute = ref(null)
const attributeDetail = ref(null)
const detailLoading = ref(false)
const detailError = ref(null)


async function fetchAttributes() {
  if (!props.productId || !props.variantId) return
  attributeLoading.value = true
  attributeError.value = null
  try {
    const res = await attributeStore.fetchAttributes(props.productId, props.variantId)
    if (res.success) {
      attributes.value = res.data
    } else {
      attributeError.value = res
    }
  } catch (err) {
    attributeError.value = err
  } finally {
    attributeLoading.value = false
  }
}


async function fetchAttributeDetail(attrId) {
  if (!props.productId || !props.variantId || !attrId) return
  detailLoading.value = true
  detailError.value = null
  try {
    const res = await attributeStore.fetchAttributeById(props.productId, props.variantId, attrId)
    if (res.success) {
      attributeDetail.value = res.data
    } else {
      detailError.value = res
    }
  } catch (err) {
    detailError.value = err
  } finally {
    detailLoading.value = false
  }
}


function toggleExpand(attr) {
  if (expandedAttribute.value?.id === attr.id) {
    expandedAttribute.value = null
    attributeDetail.value = null
  } else {
    expandedAttribute.value = attr
    fetchAttributeDetail(attr.id)
  }
}


onMounted(fetchAttributes)


watch(() => props.variantId, async () => {
  expandedAttribute.value = null
  attributeDetail.value = null
  await fetchAttributes()
})
</script>

<style scoped>
.attributes {
  margin-top: 1rem;
}
.attributes-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.attribute-list {
  list-style: none;
  padding: 0;
}
.attribute-list li {
  margin-bottom: 0.25rem;
}
.attribute-header {
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  padding: 0.25rem 0;
}
.attribute-detail {
  padding-left: 1rem;
  background: #f9f9f9;
  margin-top: 0.25rem;
}
.error {
  color: red;
}
</style> -->




<template>
  <div class="attributes">
    <div v-if="attributeLoading">Loading attributes...</div>
    <div v-else-if="attributeError" class="error">
      {{ attributeError.message || "Failed to load attributes" }}
    </div>
    <div v-else-if="attributes?.length">
      <h4 class="attributes-title">Attributes</h4>
      <ul class="attribute-list">
        <li v-for="attr in attributes" :key="attr.id">
          <div class="attr-header" @click="toggleDetail(attr.id)">
            <strong>{{ attr.name }}</strong>
            <span class="toggle-indicator">{{ isExpanded(attr.id) ? "▲" : "▼" }}</span>
          </div>

          <!-- Attribute detail -->
          <div v-if="isExpanded(attr.id)" class="attr-detail">
            <div v-if="detailLoading">Loading details...</div>
            <div v-else-if="detailError" class="error">{{ detailError.message || 'Failed to load detail' }}</div>
            <div v-else-if="attributeDetail && attributeDetail.id === attr.id">
              <pre>{{ attributeDetail }}</pre>
            </div>
            <div v-else>No detail available</div>
          </div>
        </li>
      </ul>
    </div>
    <div v-else>No attributes available</div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import { storeToRefs } from "pinia"
import { useAttributeStore } from "~/stores/modules/product/attributeStore"

const props = defineProps({
  productId: { type: String, required: true },
  variantId: { type: String, required: true }
})

const attributeStore = useAttributeStore()
const {
  attributes,
  attributeLoading,
  attributeError,
  attributeDetail,
  detailLoading,
  detailError
} = storeToRefs(attributeStore)

// track expanded attribute IDs
const expanded = ref(new Set())

// fetch attributes on mount and whenever variantId changes
onMounted(async () => {
  if (props.productId && props.variantId) {
    await attributeStore.fetchAttributes(props.productId, props.variantId)
  }
})

watch(() => props.variantId, async (newId) => {
  if (props.productId && newId) {
    expanded.value.clear()
    await attributeStore.fetchAttributes(props.productId, newId)
  }
})

// toggle expand/collapse and fetch detail
async function toggleDetail(attrId) {
  if (expanded.value.has(attrId)) {
    expanded.value.delete(attrId)
  } else {
    expanded.value.clear() // only one expanded at a time
    expanded.value.add(attrId)
    await attributeStore.fetchAttributeById(props.productId, props.variantId, attrId)
  }
}

function isExpanded(attrId) {
  return expanded.value.has(attrId)
}
</script>

<style scoped>
.attributes {
  margin-top: 1rem;
}
.attributes-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.attribute-list {
  list-style: none;
  padding: 0;
}
.attribute-list li {
  margin-bottom: 0.5rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.25rem;
}
.attr-header {
  display: flex;
  justify-content: space-between;
  cursor: pointer;
}
.attr-detail {
  margin-top: 0.25rem;
  padding-left: 1rem;
  font-size: 0.9rem;
  background: #f9f9f9;
  border-left: 2px solid #ccc;
}
.error {
  color: red;
}
.toggle-indicator {
  font-weight: bold;
}
</style>
