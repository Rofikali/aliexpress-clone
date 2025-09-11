// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
            baseApi: 'http://localhost:8000/api/v1', // Change to your Django API
        },
    },
    pages: true,
    modules: [
        'nuxt-icon',
        '@pinia/nuxt',
        '@pinia-plugin-persistedstate/nuxt',
        '@nuxtjs/tailwindcss',
        '@nuxt/image',
    ],
})
