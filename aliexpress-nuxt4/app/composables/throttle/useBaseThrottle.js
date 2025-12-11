/**
 * useBaseThrottle
 * ----------------------------
 * A production-ready throttle composable for Nuxt 3.
 * - Works with sync and async functions
 * - Cancel pending calls
 * - Leading/trailing edge control
 *
 * @param {Function} fn - Function to be throttled
 * @param {number} delay - Delay in ms (default: 300ms)
 * @param {Object} options
 * @param {boolean} options.leading - Trigger on leading edge (default: true)
 * @param {boolean} options.trailing - Trigger on trailing edge (default: true)
 *
 * @returns {Object} { run, cancel }
 */
export function useBaseThrottle(fn, delay = 300, options = {}) {
    const { leading = true, trailing = true } = options

    let lastCallTime = 0
    let timeoutId = null
    let lastArgs = null
    let lastThis = null

    const run = function (...args) {
        const now = Date.now()

        if (!lastCallTime && !leading) {
            lastCallTime = now
        }

        const remaining = delay - (now - lastCallTime)
        lastArgs = args
        lastThis = this

        if (remaining <= 0 || remaining > delay) {
            if (timeoutId) {
                clearTimeout(timeoutId)
                timeoutId = null
            }
            lastCallTime = now
            fn.apply(lastThis, lastArgs)
            lastArgs = lastThis = null
        } else if (!timeoutId && trailing) {
            timeoutId = setTimeout(() => {
                lastCallTime = leading ? Date.now() : 0
                timeoutId = null
                fn.apply(lastThis, lastArgs)
                lastArgs = lastThis = null
            }, remaining)
        }
    }

    const cancel = () => {
        if (timeoutId) {
            clearTimeout(timeoutId)
            timeoutId = null
        }
        lastCallTime = 0
        lastArgs = lastThis = null
    }

    return { run, cancel }
}
