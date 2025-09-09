// // // ~/stores/modules/productStore.js
// // import { defineStore } from "pinia"
// // import { ref } from "vue"
// // import { useApi } from "~/composables/core/useApi"

// // export const useProductStore = defineStore("productStore", () => {
// //     const products = ref([])
// //     const loading = ref(false)
// //     const error = ref(null)

// //     // Pagination state
// //     const cursor = ref("first")  // backend cursor key
// //     const hasNext = ref(true)
// //     const pageSize = 12  // default page size; adjust in backend if needed

// //     /**
// //      * Reset products (e.g., on filter/search change)
// //      */
// //     function resetProducts() {
// //         products.value = []
// //         cursor.value = "first"
// //         hasNext.value = true
// //         error.value = null
// //     }

// //     /**
// //      * Fetch products from backend (supports cursor-based pagination)
// //      */
// //     async function fetchProducts({ cursorParam = cursor.value } = {}) {
// //         loading.value = true
// //         error.value = null

// //         try {
// //             const { data, status, error: fetchError } = await useApi(
// //                 `/products/?cursor=${cursorParam}&page_size=${pageSize}`,
// //                 { method: "GET" }
// //             )

// //             if (status !== 200 || fetchError) {
// //                 throw fetchError || new Error("Failed to fetch products")
// //             }

// //             // Backend response: { data: { results: [...], next: cursor } }
// //             const results = data?.data?.results || data?.data?.products || []
// //             const nextCursor = data?.data?.next || null

// //             // Prevent duplicates
// //             const existingIds = new Set(products.value.map(p => p.id))
// //             const newProducts = results.filter(p => !existingIds.has(p.id))

// //             products.value.push(...newProducts)
// //             cursor.value = nextCursor || null
// //             hasNext.value = Boolean(nextCursor) && newProducts.length > 0

// //             return { products: products.value, next: nextCursor }

// //         } catch (err) {
// //             console.error("[productStore] fetchProducts failed:", err)
// //             error.value = err.message || "Unknown error"
// //             throw err
// //         } finally {
// //             loading.value = false
// //         }
// //     }

// //     /**
// //      * Load next page (for infinite scroll)
// //      */
// //     async function loadMore() {
// //         if (!hasNext.value || loading.value) return
// //         await fetchProducts({ cursorParam: cursor.value })
// //     }

// //     /**
// //      * Fetch single product by ID
// //      */
// //     async function fetchProductById(id) {
// //         loading.value = true
// //         error.value = null

// //         try {
// //             const { data, status, error: fetchError } = await useApi(`/products/${id}/`, { method: "GET" })

// //             if (status !== 200 || fetchError) {
// //                 throw fetchError || new Error("Failed to fetch product")
// //             }

// //             // Replace or add product in store
// //             const index = products.value.findIndex(p => p.id === id)
// //             if (index > -1) products.value[index] = data.data || data
// //             else products.value.push(data.data || data)

// //             return data.data || data

// //         } catch (err) {
// //             console.error("[productStore] fetchProductById failed:", err)
// //             error.value = err.message || "Unknown error"
// //             throw err
// //         } finally {
// //             loading.value = false
// //         }
// //     }

// //     return {
// //         // state
// //         products,
// //         loading,
// //         error,
// //         cursor,
// //         hasNext,

// //         // actions
// //         resetProducts,
// //         fetchProducts,
// //         loadMore,
// //         fetchProductById,
// //     }
// // })


// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { useInfiniteScrollProducts } from "~/composables/products/useInfiniteScrollProducts"

// export const useProductStore = defineStore("productStore", () => {
//     // Infinite scroll composable handles cursor, loading, errors
//     const {
//         items: products,
//         isLoading,
//         error,
//         hasNext,
//         loadMore,
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,
//     } = useInfiniteScrollProducts({ pageSize: 12 }) // default pageSize configurable

//     /**
//      * Reset the store and reload first page
//      */
//     function reset() {
//         products.value = []
//         hasNext.value = true
//         sentinelRef.value = null
//         loadMore()
//     }

