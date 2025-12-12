<script setup lang="ts">
import { resolveColor, hexToApproxName } from "~/utils/colors"

const props = defineProps({
  label: String,
  value: String,
  selected: Boolean,
  disabled: Boolean
})

const emit = defineEmits(["select"])

const bg = computed(() => resolveColor(props.value))

// For text tooltips
const colorLabel = computed(() => {
  if (props.value.startsWith("#")) return hexToApproxName(props.value)
  return props.value
})
</script>

<template>
  <div
    class="relative flex items-center justify-center cursor-pointer transition-all"
    :class="[
      disabled ? 'opacity-40 cursor-not-allowed' : 'hover:scale-105',
    ]"
    @click="!disabled && emit('select', value)"
  >
    <!-- Swatch circle -->
    <div
      class="w-10 h-10 rounded-full border shadow-sm"
      :style="{ backgroundColor: bg }"
      :title="colorLabel"
    ></div>

    <!-- White color border fix -->
    <div
      v-if="bg === '#ffffff'"
      class="absolute inset-0 rounded-full border border-gray-300"
    ></div>

    <!-- Selected checkmark -->
    <div
      v-if="selected"
      class="absolute inset-0 rounded-full border-4 border-primary-500"
    ></div>

    <!-- Check mark icon -->
    <div v-if="selected" class="absolute text-white text-xs">
      ✓
    </div>
  </div>
</template>
