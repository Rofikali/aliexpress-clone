<template>
  <section>
    <h2>{{ data.title }}</h2>
    <div class="grid md:grid-cols-4 sm:grid-cols-2 gap-4">
      <div
        v-for="cat in data.categories || []"
        :key="cat.id"
        class="p-4 border rounded"
      >

      <NuxtLink :to="{ name: 'home-categories-id', params: { id: cat.category.id } }" class="block">
        <p>{{ cat.category.name || 'Unnamed Category' }}</p>
      </NuxtLink>
      <h1>ids : {{ cat.category.id }}</h1>
        <p>{{ cat.category.description || 'Unnamed Category' }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>




