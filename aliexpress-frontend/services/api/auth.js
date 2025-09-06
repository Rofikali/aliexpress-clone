// services/api/auth.js

import { useApi } from '~/composables/core/useApi'

// const API_PREFIX = '/api/v1'

/**
 * Auth Service
 * Handles login, register, logout, email verification
 */
export const AuthService = {
    /**
     * Register new user
     * @param {Object} payload - { username, email, password, phone_number, role }
     */
    async register(payload) {
        return await useApi(`/register/`, {
            method: 'POST',
            body: payload,
        })
    },

    /**
     * Login user
     * @param {Object} payload - { email, password }
     */
    async login(payload) {
        return await useApi(`/login/`, {
            method: 'POST',
            body: payload,
        })
    },

    /**
     * Verify email with OTP
     * @param {Object} payload - { email, otp }
     */
    async verifyEmail(payload) {
        return await useApi(`/email-verification-confirm/`, {
            method: 'POST',
            body: payload,
        })
    },

    /**
     * Refresh token
     * @param {string} refresh
     */
    async refreshToken(refresh) {
        return await useApi(`/refresh/`, {
            method: 'POST',
            body: { refresh },
        })
    },

    /**
     * Get current user profile
     */
    async profile() {
        return await useApi(`/profile/`, {
            method: 'GET',
        })
    },
}
