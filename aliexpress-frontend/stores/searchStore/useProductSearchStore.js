// stores/searchStore/useProductSearchStore.js
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useDebouncedSearch } from '@/composables/debounce/useDebouncedSearch'

export const useProductSearchStore = defineStore('product-search', () => {
    const query = ref('')

    const { result, isSearching, trigger } = useDebouncedSearch(
        (q) => useFetch(`/api/products/search?query=${encodeURIComponent(q)}`),
        300
    )

    watch(query, (q) => trigger(q))

    return {
        query,
        result,
        isSearching,
        trigger
    }
})
