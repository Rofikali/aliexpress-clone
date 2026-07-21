<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useAuthStore } from '~/stores/modules/authStore'

const auth = useAuthStore()
const form = reactive({ email: '', password: '' })
const error = ref<string | null>(null)

async function submit(): Promise<void> {
  error.value = null
  const response = await auth.login({ ...form })

  if (!response.success) {
    error.value = response.message || 'Unable to sign in'
    return
  }

  await navigateTo('/auth/profile')
}
</script>

<template>
  <main class="mx-auto mt-16 max-w-md rounded-lg bg-white p-6 shadow-md">
    <h1 class="mb-4 text-2xl font-bold">Sign in</h1>

    <form @submit.prevent="submit">
      <label class="mb-4 block" for="login-email">
        <span class="mb-1 block">Email</span>
        <input id="login-email" v-model="form.email" data-testid="login-email" class="w-full rounded border p-2" type="email" required>
      </label>

      <label class="mb-4 block" for="login-password">
        <span class="mb-1 block">Password</span>
        <input id="login-password" v-model="form.password" data-testid="login-password" class="w-full rounded border p-2" type="password" required>
      </label>

      <p v-if="error" class="mb-4 text-red-600" role="alert">{{ error }}</p>
      <button data-testid="login-submit" class="w-full rounded bg-red-600 p-2 text-white" :disabled="auth.loading" type="submit">
        {{ auth.loading ? 'Signing in…' : 'Sign in' }}
      </button>
    </form>
  </main>
</template>
