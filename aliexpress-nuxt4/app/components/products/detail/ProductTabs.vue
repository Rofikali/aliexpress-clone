<template>
  <div class="product-tabs">
    <div class="tab-buttons">
      <button
        v-for="tab in tabs"
        :key="tab"
        :class="{ active: currentTab === tab }"
        @click="currentTab = tab"
      >
        {{ tab }}
      </button>
    </div>

    <div class="tab-content">
      <slot name="description" v-if="currentTab === 'Description'" />
      <slot name="reviews" v-if="currentTab === 'Reviews'" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

const tabs = ["Description", "Reviews"]
const currentTab = ref("Description")
</script>

<style scoped>
.tab-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}
.tab-buttons button.active {
  font-weight: bold;
  border-bottom: 2px solid blue;
}
</style>
