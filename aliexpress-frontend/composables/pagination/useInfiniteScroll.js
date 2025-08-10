// ~/composables/pagination/useInfiniteScroll.js
import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * useInfiniteScroll
 * @param {Function} loadMoreFn - function to call to load more items
 * @param {Object} options - { root, rootMargin, threshold }
 * returns: { sentinelRef, observing, stop, start }
 */
export function useInfiniteScroll(loadMoreFn, options = {}) {
    const sentinelRef = ref(null)
    const observing = ref(false)
    let observer = null

    const root = options.root || null
    const rootMargin = options.rootMargin || '0px'
    const threshold = options.threshold ?? 0.1 // 10% visibility

    function onIntersect(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                loadMoreFn()
            }
        })
    }

    function start() {
        if (observer || !sentinelRef.value) return
        observer = new IntersectionObserver(onIntersect, { root, rootMargin, threshold })
        observer.observe(sentinelRef.value)
        observing.value = true
    }

    function stop() {
        if (!observer) return
        observer.disconnect()
        observer = null
        observing.value = false
    }

    onMounted(() => {
        // if sentinel exists, start observing
        if (sentinelRef.value) start()
    })

    onBeforeUnmount(() => {
        stop()
    })

    return {
        sentinelRef,
        observing,
        start,
        stop
    }
}
