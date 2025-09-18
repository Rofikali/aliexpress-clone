// ~/stores/modules/categoryStore.js
import { defineStore } from "pinia"
import { ref } from "vue"
import { useApi } from "~/composables/core/base"

export const useCategoryStore = defineStore("categoryStore", () => {
    const categories = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Pagination state
    const page = ref(1)
    const hasNext = ref(true)
    const pageSize = 12 // adjust if needed

    /**
     * Reset categories (e.g., on filter/search reset)
     */
    function resetCategories() {
        categories.value = []
        page.value = 1
        hasNext.value = true
    }

    /**
     * Fetch categories from backend
     */
    async function fetchCategories({ page: pageParam = 1 } = {}) {
        loading.value = true
        error.value = null
        try {
            const { data, status, error: fetchError } = await useApi(`/categories/?page=${pageParam}&page_size=${pageSize}`, {
                method: "GET",
            })

            if (status !== 200 || fetchError) {
                throw fetchError || new Error("Failed to fetch categories")
            }

            const results = data?.results || data?.categories || []
            const next = data?.next || null

            if (pageParam === 1) {
                categories.value = results
            } else {
                categories.value.push(...results)
            }

            hasNext.value = Boolean(next) && results.length > 0
            page.value = pageParam

        } catch (err) {
            console.error("fetchCategories failed:", err)
            error.value = err
        } finally {
            loading.value = false
        }
    }

    /**
     * Load next page for infinite scroll
     */
    async function loadMore() {
        if (!hasNext.value || loading.value) return
        await fetchCategories({ page: page.value + 1 })
    }

    return {
        categories,
        loading,
        error,
        page,
        hasNext,
        resetCategories,
        fetchCategories,
        loadMore,
    }
})
