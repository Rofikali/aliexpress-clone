// // ~/composables/pagination/useFillViewport.js
import { nextTick } from 'vue'

/**
 * Ensures the viewport is filled with content
 * (useful for large screens or initial load)
 *
 * @param {Function} loadMore  - async function to fetch more items
 * @param {Ref<Boolean>} hasNext - ref indicating if more items are available
 * @param {Object} opts - { maxLoops?: number, debug?: boolean }
 */
export function useFillViewport(loadMore, hasNext, opts = {}) {
    const maxLoops = opts.maxLoops ?? 10 // safety limit to avoid infinite loops

    const checkAndLoadUntilScrollable = async (loopCount = 0) => {
        const scrollHeight = document.documentElement.scrollHeight
        const clientHeight = document.documentElement.clientHeight

        if (opts.debug) {
            console.log(`[useFillViewport] loop=${loopCount} height=${scrollHeight}/${clientHeight}`)
        }

        if (scrollHeight <= clientHeight && hasNext.value && loopCount < maxLoops) {
            await loadMore()
            await nextTick()
            return checkAndLoadUntilScrollable(loopCount + 1)
        }
    }

    return {
        checkAndLoadUntilScrollable
    }
}
