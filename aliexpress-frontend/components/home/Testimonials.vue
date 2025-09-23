<template>
  <section class="py-8">
    <h2>{{ data.title }}</h2>
    <div class="grid md:grid-cols-3 sm:grid-cols-2 gap-4">
      <div
        v-for="testi in data.testimonials || []"
        :key="testi.id"
        class="p-4 border rounded shadow-sm"
      >
        <p class="italic">"{{ testi.message }}"</p>
        <p class="mt-2 font-semibold">- {{ testi.name || 'Anonymous' }}</p>
      </div>
    </div>
    <div v-if="!data.testimonials || !data.testimonials.length">
      <p>No testimonials available.</p>
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  data: { type: Object, required: true }
})
</script>
