
<template>
  <div>
    <h1 class="text-2xl font-bold mb-4">Homepage</h1>

    <div v-if="loading" class="text-center py-10">Loading homepage...</div>
    <div v-else-if="error" class="text-center text-red-500 py-10">
      {{ error.message || "Something went wrong" }}
    </div>


    <div v-else>
      <strong>Hero Section</strong>
      <LazyHomeHero v-if="heroSection" :data="heroSection" />
      <br>

      <strong>Banner Section</strong>
      <LazyHomeBanner v-if="bannerSection" :data="bannerSection" />

      <strong>Featured Products</strong>
      <LazyHomeFeaturedProducts
        v-if="featuredProductsSection"
        :data="featuredProductsSection"
      />

      <LazyHomeCategories v-if="categoriesSection" :data="categoriesSection" />

      <LazyHomePromoSection 
        v-if="promotions && promotions.promotions && promotions.promotions.length" 
        :data="promotions" 
      />
      <div v-else>No promotions data</div>

      <strong>For Feauture Plan</strong>
      <LazyHomeTestimonials v-if="testimonialsSection" :data="testimonialsSection" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"
import { storeToRefs } from "pinia"
import { useHomepageStore } from "~/stores/modules/homepage/homepageStore"

const homeStore = useHomepageStore()
const { sections, loading, error } = storeToRefs(homeStore)
console.log('sectins in index.vue ', sections);
const { fetchHomepageData } = homeStore

onMounted(() => {
  fetchHomepageData()
})

const heroSection = computed(() => sections.value.find(s => s.type === "hero"))
const bannerSection = computed(() => sections.value.find(s => s.type === "banner"))
const featuredProductsSection = computed(() => sections.value.find(s => s.type === "products"))
const categoriesSection = computed(() => sections.value.find(s => s.type === "categories"))
const testimonialsSection = computed(() => sections.value.find(s => s.type === "testimonials"))
const promotions = computed(() => {
  return sections.value.find(s => s.type === "promo");
});


</script>

<!-- <template>
  <div class="min-h-screen bg-gray-50">
    <header class="sticky top-0 z-50 bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-6 flex items-center justify-between h-16">
        Logo
        <a href="/" class="flex items-center gap-2">
          <img src="/google-logo.png" alt="Logo" class="w-10 h-10" />
          <span class="text-xl font-bold text-gray-800">MyShop</span>
        </a>

        Search
        <div class="flex-1 px-4">
          <form @submit.prevent="onSearch" class="relative max-w-md mx-auto">
            <input
              v-model="query"
              type="search"
              placeholder="Search products..."
              class="w-full rounded-md border border-gray-300 px-4 py-2 pr-12 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
            <button
              type="submit"
              class="absolute right-1 top-1/2 -translate-y-1/2 text-gray-600"
            >
              🔍
            </button>
          </form>
        </div>

        Icons
        <div class="flex items-center gap-4">
          Wishlist
          <button class="p-2 rounded hover:bg-gray-100">❤️</button>
          Cart
          <button class="relative p-2 rounded hover:bg-gray-100">
            🛒
            <span
              v-if="cartCount > 0"
              class="absolute -top-1 -right-1 bg-red-600 text-white text-xs rounded-full px-1"
            >
              {{ cartCount }}
            </span>
          </button>
          Account
          <a href="/account" class="p-2 rounded hover:bg-gray-100">👤</a>
        </div>
      </div>
    </header>

    <section class="relative bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-6 py-24 flex flex-col items-center text-center">
        <img src="/google-logo.png" alt="" class="w-24 h-24 mb-6" />
        <h1 class="text-4xl md:text-6xl font-bold mb-6">Welcome to MyShop</h1>
        <p class="text-lg md:text-xl max-w-2xl mb-8">
          Discover amazing products, top categories, and exclusive deals all in one place.
        </p>
        <button
          class="bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg shadow hover:bg-gray-100"
        >
          Shop Now
        </button>
      </div>
    </section>


    <section class="max-w-7xl mx-auto px-6 py-16">
      <h2 class="text-2xl font-bold mb-8">Browse Categories</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg cursor-pointer"
        >
          <img
            :src="cat.image || '/placeholder-category.png'"
            alt=""
            class="w-full h-32 object-cover rounded-lg mb-4"
          />
          <h3 class="text-lg font-semibold">{{ cat.name }}</h3>
        </div>
      </div>
    </section>


    <section class="bg-gray-100 py-16">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-2xl font-bold mb-8">Featured Products</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="prod in products"
            :key="prod.id"
            class="bg-white rounded-xl shadow p-4 hover:shadow-lg cursor-pointer flex flex-col"
          >
            <img
              :src="prod.image || '/placeholder-product.png'"
              alt=""
              class="w-full h-40 object-cover rounded-lg mb-4"
            />
            <h3 class="font-medium text-gray-800 flex-1">{{ prod.title }}</h3>
            <p class="text-blue-600 font-bold mt-2">${{ prod.default_price }}</p>
          </div>
        </div>
      </div>
    </section>


    <section class="relative bg-yellow-400 text-gray-900">
      <div class="max-w-7xl mx-auto px-6 py-20 flex flex-col items-center text-center">
        <h2 class="text-3xl font-bold mb-4">Big Sale: Up to 50% Off</h2>
        <p class="mb-6">Don’t miss out on our limited-time discounts!</p>
        <button
          class="bg-gray-900 text-white px-6 py-3 rounded-lg shadow hover:bg-black"
        >
          Shop Deals
        </button>
      </div>
    </section>


    <section class="max-w-7xl mx-auto px-6 py-16">
      <h2 class="text-2xl font-bold mb-8">Top Shops</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        <div
          v-for="shop in shops"
          :key="shop.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg text-center"
        >
          <img
            :src="shop.logo || '/placeholder-shop.png'"
            alt=""
            class="w-20 h-20 object-cover rounded-full mx-auto mb-4"
          />
          <h3 class="text-lg font-semibold">{{ shop.name }}</h3>
          <p class="text-sm text-gray-500">Rating: {{ shop.rating }}</p>
        </div>
      </div>
    </section>


    <footer class="bg-white border-t">
      <div class="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-sm text-gray-600">&copy; 2025 MyShop. All rights reserved.</p>
        <div class="flex gap-4 text-gray-600">
          <a href="#">Privacy</a>
          <a href="#">Terms</a>
          <a href="#">Support</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from "vue"

