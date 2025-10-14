<!-- <template>
    <div class="max-w-md mx-auto mt-16 p-6 bg-white shadow-md rounded-lg">
        <h2 class="text-2xl font-bold mb-4">Register</h2>

        <form @submit.prevent="handleRegister">
            <Input v-model="form.username" label="Username" placeholder="Enter username" required />

            <Input v-model="form.email" type="email" label="Email" placeholder="Enter email" required />

            <Input v-model="form.phone_number" label="Phone" placeholder="Enter phone number" required />

            <Input v-model="form.password" type="password" label="Password" placeholder="Enter password" required />

            <Select v-model="form.role" :options="roles" label="Role" required />

            <Button :loading="loading" type="submit" class="w-full mt-4">
                Register
            </Button>

            <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
        </form>
    </div>
</template>

<script setup>
import { reactive } from "vue";
import { useAuthStore } from "~/stores/modules/authStore";
import Input from "~/components/ui/Input.vue";
import Select from "~/components/ui/Select.vue";
import Button from "~/components/ui/Button.vue";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const roles = [
    { label: "Buyer", value: "buyer" },
    { label: "Seller", value: "seller" },
];

const form = reactive({
    username: "",
    email: "",
    phone_number: "",
    password: "",
    role: "buyer",
});

const loading = ref(false);
const error = ref(null);

async function handleRegister() {
    loading.value = true;
    error.value = null;
    try {
        const data = await authStore.registerUser(form);
        console.log("Registered successfully:", data);

        // Redirect to email verification page if OTP needed
        if (data.email_verification?.sent) {
            router.push({
                path: "/auth/verify-email",
                query: { email: form.email },
            });
        } else {
            router.push("/profile/");
        }
    } catch (err) {
        error.value = authStore.error || "Registration failed";
    } finally {
        loading.value = false;
    }
}
</script> -->

<script setup>
import { useToast } from '#imports'
import { z } from 'zod'

const toast = useToast()

const fields = [
    {
        name: 'email',
        type: 'email',
        label: 'Email',
        placeholder: 'Enter your email',
        required: true
    },
    {
        name: 'password',
        label: 'Password',
        type: 'password',
        placeholder: 'Enter your password',
        required: true
    },
    {
        name: 'remember',
        label: 'Remember me',
        type: 'checkbox'
    }
]

const providers = [
    {
        label: 'Google',
        icon: 'i-simple-icons-google',
        onClick: () => {
            toast.add({ title: 'Google', description: 'Login with Google' })
        }
    },
    {
        label: 'GitHub',
        icon: 'i-simple-icons-github',
        onClick: () => {
            toast.add({ title: 'GitHub', description: 'Login with GitHub' })
        }
    }
]

// ✅ Plain JS version (no TypeScript types)
const schema = z.object({
    email: z.string().email('Invalid email'),
    password: z.string().min(8, 'Must be at least 8 characters')
})

// ✅ Regular JS function for form submission
function onSubmit(payload) {
    console.log('Submitted', payload)
}
</script>

<template>
    <div class="flex flex-col items-center justify-center gap-4 p-4">
        <UPageCard class="w-full max-w-md">
            <UAuthForm :schema="schema" title="Login" description="Enter your credentials to access your account."
                icon="i-lucide-user" :fields="fields" :providers="providers" @submit="onSubmit" />
        </UPageCard>
    </div>
</template>
