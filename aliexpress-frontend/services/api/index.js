// // services/api/index.js
// import axios from "axios";
// import { useAuthStore } from "~/stores/modules/authStore";

// const api = axios.create({
//     baseURL: "http://localhost:8000/api/v1", // 👈 change to your DRF base URL
//     headers: {
//         "Content-Type": "application/json",
//     },
// });

// // ✅ Request interceptor → attach JWT token
// api.interceptors.request.use((config) => {
//     const authStore = useAuthStore();
//     if (authStore?.accessToken) {
//         config.headers.Authorization = `Bearer ${authStore.accessToken}`;
//     }
//     return config;
// });

// // ✅ Response interceptor → handle 401 & refresh
// api.interceptors.response.use(
//     (response) => response,
//     async (error) => {
//         const authStore = useAuthStore();
//         if (error.response?.status === 401 && authStore?.refreshToken) {
//             try {
//                 // Try refresh
//                 const { data } = await axios.post(
//                     "http://localhost:8000/api/v1/auth/refresh/",
//                     { refresh: authStore.refreshToken }
//                 );
//                 authStore.setAccessToken(data.access);

//                 // Retry original request
//                 error.config.headers.Authorization = `Bearer ${data.access}`;
//                 return api.request(error.config);
//             } catch (refreshError) {
//                 authStore.logout();
//             }
//         }
//         return Promise.reject(error);
//     }
// );

// export default api;


import * as products from "./product"
import * as categories from "./category"
import * as users from "./user"
import * as comments from "./comments"
import * as likes from "./like"

export const api = {
    products,
    categories,
    users,
    comments,
    likes,
}

// import { api } from "~/services/api"

// // Products
// const { data: products } = await api.products.getProducts({ page: 1 })

// // Categories
// const { data: cats } = await api.categories.getCategories()

// // Users
// const { data: user } = await api.users.getUserById(123)
