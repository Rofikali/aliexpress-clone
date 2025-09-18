// // services/api/auth.js

// import { useApi } from '~/composables/core/base'

// // const API_PREFIX = '/api/v1'

// /**
//  * Auth Service
//  * Handles login, register, logout, email verification
//  */
// export const AuthService = {
//     /**
//      * Register new user
//      * @param {Object} payload - { username, email, password, phone_number, role }
//      */
//     async register(payload) {
//         return await useApi(`/register/`, {
//             method: 'POST',
//             body: payload,
//         })
//     },

//     /**
//      * Login user
//      * @param {Object} payload - { email, password }
//      */
//     async login(payload) {
//         return await useApi(`/login/`, {
//             method: 'POST',
//             body: payload,
//         })
//     },

//     /**
//      * Verify email with OTP
//      * @param {Object} payload - { email, otp }
//      */
//     async verifyEmail(payload) {
//         return await useApi(`/email-verification-confirm/`, {
//             method: 'POST',
//             body: payload,
//         })
//     },

//     /**
//      * Refresh token
//      * @param {string} refresh
//      */
//     async refreshToken(refresh) {
//         return await useApi(`/refresh/`, {
//             method: 'POST',
//             body: { refresh },
//         })
//     },

//     /**
//      * Get current user profile
//      */
//     async profile() {
//         return await useApi(`/profile/`, {
//             method: 'GET',
//         })
//     },
// }


// ~/services/api/auth.js
import { normalizeResponse, handleError } from "~/composables/core/base"

export const AuthService = {
    async register(payload) {
        try {
            const { $api } = useNuxtApp()
            const res = await $api.post("/register/", payload)
            return normalizeResponse(res)
        } catch (err) {
            return handleError(err)
        }
    },

    async login(payload) {
        try {
            const { $api } = useNuxtApp()
            const res = await $api.post("/login/", payload)
            return normalizeResponse(res)
        } catch (err) {
            return handleError(err)
        }
    },

    async profile() {
        try {
            const { $api } = useNuxtApp()
            const res = await $api.get("/profile/")
            return normalizeResponse(res)
        } catch (err) {
            return handleError(err)
        }
    },
}



// import { api } from '~/composables/core/base'

// const AUTH_PREFIX = "/api/v1"

// export const AuthService = {
//     /**
//      * Register new user
//      * @param {Object} payload - { username, email, password, phone_number, role }
//      */
//     async register(payload) {
//         return api("post", `${AUTH_PREFIX}/register/`, payload)
//     },

//     /**
//      * Login user
//      * @param {Object} payload - { email, password }
//      */
//     async login(payload) {
//         return api("post", `${AUTH_PREFIX}/login/`, payload)
//     },

//     /**
//      * Verify email with OTP
//      * @param {Object} payload - { email, otp }
//      */
//     async verifyEmail(payload) {
//         return api("post", `${AUTH_PREFIX}/email-verification-confirm/`, payload)
//     },

//     /**
//      * Refresh token
//      * @param {string} refresh
//      */
//     async refreshToken(refresh) {
//         return api("post", `${AUTH_PREFIX}/refresh/`, { refresh })
//     },

//     /**
//      * Get current user profile
//      * @param {string|null} token - optional access token
//      */
//     async profile(token = null) {
//         return api("get", `${AUTH_PREFIX}/profile/`, null, {
//             headers: authHeaders(token),
//         })
//     },
// }
