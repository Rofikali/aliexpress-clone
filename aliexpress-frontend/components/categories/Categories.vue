<!-- <template>
  <section class="max-w-7xl mx-auto px-6 py-12">
    <h2 class="text-2xl font-bold mb-8 text-gray-800 text-center">
      Browse Categories
    </h2>

    <div v-if="category"
      class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6"
    >
      <NuxtLink
        to="#"
        class="group bg-white rounded-xl shadow hover:shadow-lg transition-all duration-300 overflow-hidden cursor-pointer"
        >

         <h1>Count - {{ category.id }}</h1>
        <div class="relative h-32 sm:h-40 w-full overflow-hidden">
          <img
            :src="category.image || '/github-logo.png'"
            :alt="category.name"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />

          <div
            class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"
          ></div>
        </div>


        <div class="p-4 text-center">
          <h3
            class="text-base font-semibold text-gray-800 group-hover:text-primary transition-colors"
          >
            {{ category.name }}
          </h3>
          <p class="text-xs text-gray-500 mt-1 line-clamp-2">
            {{ category.description }}
          </p>
        </div>
      </NuxtLink>
    </div>


    <div v-else
      v-if="!category || !category.length"
      class="text-center text-gray-500 mt-10"
    >
      No Categories Found.
    </div>
  </section>
</template>

<script setup>
const props = defineProps({
  category: {
    type: Array, // should be Array not Object
    required: true,
    default: () => [],
  },
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> -->


<!-- :to="{ name: 'home-categories-id', params: { id: category.id } }"  -->
 <!-- :to="{ name: 'home-categories-id', params: { id: category.id } }" -->


<template>
  <section>
    {{ category.id }}
    <NuxtLink
     :to="{ name: 'home-categories-id', params: { id: category.id } }"
      class="group block bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-gray-100"
    >
      <!-- Image -->
      <div class="relative h-40 sm:h-48 w-full overflow-hidden">
        <img
          :src="category.image || '/github-logo.png'"
          :alt="category.name"
          class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          loading="lazy"
        />
        <!-- Gradient overlay -->
        <div
          class="absolute inset-0 bg-gradient-to-t from-black/30 via-black/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        ></div>

      </div>

      <!-- Details -->
      <div class="p-4 text-center">
        <h3
          class="text-lg font-semibold text-gray-800 group-hover:text-primary transition-colors"
        >
          name - {{ category.name }}
        </h3>
        <h3
          class="text-lg font-semibold text-gray-800 group-hover:text-primary transition-colors"
        >
          slug - {{ category.slug }}
        </h3>
        <p
          class="text-sm text-gray-500 mt-2 line-clamp-2 group-hover:text-gray-600"
        >
          desc - {{ category.description }}
        </p>
      </div>
    </NuxtLink>
  </section>
</template>

<script setup>
const props = defineProps({
  category: {
    type: Object,
    required: true,
    default: () => ({}),
  },
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