const query = ref("")
const cartCount = ref(0)

function onSearch() {
  console.log("Searching for:", query.value)
}

Dummy Data
const categories = [
  { id: 1, name: "Electronics", image: "/google-logo.png" },
  { id: 2, name: "Fashion", image: "/visa.png" },
  { id: 3, name: "Home & Kitchen", image: "/github-logo.png" },
  { id: 4, name: "Sports", image: "/cart-empty.png" },
]

const products = [
  { id: 1, title: "Wireless Headphones", default_price: 59.99, image: "/cart-empty.png" },
  { id: 2, title: "Smart Watch", default_price: 120.0, image: "/github-logo.png" },
  { id: 3, title: "Running Shoes", default_price: 75.0, image: "/visa.png" },
  { id: 4, title: "Backpack", default_price: 35.5, image: "/google-logo.png" },
]

const shops = [
  { id: 1, name: "TechWorld", logo: "/shop-tech.jpg", rating: 4.8 },
  { id: 2, name: "StyleHub", logo: "/shop-style.jpg", rating: 4.5 },
  { id: 3, name: "HomeEssentials", logo: "/shop-home.jpg", rating: 4.6 },
  { id: 4, name: "Sportify", logo: "/shop-sport.jpg", rating: 4.7 },
]
</script>

<style scoped>
/* clamp 2 lines for product titles if too long */
h3 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> -->



