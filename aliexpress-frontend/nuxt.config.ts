// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
            baseApi: 'http://localhost:8000/api/v1', // Change to your Django API
            // apiBase: 'http://localhost:8000', // Change to your Django API
        },
    },
    pages: true,
    modules: [
        'nuxt-icon',
        // 'nuxt-lodash',
        '@pinia/nuxt',
        '@pinia-plugin-persistedstate/nuxt',
        '@nuxtjs/tailwindcss',
        '@nuxt/image',
        // '@nuxtjs/supabase'
    ],
})
