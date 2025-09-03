// // // stores/modules/productStore.js
// // import { defineStore } from "pinia";
// // import {
// //     getProducts,
// //     getProductById,
// //     createProduct,
// //     updateProduct,
// //     deleteProduct,
// // } from "~/services/api/products";

// // export const useProductStore = defineStore("products", () => {
// //     const products = ref([]);
// //     const currentProduct = ref(null);
// //     const loading = ref(false);
// //     const error = ref(null);

// //     async function fetchProducts(params = {}) {
// //         loading.value = true;
// //         try {
// //             const { data } = await getProducts(params);
// //             products.value = data.results || data; // supports cursor pagination
// //         } catch (err) {
// //             error.value = err.response?.data || err.message;
// //         } finally {
// //             loading.value = false;
// //         }
// //     }

// //     async function fetchProduct(id) {
// //         try {
// //             const { data } = await getProductById(id);
// //             currentProduct.value = data;
// //         } catch (err) {
// //             error.value = err.response?.data || err.message;
// //         }
// //     }

// //     async function addProduct(productData) {
// //         const { data } = await createProduct(productData);
// //         products.value.unshift(data);
// //     }

// //     async function editProduct(id, productData) {
// //         const { data } = await updateProduct(id, productData);
// //         currentProduct.value = data;
// //         products.value = products.value.map((p) => (p.id === id ? data : p));
// //     }

// //     async function removeProduct(id) {
// //         await deleteProduct(id);
// //         products.value = products.value.filter((p) => p.id !== id);
// //     }

// //     return {
// //         products,
// //         currentProduct,
// //         loading,
// //         error,
// //         fetchProducts,
// //         fetchProduct,
// //         addProduct,
// //         editProduct,
// //         removeProduct,
// //     };
// // });


// // stores/modules/productStore.js
// // import { defineStore } from "pinia";
// // import { useApi } from "~/composables/useApi";

// // export const useProductStore = defineStore("product", () => {
// //     const products = ref([]);
// //     const pagination = ref({ next: null, previous: null });
// //     const loading = ref(false);
// //     const error = ref(null);

// //     async function fetchProducts(params = {}) {
// //         loading.value = true;
// //         error.value = null;

// //         const query = new URLSearchParams(params).toString();
// //         const url = `/products/${query ? `?${query}` : ""}`;
// //         console.log('stoductSTORE URL ', url);

// //         try {
// //             const { data, error: apiError } = await useApi(url);
// //             console.log('data is ', data.data);
// //             if (apiError) throw apiError;

// //             products.value = data?.results || data?.products || [];
// //             pagination.value = {
// //                 next: data?.next || null,
// //                 previous: data?.previous || null,
// //             };
// //         } catch (err) {
// //             error.value = err?.data?.detail || "Failed to load products";
// //         } finally {
// //             loading.value = false;
// //         }
// //     }

// //     async function fetchMore() {
// //         if (!pagination.value.next) return null;

// //         try {
// //             const { data } = await useApi(pagination.value.next);
// //             if (Array.isArray(data?.results) || Array.isArray(data?.products)) {
// //                 products.value.push(...(data.results || data.products));
// //             }
// //             pagination.value.next = data?.next || null;
// //             return data;
// //         } catch (err) {
// //             error.value = err?.data?.detail || "Failed to load more products";
// //         }
// //     }

// //     return {
// //         products,
// //         pagination,
// //         loading,
// //         error,
// //         fetchProducts,
// //         fetchMore,
// //     };
// // });


// import { defineStore } from "pinia";
// import { useApi } from "~/composables/useApi";

// export const useProductStore = defineStore("product", () => {
//     const products = ref([]);
//     const pagination = ref({ next: null, previous: null });
//     const loading = ref(false);
//     const error = ref(null);

//     async function fetchProducts(params = {}) {
//         loading.value = true;
//         error.value = null;

//         try {
//             const { data, error: apiError } = await useApi("/products/", {
//                 query: params,
//             });

//             if (apiError) throw apiError;

//             products.value = data?.results || data?.products || [];
//             pagination.value = {
//                 next: data?.next || null,
//                 previous: data?.previous || null,
//             };
//         } catch (err) {
//             error.value = err?.data?.detail || "Failed to load products";
//         } finally {
//             loading.value = false;
//         }
//     }

//     function resetProducts() {
//         products.value = [];
//         pagination.value = { next: null, previous: null };
//         error.value = null;
//     }

//     return {
//         products,
//         pagination,
//         loading,
//         error,
//         fetchProducts,
//         resetProducts,
//     };
// });




// import { defineStore } from 'pinia'

// export const useProductStore = defineStore('product', () => {
//     const products = ref([])
//     const loading = ref(false)
//     const error = ref(null)

//     async function fetchProducts(params = {}) {
//         loading.value = true
//         error.value = null

//         const query = new URLSearchParams(params).toString()
//         const url = `/products/${query ? `?${query}` : ''}`

//         const { $api } = useNuxtApp()

//         try {
//             const { data, error: apiError } = await $api(url)
//             if (apiError) throw apiError
//             products.value = data?.results || []
//         } catch (err) {
//             error.value = err?.data?.detail || 'Failed to load products'
//         } finally {
//             loading.value = false
//         }
//     }

//     return { products, loading, error, fetchProducts }
// })

// ~/stores/modules/productStore.js
import { defineStore } from "pinia"
import { ref } from "vue"
import { useApi } from "~/composables/core/useApi"

export const useProductStore = defineStore("productStore", () => {
    const products = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Pagination state
    const page = ref(1)
    const hasNext = ref(true)
    const pageSize = 12 // or configure via backend

    /**
     * Reset products (e.g., when filter/search changes)
     */
    function resetProducts() {
        products.value = []
        page.value = 1
        hasNext.value = true
    }

    /**
     * Load products for a specific page
     */
    async function fetchProducts({ page: pageParam = 1 } = {}) {
        loading.value = true
        error.value = null
        try {
            const { data, status, error: fetchError } = await useApi(`/products/?page=${pageParam}&page_size=${pageSize}`, {
                method: "GET",
            })

            if (status !== 200 || fetchError) {
                throw fetchError || new Error("Failed to fetch products")
            }

            // Support both list or cursor pagination style
            const results = data?.results || data?.products || []
            const next = data?.next || null

            if (pageParam === 1) {
                products.value = results
            } else {
                products.value.push(...results)
            }

            hasNext.value = Boolean(next) && results.length > 0
            page.value = pageParam

        } catch (err) {
            console.error("fetchProducts failed:", err)
            error.value = err
        } finally {
            loading.value = false
        }
    }

    /**
     * Load next page (for infinite scroll)
     */
    async function loadMore() {
        if (!hasNext.value || loading.value) return
        await fetchProducts({ page: page.value + 1 })
    }

    return {
        products,
        loading,
        error,
        page,
        hasNext,
        resetProducts,
        fetchProducts,
        loadMore,
    }
})