<!-- <template>
  <div class="min-h-screen bg-gray-50">

    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <img src="/google-logo.png" alt="Logo" class="h-10 w-10" />
          <span class="text-xl font-bold text-gray-800">MyShop</span>
        </div>
        <nav class="hidden md:flex space-x-6 text-gray-600 font-medium">
          <a href="#" class="hover:text-blue-600">Home</a>
          <a href="#" class="hover:text-blue-600">Categories</a>
          <a href="#" class="hover:text-blue-600">Products</a>
          <a href="#" class="hover:text-blue-600">Shops</a>
          <a href="#" class="hover:text-blue-600">Contact</a>
        </nav>
        <div class="flex items-center space-x-4">
          <img src="/cart-empty.png" alt="Cart" class="h-8 w-8 cursor-pointer" />
          <img src="/github-logo.png" alt="User" class="h-8 w-8 cursor-pointer rounded-full" />
        </div>
      </div>
    </header>


    <section class="relative bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
      <div class="max-w-7xl mx-auto px-6 py-24 flex flex-col items-center text-center">
        <img src="/google-logo.png" alt="" class="h-20 w-20 mb-4" />
        <h1 class="text-4xl md:text-6xl font-bold mb-6">Welcome to MyShop</h1>
        <p class="text-lg md:text-xl max-w-2xl mb-8">
          Discover amazing products, top categories, and exclusive deals all in one place.
        </p>
        <button
          class="bg-white text-blue-600 font-semibold px-6 py-3 rounded-lg shadow hover:bg-gray-100"
        >
          Shop Now
        </button>
      </div>
    </section>


    <section class="max-w-7xl mx-auto px-6 py-16">
      <h2 class="text-2xl font-bold mb-8">Browse Categories</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        <div
          v-for="cat in categories"
          :key="cat.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg cursor-pointer"
        >
          <img
            :src="cat.image || '/placeholder-category.png'"
            alt=""
            class="w-full h-32 object-cover rounded-lg mb-4"
          />
          <h3 class="text-lg font-semibold">{{ cat.name }}</h3>
        </div>
      </div>
    </section>


    <section class="bg-yellow-400 text-gray-900">
      <div class="max-w-7xl mx-auto px-6 py-16 text-center">
        <h2 class="text-3xl font-bold mb-4">🔥 Limited-Time Promotions</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div
            v-for="promo in promotions"
            :key="promo.id"
            class="bg-white rounded-xl shadow p-6 hover:shadow-lg"
          >
            <img
              :src="promo.image || '/placeholder-promo.png'"
              alt=""
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


    <section class="bg-gray-100 py-16">
      <div class="max-w-7xl mx-auto px-6">
        <h2 class="text-2xl font-bold mb-8">Featured Products</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <div
            v-for="prod in products"
            :key="prod.id"
            class="bg-white rounded-xl shadow p-4 hover:shadow-lg cursor-pointer flex flex-col"
          >
            <img
              :src="prod.image || '/placeholder-product.png'"
              alt=""
              class="w-full h-40 object-cover rounded-lg mb-4"
            />
            <h3 class="font-medium text-gray-800 flex-1">{{ prod.title }}</h3>
            <p class="text-blue-600 font-bold mt-2">${{ prod.default_price }}</p>
          </div>
        </div>
      </div>
    </section>


    <section class="max-w-7xl mx-auto px-6 py-16">
      <h2 class="text-2xl font-bold mb-8">Top Shops</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
        <div
          v-for="shop in shops"
          :key="shop.id"
          class="bg-white rounded-xl shadow p-6 hover:shadow-lg text-center"
        >
          <img
            :src="shop.logo || '/placeholder-shop.png'"
            alt=""
            class="w-20 h-20 object-cover rounded-full mx-auto mb-4"
          />
          <h3 class="text-lg font-semibold">{{ shop.name }}</h3>
          <p class="text-sm text-gray-500">Rating: {{ shop.rating }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const categories = [
  { id: 1, name: "Electronics", image: "/google-logo.png" },
  { id: 2, name: "Fashion", image: "/visa.png" },
  { id: 3, name: "Home & Kitchen", image: "/github-logo.png" },
  { id: 4, name: "Sports", image: "/cart-empty.png" },
]

const promotions = [
  {
    id: 1,
    title: "Summer Sale – Up to 50% Off",
    description: "Get the hottest deals this season. Limited time only!",
    image: "/promo-summer.jpg",
  },
  {
    id: 2,
    title: "Buy 1 Get 1 Free",
    description: "Available on selected fashion items.",
    image: "/promo-bogo.jpg",
  },
  {
    id: 3,
    title: "Flash Sale – 24 Hours Only",
    description: "Exclusive discounts on electronics.",
    image: "/promo-flash.jpg",
  },
]

const products = [
  { id: 1, title: "Wireless Headphones", default_price: 59.99, image: "/cart-empty.png" },
  { id: 2, title: "Smart Watch", default_price: 120.0, image: "/github-logo.png" },
  { id: 3, title: "Running Shoes", default_price: 75.0, image: "/visa.png" },
  { id: 4, title: "Backpack", default_price: 35.5, image: "/google-logo.png" },
]

const shops = [
  { id: 1, name: "TechWorld", logo: "/shop-tech.jpg", rating: 4.8 },
  { id: 2, name: "StyleHub", logo: "/shop-style.jpg", rating: 4.5 },
  { id: 3, name: "HomeEssentials", logo: "/shop-home.jpg", rating: 4.6 },
  { id: 4, name: "Sportify", logo: "/shop-sport.jpg", rating: 4.7 },
]
</script> -->