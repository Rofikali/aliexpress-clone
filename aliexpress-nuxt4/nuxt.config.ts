export default defineNuxtConfig({
  runtimeConfig: {
    apiInternalBase: process.env.NUXT_API_INTERNAL_BASE || 'http://localhost:8000/api/v1',
    sessionCookieSecure: process.env.NUXT_SESSION_COOKIE_SECURE === 'true',
    public: {
      baseApi: '/api/backend',
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
