// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    runtimeConfig: {
        public: {
            apiBase: 'http://localhost:8000/', // Change to your Django API
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
    // runtimeConfig: {
    //     public: {
    //       stripePk: process.env.STRIPE_PK_KEY
    //     }
    // },
    // app: {
    //     head: {
    //       script: [
    //         { src: 'https://js.stripe.com/v3/', defer: true }
    //       ],
    //     }
    //   }
})


// nuxt.config.ts
// export default defineNuxtConfig({
//   runtimeConfig: {
//     public: {
//       apiBase: 'http://localhost:8000/api', // Change to your Django API
//     },
//   },
//   modules: ['@pinia/nuxt'],
// })
