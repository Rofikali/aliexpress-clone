// // composables/debounce/useDebouncedSearch.js
// import { ref } from 'vue'

// export function useDebouncedSearch(fetchFunction, delay = 300) {
//     const isSearching = ref(false)
//     const result = ref(null)
//     let timeout

//     const trigger = (query) => {
//         clearTimeout(timeout)
//         if (!query) {
//             result.value = null
//             isSearching.value = false
//             return
//         }

//         isSearching.value = true
//         timeout = setTimeout(async () => {
//             try {
//                 const { data, error } = await fetchFunction(query)
//                 if (!error.value) {
//                     result.value = data.value
//                 } else {
//                     console.error('Search error:', error.value)
//                 }
//             } finally {
//                 isSearching.value = false
//             }
//         }, delay)
//     }

//     return {
//         result,
//         isSearching,
//         trigger
//     }
// }


// ~/composables/debounce/useDebouncedSearch.js
import { ref, onBeforeUnmount } from 'vue'

/**
 * useDebouncedSearch
 * ---------------------------------
 * Universal debounce wrapper for async searches.
 * Handles:
 * - Canceling stale requests
 * - Reactive error/loading states
 * - Cleanup on unmount
 * - Works with Promise-based or Ref-returning fetchers
 *
 * @param {Function} fetchFunction - async (query) => { data, error }
 * @param {Number} delay - debounce delay in ms
 */
export function useDebouncedSearch(fetchFunction, delay = 300) {
    const result = ref(null)
    const isSearching = ref(false)
    const error = ref(null)

    let timeoutId
    let currentRequestId = 0 // prevents stale results overwriting new ones

    const trigger = (query) => {
        clearTimeout(timeoutId)

        if (query == null || query === '') {
            result.value = null
            error.value = null
            isSearching.value = false
            return
        }

        timeoutId = setTimeout(async () => {
            const requestId = ++currentRequestId
            isSearching.value = true
            error.value = null

            try {
                const maybeRefResult = await fetchFunction(query)

                // Unwrap if refs are returned
                const data = maybeRefResult?.data?.value ?? maybeRefResult?.data ?? maybeRefResult
                const fetchError = maybeRefResult?.error?.value ?? maybeRefResult?.error ?? null

                // Only update if this request is still the latest
                if (requestId === currentRequestId) {
                    if (fetchError) {
                        error.value = fetchError
                        result.value = null
                    } else {
                        result.value = data
                    }
                }
            } catch (err) {
                if (requestId === currentRequestId) {
                    error.value = err
                    result.value = null
                }
            } finally {
                if (requestId === currentRequestId) {
                    isSearching.value = false
                }
            }
        }, delay)
    }

    // Cleanup when component unmounts
    onBeforeUnmount(() => {
        clearTimeout(timeoutId)
        currentRequestId++
    })

    return {
        result,
        isSearching,
        error,
        trigger
    }
}
