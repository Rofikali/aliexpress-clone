// import axios from "axios"

// export default defineNuxtPlugin((NuxtApp) => {

//     // axios.defaults.withCredentials = true;
//     axios.defaults.baseURL = 'http://localhost:8000'

//     return {
//         provide: {
//             axios: axios
//         },
//     }
// })


// ~/plugins/axios.js
import axios from 'axios'

export default defineNuxtPlugin((nuxtApp) => {
    const config = useRuntimeConfig()

    const instance = axios.create({
        baseURL: config.public.apiBase,
        timeout: 10000,
        headers: {
            'Content-Type': 'application/json',
        }
    })

    // Request Interceptor
    instance.interceptors.request.use((request) => {
        const token = useCookie('access_token').value
        if (token) {
            request.headers.Authorization = `Bearer ${token}`
        }
        return request
    })

    // Response Interceptor
    instance.interceptors.response.use(
        (response) => response,
        async (error) => {
            const originalRequest = error.config
            if (error.response?.status === 401 && !originalRequest._retry) {
                originalRequest._retry = true
                const refreshToken = useCookie('refresh_token').value

                if (refreshToken) {
                    try {
                        const { data } = await instance.post('/auth/refresh/', {
                            refresh: refreshToken
                        })
                        useCookie('access_token').value = data.access
                        originalRequest.headers.Authorization = `Bearer ${data.access}`
                        return instance(originalRequest)
                    } catch (refreshError) {
                        console.error('Token refresh failed:', refreshError)
                        navigateTo('/login')
                    }
                }
            }
            return Promise.reject(error)
        }
    )

    // Make instance available globally
    return {
        provide: {
            axios: instance
        }
    }
})
