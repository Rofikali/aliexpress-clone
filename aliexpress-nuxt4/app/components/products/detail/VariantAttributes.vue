


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
