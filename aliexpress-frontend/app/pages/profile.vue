<script setup>
import { useAuth } from '~/app/composables/useAuth'

definePageMeta({
    middleware: 'auth'
})

const { user } = useAuth()
</script>

<template>
    <div class="max-w-md mx-auto mt-10">
        <h1 class="text-xl font-bold">Profile</h1>
        <pre>{{ user }}</pre>
    </div>
</template>
