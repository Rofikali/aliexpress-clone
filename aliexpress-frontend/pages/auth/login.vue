<template>
    <div class="max-w-md mx-auto mt-16 p-6 bg-white shadow-md rounded-lg">
        <h2 class="text-2xl font-bold mb-4">Login</h2>

        <form @submit.prevent="handleLogin">
            <Input v-model="form.email" type="email" label="Email" placeholder="Enter email" required />

            <Input v-model="form.password" type="password" label="Password" placeholder="Enter password" required />

            <Button :loading="loading" type="submit" class="w-full mt-4">
                Login
            </Button>

            <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
        </form>
    </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useAuthStore } from "~/stores/modules/authStore";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const form = reactive({
    email: "",
    password: "",
});

const loading = ref(false);
const error = ref(null);

async function handleLogin() {
    loading.value = true;
    error.value = null;
    try {
        await authStore.loginUser(form.email, form.password);
        router.push("/profile/");
    } catch (err) {
        error.value = authStore.error || "Login failed";
    } finally {
        loading.value = false;
    }
}
</script>
