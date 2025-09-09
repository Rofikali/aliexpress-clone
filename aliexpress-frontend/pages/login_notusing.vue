<!-- <script setup>
import { useAuth } from '~/composables/useAuth'

const { login } = useAuth()
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

async function handleLogin() {
    loading.value = true
    errorMessage.value = ''

    try {
        await login({ email: email.value, password: password.value })
        await navigateTo('/') // Redirect after login
    } catch (err) {
        errorMessage.value = 'Invalid email or password'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="max-w-sm mx-auto mt-10">
        <h1 class="text-xl font-bold mb-4">Login</h1>

        <form @submit.prevent="handleLogin" class="space-y-4">
            <input v-model="email" type="email" placeholder="Email" class="border p-2 w-full" />
            <input v-model="password" type="password" placeholder="Password" class="border p-2 w-full" />

            <button type="submit" class="bg-blue-600 text-white px-4 py-2 w-full" :disabled="loading">
                {{ loading ? 'Logging in...' : 'Login' }}
            </button>

            <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
        </form>
    </div>
</template> -->


<script setup>
import { useProductStore } from "~/stores/modules/productStore";

// SSR-friendly fetching
const productStore = useProductStore();

await useAsyncData("products", () => productStore.fetchProducts({ page: 1 }));
</script>

<template>
    <div class="p-6">
        <h1 class="text-2xl font-bold mb-4">Products</h1>

        <!-- Loading -->
        <div v-if="productStore.loading" class="text-gray-500">Loading...</div>

        <!-- Error -->
        <div v-else-if="productStore.error" class="text-red-600">
            {{ productStore.error }}
        </div>

        <!-- Products -->
        <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div v-for="product in productStore.products" :key="product.id"
                class="border p-4 rounded-lg shadow-sm hover:shadow-md">
                <img v-if="product.image" :src="product.image" alt="product" class="w-full h-40 object-cover mb-2" />
                <h2 class="font-semibold">{{ product.title }}</h2>
                <p class="text-sm text-gray-500">{{ product.category?.name }}</p>
                <p class="text-lg font-bold mt-1">${{ product.price }}</p>
            </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between mt-6">
            <button v-if="productStore.pagination.previous" @click="productStore.fetchProducts({ page: 1 })"
                class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
                Prev
            </button>
            <button v-if="productStore.pagination.next" @click="productStore.fetchProducts({ page: 2 })"
                class="px-4 py-2 bg-gray-200 rounded hover:bg-gray-300">
                Next
            </button>
        </div>
    </div>
</template>
