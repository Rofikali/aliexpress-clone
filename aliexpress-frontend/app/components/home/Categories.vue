<template>
  <div>
    <section class="max-w-7xl mx-auto px-6 py-16">
      <h2 class="text-2xl font-bold mb-8">HOME/CATEGOIRES Browse Categories</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        <div v-for="cat in data || []" :key="cat.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg cursor-pointer">
          <NuxtLink :to="{ name: 'home-categories-id', params: { id: cat.id } }" class="block">
            <NuxtImg class="rounded-T" :src="cat.image || '/github-logo.png'" alt="Image Not Available"
              loading="lazy" />

            <h3 class="text-lg font-semibold">name - {{ cat.name }}</h3>
            <h2 class="text-lg font-semibold">desc - {{ cat.description }}</h2>
          </NuxtLink>
        </div>
        <div>No Products Related This Category .</div>
      </div>
    </section>
  </div>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>

<style scoped></style>