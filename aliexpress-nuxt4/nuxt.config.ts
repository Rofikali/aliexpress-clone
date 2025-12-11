export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      baseApi: 'http://localhost:8000/api/v1', // Change to your Django API
    },
  },
  compatibilityDate: '2025-07-15',
  modules: ['@pinia/nuxt', '@nuxt/ui', '@nuxt/image'],
  css: ['~/assets/css/main.css'],
  devtools: { enabled: true },
})