//     /**
//      * Manual reload (useful for filters/search)
//      */
//     async function reload() {
//         products.value = []
//         hasNext.value = true
//         await loadMore()
//     }

//     /**
//      * Fetch single product by ID
//      * Useful for product detail page
//      */
//     async function fetchProductById(id) {
//         try {
//             const { data, status } = await useApi(`/products/${id}/`, { method: "GET" })
//             if (status !== 200 || !data) throw new Error(data?.message || "Failed to fetch product")
//             return data
//         } catch (err) {
//             console.error("fetchProductById failed:", err)
//             throw err
//         }
//     }

//     return {
//         // Data
//         products,
//         isLoading,
//         error,
//         hasNext,

//         // Actions
//         loadMore,
//         reset,
//         reload,
//         fetchProductById,

//         // Sentinel for infinite scroll binding
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,
//     }
// })



// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { usePagination } from "~/composables/pagination/useBasePagination"
// import { useInfiniteScroll } from "~/composables/pagination/useInfiniteScroll"

// export const useProductStore = defineStore("productStore", () => {
//     // 1. Pagination composable for products
//     const {
//         products,
//         loading,
//         error,
//         hasNext,
//         nextCursor,
//         count,
//         fetchFirst,
//         loadMore,
//         reset,
//         forceReload,
//     } = usePagination("/products/", {
//         pageSize: 12,
//         dedupeKey: "id",
//         retries: 2,
//         retryBackoffMs: 300,
//         autoFetch: true,
//         debug: true,
//     })

//     console.log('inside productStore ', products);

//     // 2. Infinite scroll observer
//     const { sentinelRef, bindSentinel, unbindSentinel } = useInfiniteScroll({
//         loadMore,
//         hasNext,
//         isLoading: loading,
//         threshold: 0.25, // load earlier
//         prefetch: true,
//         debug: true,
//     })

//     // 3. Store API
//     return {
//         // state
//         products,
//         loading,
//         error,
//         hasNext,
//         nextCursor,
//         count,

//         // actions
//         fetchFirst,
//         loadMore,
//         reset,
//         forceReload,

//         // infinite scroll refs
//         sentinelRef,
//         bindSentinel,
//         unbindSentinel,
//     }
// })



// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { getProducts } from "~/services/api/products"

// export const useProductStore = defineStore("productStore", () => {
//     const products = ref([])
//     const products_data = ref([])
//     const loading = ref(false)
//     const error = ref(null)
//     const nextCursor = ref(null)
//     const hasNext = ref(true)

//     const reset = () => {
//         products.value = []
//         nextCursor.value = null
//         hasNext.value = true
//         error.value = null
//     }

//     const fetchFirst = async (params = {}) => {
//         loading.value = true
//         error.value = null
//         try {
//             const { data, status } = await getProducts(params)
//             products.value = data.products || []
//             products_data.value = data.data.products || []
//             nextCursor.value = data.next_cursor ?? null
//             hasNext.value = !!data.has_next || nextCursor.value !== null
//         } catch (err) {
//             error.value = err
//         } finally {
//             loading.value = false
//         }
//     }
//     console.log('inside productStore with data.products ', products.value);
//     console.log('inside productStore with data.data.products ', products_data.value);

//     const loadMore = async (params = {}) => {
//         if (!hasNext.value || loading.value) return
//         loading.value = true
//         error.value = null
//         try {
//             const requestParams = { ...params }
//             if (nextCursor.value) requestParams.cursor = nextCursor.value
//             const { data } = await getProducts(requestParams)
//             const newItems = data.products || []
//             // append with dedupe by 'id'
//             const map = new Map(products.value.map(p => [p.id, p]))
//             for (const item of newItems) map.set(item.id, item)
//             products.value = Array.from(map.values())
//             nextCursor.value = data.next_cursor ?? null
//             hasNext.value = !!data.has_next || nextCursor.value !== null
//         } catch (err) {
//             error.value = err
//         } finally {
//             loading.value = false
//         }
//     }

