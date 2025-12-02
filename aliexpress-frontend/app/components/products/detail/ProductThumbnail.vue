<template>
  <img
    :src="src"
    class="thumbnail"
    :class="{ active }"
    @click="$emit('click')"
  />
</template>

<script setup>
const props = defineProps({
  src: String,
  active: Boolean
})
</script>

<style scoped>
.thumbnail {
  width: 60px;
  height: 60px;
  object-fit: cover;
  cursor: pointer;
  border: 2px solid transparent;
}
.thumbnail.active {
  border-color: blue;
}
</style>
