// ~/composables/useObserverCore.js
import { ref, onMounted, onBeforeUnmount, watch, isRef, nextTick } from 'vue'

// /**
//  * useObserverCore
//  * Production-ready IntersectionObserver engine
//  *
//  * Features:
//  * - lazy polyfill load (intersection-observer)
//  * - multi-target support (observe/unobserve)
//  * - debounce or throttle user callback
//  * - safe async callback invocation
//  * - start/stop/pause/resume lifecycle
//  *
//  * Returns:
//  * {
//  *   observe(node, opts), unobserve(node),
//  *   start(), stop(), pause(), resume(),
//  *   isRunning (ref)
//  * }
//  *
//  * observe(node, opts) accepts node or ref(node) and optional per-node options:
//  * { threshold, root, rootMargin, once, debounceMs, throttleMs, priority }
//  */
async function ensureObserverSupport() {
    if (typeof window !== 'undefined' && !('IntersectionObserver' in window)) {
        // dynamic import polyfill; package 'intersection-observer' must be added to deps if needed
        // webpack/nuxt will code-split this import
        await import('intersection-observer')
    }
}

function createDebounced(fn, ms) {
    if (!ms || ms <= 0) return fn
    let t = null
    return (...args) => {
        if (t) clearTimeout(t)
        t = setTimeout(() => { t = null; fn(...args) }, ms)
    }
}

function createThrottled(fn, ms) {
    if (!ms || ms <= 0) return fn
    let last = 0
    let t = null
    return (...args) => {
        const now = Date.now()
        const remaining = ms - (now - last)
        if (remaining <= 0) {
            if (t) { clearTimeout(t); t = null }
            last = now
            fn(...args)
        } else if (!t) {
            t = setTimeout(() => {
                last = Date.now()
                t = null
                fn(...args)
            }, remaining)
        }
    }
}

export function useObserverCore(globalOptions = {}) {
    const {
        defaultThreshold = 0.1,
        defaultRoot = null,
        defaultRootMargin = '0px',
        defaultDebounceMs = 0,
        defaultThrottleMs = 0,
        debug = false
    } = globalOptions

    const isClient = typeof window !== 'undefined' && !!window.IntersectionObserver
    const isRunning = ref(false)
    let observer = null
    const nodes = new Map() // node -> { callback, opts, wrappedHandler }

    // Choose the best callback wrapper based on node opts
    function wrapHandler(cb, { debounceMs = defaultDebounceMs, throttleMs = defaultThrottleMs } = {}) {
        let handler = async (entry) => {
            try {
                await cb(entry)
            } catch (err) {
                // swallow but surface in dev
                if (debug) console.error('[useObserverCore] callback error', err)
            }
        }
        // apply throttle then debounce (throttle has priority)
        handler = createThrottled(handler, throttleMs)
        handler = createDebounced(handler, debounceMs)
        return handler
    }

    async function createObserver() {
        if (!isClient) return
        if (observer) return

        await ensureObserverSupport()
        // use a single global observer; options vary per-node, so we observe and filter in callback
        observer = new IntersectionObserver((entries) => {
            // Prefer to process the most relevant entry first:
            // find first intersecting entry, else process all.
            const intersecting = entries.find(e => e.isIntersecting)
            if (intersecting) _dispatchEntry(intersecting)
            else {
                for (const e of entries) _dispatchEntry(e)
            }
        }, { root: defaultRoot, rootMargin: defaultRootMargin, threshold: defaultThreshold })

        // if nodes registered before creation, observe them
        for (const node of nodes.keys()) {
            try { observer.observe(node) } catch (e) { if (debug) console.warn('observe failed', e) }
        }
        isRunning.value = true
    }

    function _dispatchEntry(entry) {
        const node = entry.target
        const meta = nodes.get(node)
        if (!meta) return
        // If per-node threshold/root differ we don't recreate observer per-node (browser doesn't allow)
        // Instead we rely on global observer granularity and let per-node handler decide.
        // Only call handler if entry.intersectionRatio meets node's threshold if provided.
        const { opts, wrappedHandler } = meta
        const threshold = (opts && opts.threshold !== undefined) ? opts.threshold : defaultThreshold
        if (Array.isArray(threshold)) {
            // if any threshold <= intersectionRatio -> pass
            if (!threshold.some(t => entry.intersectionRatio >= t)) return
        } else {
            if (entry.intersectionRatio < threshold) return
        }
        // If node-level "once" already handled, skip
        wrappedHandler(entry)
        if (opts && opts.once && entry.isIntersecting) {
            unobserve(node)
        }
    }

    function observe(nodeOrRef, userCallback, nodeOptions = {}) {
        const node = isRef(nodeOrRef) ? nodeOrRef.value : nodeOrRef
        if (!node) {
            if (debug) console.warn('[useObserverCore] observe called with null node')
            return
        }
        if (!userCallback || typeof userCallback !== 'function') {
            throw new Error('observe requires a callback function')
        }
        const opts = {
            threshold: nodeOptions.threshold ?? defaultThreshold,
            root: nodeOptions.root ?? defaultRoot,
            rootMargin: nodeOptions.rootMargin ?? defaultRootMargin,
            once: nodeOptions.once ?? false,
            debounceMs: nodeOptions.debounceMs ?? defaultDebounceMs,
            throttleMs: nodeOptions.throttleMs ?? defaultThrottleMs,
            priority: nodeOptions.priority ?? 0
        }
        const wrappedHandler = wrapHandler(userCallback, opts)
        nodes.set(node, { callback: userCallback, opts, wrappedHandler })
        if (observer) {
            try { observer.observe(node) } catch (e) { if (debug) console.warn('observer.observe failed', e) }
        }
        // ensure observer exists
        createObserver().catch(err => { if (debug) console.error(err) })
    }

    function unobserve(nodeOrRef) {
        const node = isRef(nodeOrRef) ? nodeOrRef.value : nodeOrRef
        if (!node) return
        if (observer) {
            try { observer.unobserve(node) } catch (e) { if (debug) console.warn('observer.unobserve failed', e) }
        }
        nodes.delete(node)
    }

    function start() {
        if (!isClient) return
        createObserver()
    }

    function pause() {
        // pause by disconnecting observer but keep nodes map so we can resume
        if (observer) {
            try { observer.disconnect() } catch (e) { if (debug) console.warn('disconnect failed', e) }
            observer = null
        }
        isRunning.value = false
    }

    function resume() {
        if (!isClient) return
        createObserver()
    }

    function stop() {
        if (observer) {
            try { observer.disconnect() } catch (e) { if (debug) console.warn('disconnect failed', e) }
            observer = null
        }
        nodes.clear()
        isRunning.value = false
    }

    onMounted(() => {
        // create lazily if node observed; we do not auto-create to avoid unnecessary observers in SSR/hydration
        // but we can create if desired
    })

    onBeforeUnmount(() => {
        stop()
    })

    return {
        observe,
        unobserve,
        start,
        stop,
        pause,
        resume,
        isRunning,
        // expose internal state for diagnostics (debugging)
        _debug: () => ({ nodesCount: nodes.size })
    }
}
