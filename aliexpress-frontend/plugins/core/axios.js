// ~/plugins/core/axios.js
import axios from "axios"
import { useAuthStore } from "~/stores/modules/authStore"

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()

  const api = axios.create({
    baseURL: config.public.baseApi,
    timeout: 10000,
    headers: { "Content-Type": "application/json" },
  })

  // === Interceptors ===
  let isRefreshing = false
  let failedQueue = []

  const processQueue = (error, token = null) => {
    failedQueue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
    failedQueue = []
  }

  api.interceptors.request.use((req) => {
    const auth = useAuthStore()
    if (auth.tokens?.access) {
      req.headers.Authorization = `Bearer ${auth.tokens.access}`
    }
    return req
  })

  api.interceptors.response.use(
    (res) => res.data, // unwrap response
    async (error) => {
      const auth = useAuthStore()
      const originalRequest = error.config

      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          })
            .then((token) => {
              originalRequest.headers.Authorization = `Bearer ${token}`
              return api(originalRequest)
            })
            .catch((err) => Promise.reject(err))
        }

        originalRequest._retry = true
        isRefreshing = true

        try {
          const res = await axios.post(
            `${config.public.baseApi}/refresh/`,
            { refresh: auth.tokens.refresh }
          )

          const newAccess = res.data.data.access
          auth.setAccessToken(newAccess)

          processQueue(null, newAccess)
          originalRequest.headers.Authorization = `Bearer ${newAccess}`
          return api(originalRequest)
        } catch (err) {
          processQueue(err, null)
          auth.logout()
          return Promise.reject(err)
        } finally {
          isRefreshing = false
        }
      }

      return Promise.reject(error)
    }
  )

  // make available globally
  return {
    provide: {
      api,
    },
  }
})


















// // ~/plugins/core/axios.js
// import axios from 'axios'

// export default defineNuxtPlugin((nuxtApp) => {
//     const config = useRuntimeConfig()

//     const instance = axios.create({
//         baseURL: config.public.apiBase,
//         timeout: 10000,
//         headers: {
//             'Content-Type': 'application/json',
//         }
//     })

//     // Request Interceptor
//     instance.interceptors.request.use((request) => {
//         const token = useCookie('access_token').value
//         if (token) {
//             request.headers.Authorization = `Bearer ${token}`
//         }
//         return request
//     })

//     // Response Interceptor
//     instance.interceptors.response.use(
//         (response) => response,
//         async (error) => {
//             const originalRequest = error.config
//             if (error.response?.status === 401 && !originalRequest._retry) {
//                 originalRequest._retry = true
//                 const refreshToken = useCookie('refresh_token').value

//                 if (refreshToken) {
//                     try {
//                         const { data } = await instance.post('/refresh/', {
//                             refresh: refreshToken
//                         })
//                         useCookie('access_token').value = data.access
//                         originalRequest.headers.Authorization = `Bearer ${data.access}`
//                         return instance(originalRequest)
//                     } catch (refreshError) {
//                         console.error('Token refresh failed:', refreshError)
//                         navigateTo('/login')
//                     }
//                 }
//             }
//             return Promise.reject(error)
//         }
//     )

//     // Make instance available globally
//     return {
//         provide: {
//             axios: instance
//         }
//     }
// })
