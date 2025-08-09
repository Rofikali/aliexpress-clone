// stores/searchStore/useUserSearchStore.js
import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import { useDebouncedSearch } from '@/composables/debounce/useDebouncedSearch'

export const useUserSearchStore = defineStore('user-search', () => {
    const query = ref('')

    // const { result, isSearching, trigger } = useDebouncedSearch(
    //     (q) => useFetch(`/api/users/search?query=${encodeURIComponent(q)}`),
    //     300
    // )
    const { result, isSearching, trigger } = useDebouncedSearch(
        (q) => useFetch(`https://openlibrary.org/search.json?author=${encodeURIComponent(q)}`),
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