//     return {
//         products,
//         loading,
//         error,
//         nextCursor,
//         hasNext,
//         fetchFirst,
//         loadMore,
//         reset,
//     }
// })



// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia"
// import { ref } from "vue"
// import { getProducts } from "~/services/api/products"
// import { normalizeResponse } from "~/services/helpers/response"

// export const useProductStore = defineStore("productStore", () => {
//     const products = ref([])
//     const loading = ref(false)
//     const error = ref(null)
//     const nextCursor = ref(null)
//     const hasNext = ref(true)

//     const reset = () => {
//         products.value = []
//         nextCursor.value = null
//         hasNext.value = true
//         error.value = null
//     }

//     const fetchFirst = async (params = {}) => {
//         reset()
//         loading.value = true
//         try {
//             const response = await getProducts(params)
//             console.warn("API Respone Info:", response)
//             const { data, errors, info } = normalizeResponse(response)

//             if (errors) throw errors
//             if (info) console.warn("API Info:", info)

//             console.log(`✅ API call successful. Loaded ${data.products.length} products.`)

//             products.value = data.products
//             nextCursor.value = data.pagination?.next_cursor ?? null
//             hasNext.value = data.pagination?.has_next ?? false
//         } catch (err) {
//             console.error("❌ Product fetch error:", err)
//             error.value = err
//         } finally {
//             loading.value = false
//         }
//     }

//     const loadMore = async (params = {}) => {
//         if (!hasNext.value || loading.value) return
//         loading.value = true
//         try {
//             const requestParams = { ...params }
//             if (nextCursor.value) requestParams.cursor = nextCursor.value

//             const response = await getProducts(requestParams)
//             const { data, errors, info } = normalizeResponse(response)

//             if (errors) throw errors
//             if (info) console.warn("API Info:", info)

//             const newItems = data.products

//             // Append with dedupe by 'id'
//             const map = new Map(products.value.map(p => [p.id, p]))
//             for (const item of newItems) map.set(item.id, item)
//             products.value = Array.from(map.values())

//             nextCursor.value = data.pagination?.next_cursor ?? null
//             hasNext.value = data.pagination?.has_next ?? false

//             console.log(`✅ Loaded more products. Total now: ${products.value.length}`)
//         } catch (err) {
//             console.error("❌ Load more error:", err)
//             error.value = err
//         } finally {
//             loading.value = false
//         }
//     }

//     return {
//         products,
//         loading,
//         error,
//         nextCursor,
//         hasNext,
//         fetchFirst,
//         loadMore,
//         reset,
//     }
// })

// // ~/stores/modules/productStore.js
// import { defineStore } from "pinia";
// import { ref } from "vue";
// import { getProducts } from "~/services/api/products";

// export const useProductStore = defineStore("productStore", () => {
//     const products = ref([]);
//     const loading = ref(false);
//     const error = ref(null);
//     const nextCursor = ref(null);
//     const hasNext = ref(true);

//     // 🔄 Reset state
//     const reset = () => {
//         products.value = [];
//         nextCursor.value = null;
//         hasNext.value = true;
//         error.value = null;
//         console.log("🔄 Product store reset");
//     };

//     // 📥 First fetch
//     const fetchFirst = async (params = {}) => {
//         reset();
//         loading.value = true;

//         try {
//             const response = await getProducts(params);
//             console.warn("🍍 API Response Info:", response);

//             console.log('productStore Response Type Before NarmalizeResponse ', response);
//             const { data, errors, meta } = response;
//             console.log('productStore Response Type After NarmalizeResponse Data ', data);

//             if (errors) throw errors;


//             products.value = data;
//             nextCursor.value = meta?.next_cursor ?? null;
//             hasNext.value = meta?.has_next ?? false;
//         } catch (err) {
//             console.error("❌ Product fetch error:", err);
//             error.value = err;
//         } finally {
//             loading.value = false;
//         }
//     };

