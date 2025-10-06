

<template>
  <div class="container mx-auto p-4">
     <lazy-category-products :id='categoryId' />
  </div>
</template>


<script setup>
// import { useCategoryStore } from '~/stores/modules/category/categoryPorductStore';
const route = useRoute()
const categoryId = route.params.id



</script>