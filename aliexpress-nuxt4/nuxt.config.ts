export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      baseApi: process.env.NUXT_PUBLIC_BASE_API || 'http://localhost:8000/api/v1',
    },
  },
  compatibilityDate: '2025-07-15',
  modules: ['@pinia/nuxt', '@nuxt/ui', '@nuxt/image'],
  css: ['~/assets/css/main.css'],
  devtools: { enabled: process.env.NODE_ENV === 'development' },
  routeRules: {
    '/**': {
      headers: {
        'X-Content-Type-Options': 'nosniff',
        'Referrer-Policy': 'strict-origin-when-cross-origin',
        'X-Frame-Options': 'DENY',
      },
    },
  },
})