//     // ➕ Load more (cursor-based pagination)
//     const loadMore = async (params = {}) => {
//         if (!hasNext.value) {
//             console.log("⚠️ No more products to load");
//             return;
//         }
//         if (loading.value) {
//             console.log("⏳ Already loading products, skipping loadMore call");
//             return;
//         }

//         loading.value = true;

//         try {
//             const requestParams = { ...params };
//             if (nextCursor.value) requestParams.cursor = nextCursor.value;

//             const response = await getProducts(requestParams);
//             console.warn("🍍 LoadMore API Response Info:", response);

//             const { data, errors, meta } = response;

//             if (errors) throw errors;

//             const newProducts = Array.isArray(data) ? data : data ? [data] : [];
//             console.log(`🔹 Loaded ${newProducts.length} new products`);

//             // ✅ Deduplicate by `id`
//             const map = new Map(products.value.map(p => [p.id, p]));
//             for (const item of newProducts) map.set(item.id, item);
//             products.value = Array.from(map.values());

//             nextCursor.value = meta?.next_cursor ?? null;
//             hasNext.value = meta?.has_next ?? false;

//             console.log(
//                 `✅ Total products after loadMore: ${products.value.length}`
//             );
//         } catch (err) {
//             console.error("❌ Load more error:", err);
//             error.value = err;
//         } finally {
//             loading.value = false;
//         }
//     };

//     return {
//         products,
//         loading,
//         error,
//         nextCursor,
//         hasNext,
//         fetchFirst,
//         loadMore,
//         reset,
//     };
// });



// ~/stores/modules/productStore.js
import { defineStore } from "pinia"
import { ref } from "vue"
import { getProducts } from "~/services/api/products"

export const useProductStore = defineStore("productStore", () => {
    const products = ref([])
    const loading = ref(false)
    const error = ref(null)
    const nextCursor = ref(null)
    const hasNext = ref(true)

    // 🔄 Reset state
    const reset = () => {
        products.value = []
        nextCursor.value = null
        hasNext.value = true
        error.value = null
        console.log("🔄 Product store reset")
    }

    // 📥 First fetch
    const fetchFirst = async (params = {}) => {
        reset()
        loading.value = true

        const response = await getProducts(params)

        if (!response.success) {
            error.value = response.errors || [{ message: response.message }]
            loading.value = false
            return response
        }

        products.value = response.data || []
        nextCursor.value = response.meta?.next_cursor ?? null
        hasNext.value = response.meta?.has_next ?? false
        loading.value = false

        console.log(`✅ Initial load: ${products.value.length} products`)
        return response
    }

    // ➕ Load more (cursor-based pagination)
    const loadMore = async (params = {}) => {
        if (!hasNext.value) {
            console.log("⚠️ No more products to load")
            return
        }
        if (loading.value) {
            console.log("⏳ Already loading, skipping loadMore")
            return
        }

        loading.value = true

        const requestParams = { ...params }
        if (nextCursor.value) requestParams.cursor = nextCursor.value

        const response = await getProducts(requestParams)
        console.log('load More calling her ', response);
        if (!response.success) {
            error.value = response.errors || [{ message: response.message }]
            loading.value = false
            return response
        }

        const newProducts = Array.isArray(response.data)
            ? response.data
            : response.data
                ? [response.data]
                : []

        // ✅ Deduplicate by `id`
        const map = new Map(products.value.map(p => [p.id, p]))
        for (const item of newProducts) map.set(item.id, item)
        products.value = Array.from(map.values())

        nextCursor.value = response.meta?.next_cursor ?? null
        hasNext.value = response.meta?.has_next ?? false

        loading.value = false
        console.log(`✅ Total products: ${products.value.length}`)

        return response
    }

    return {
        products,
        loading,
        error,
        nextCursor,
        hasNext,
        fetchFirst,
        loadMore,
        reset,
    }
})
