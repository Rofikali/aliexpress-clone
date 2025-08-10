<script setup>
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
</template>
