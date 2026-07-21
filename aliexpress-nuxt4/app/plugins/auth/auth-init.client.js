// // ~/plugins/auth-init.client.js
// import { defineNuxtPlugin } from '#app'
// import { useAuth } from '~/composables/useAuth'

// export default defineNuxtPlugin(() => {
//     const { init } = useAuth()
//     init()
// })

import { useAuthStore } from '~/stores/modules/authStore'

export default defineNuxtPlugin(async () => {
    const auth = useAuthStore()
    await auth.checkAuth()
})
