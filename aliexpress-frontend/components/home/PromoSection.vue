<template>
  <section class="bg-yellow-400 text-gray-900">
    <div class="max-w-7xl mx-auto px-6 py-16 text-center">
      <h2 class="text-3xl font-bold mb-8">🔥 Limited-Time Promotions</h2>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div v-for="promo in data.promotions" :key="promo.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg"
        >
          <img
            :src="promo.image || '/placeholder-promo.png'"
            alt="Promotion image"
            class="w-full h-40 object-cover rounded-lg mb-4"
          />
          <h3 class="text-xl font-semibold mb-2">{{ promo.title }}</h3>
          <p class="text-gray-600 mb-4">{{ promo.description }}</p>
          <button
            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
          >
            Shop Now
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
defineProps({
  data: {
    type: Object,
    required: true,
  },
});
</script>
