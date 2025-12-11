<!-- 

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

          Attribute detail
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

track expanded attribute IDs
const expanded = ref(new Set())

fetch attributes on mount and whenever variantId changes
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

toggle expand/collapse and fetch detail
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
</style> -->



<template>
  <div class="attributes">
    
    <!-- Loading -->
    <div v-if="attributeLoading">Loading attributes...</div>

    <!-- Error -->
    <div v-else-if="attributeError" class="error">
      {{ attributeError.message || "Failed to load attributes" }}
    </div>

    <!-- Attribute List -->
    <div v-else-if="attributes?.length">
      <h4 class="attributes-title">Attributes</h4>

      <div
        v-for="attr in attributes"
        :key="attr.id"
        class="attribute-row"
      >
        <strong class="attr-name">{{ attr.name }}:</strong>

        <!-- Show values -->
        <span class="attr-values">
          <span
            v-for="(value, index) in attr.values"
            :key="value.id"
          >
            {{ value.value }}<span v-if="index < attr.values.length - 1">, </span>
          </span>
        </span>
      </div>
    </div>

    <!-- When no attributes -->
    <div v-else>No attributes available</div>
  </div>
</template>

<script setup>
import { onMounted, watch } from "vue"
import { useAttributeStore } from "~/stores/modules/product/attributeStore"
import { storeToRefs } from "pinia"

const props = defineProps({
  productId: { type: String, required: true },
  variantId: { type: String, required: true }
})

const attributeStore = useAttributeStore()

const {
  attributes,
  attributeLoading,
  attributeError,
} = storeToRefs(attributeStore)

onMounted(async () => {
  await loadAttrs()
})

watch(() => props.variantId, async () => {
  await loadAttrs()
})

async function loadAttrs() {
  if (props.productId && props.variantId) {
    await attributeStore.fetchAttributes(props.productId, props.variantId)
  }
}
</script>

<style scoped>
.attributes {
  margin-top: 1rem;
}

.attributes-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 8px;
}

.attribute-row {
  display: flex;
  gap: 6px;
  margin-bottom: 6px;
}

.attr-name {
  min-width: 80px;
  font-weight: 600;
  text-transform: capitalize;
}

.attr-values {
  font-size: 0.95rem;
  color: #444;
}

.error {
  color: red;
}
</style>
