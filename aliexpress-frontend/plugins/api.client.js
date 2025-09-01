// plugins/api.client.js
import { useApi } from '~/composables/useApi'

export default defineNuxtPlugin((nuxtApp) => {
    const $api = async (url, options = {}) => {
        return await useApi(url, options)
    }

    nuxtApp.provide('api', $api)
})
