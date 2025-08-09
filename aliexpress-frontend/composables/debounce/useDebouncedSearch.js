// composables/debounce/useDebouncedSearch.js
import { ref } from 'vue'

export function useDebouncedSearch(fetchFunction, delay = 300) {
    const isSearching = ref(false)
    const result = ref(null)
    let timeout

    const trigger = (query) => {
        clearTimeout(timeout)
        if (!query) {
            result.value = null
            isSearching.value = false
            return
        }

        isSearching.value = true
        timeout = setTimeout(async () => {
            try {
                const { data, error } = await fetchFunction(query)
                if (!error.value) {
                    result.value = data.value
                } else {
                    console.error('Search error:', error.value)
                }
            } finally {
                isSearching.value = false
            }
        }, delay)
    }

    return {
        result,
        isSearching,
        trigger
    }
}
