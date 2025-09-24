<script setup>

const route = useRoute()
const categoryId = route.params.id
</script>

<template>
  <div class="container mx-auto p-4">
     <lazy-category-products :id='categoryId' />
  </div>
</template>
