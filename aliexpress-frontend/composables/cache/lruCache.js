// // ~/composables/cache/LRUCache.js
// export class LRUCache {
//     constructor(maxSize = 50, ttlMs = 0, persistKey = null) {
//         if (maxSize <= 0) throw new Error('LRUCache: maxSize must be > 0')
//         this.maxSize = maxSize
//         this.ttlMs = ttlMs
//         this.persistKey = persistKey
//         this.cache = new Map()

//         if (this.persistKey) this._loadFromStorage()
//     }

//     _now() {
//         return Date.now()
//     }

//     _isExpired(entry) {
//         return this.ttlMs > 0 && (this._now() - entry.timestamp) > this.ttlMs
//     }

//     get(key) {
//         const entry = this.cache.get(key)
//         if (!entry) return undefined
//         if (this._isExpired(entry)) {
//             this.delete(key)
//             return undefined
//         }
//         this.cache.delete(key)
//         this.cache.set(key, entry)
//         return entry.value
//     }

//     set(key, value) {
//         if (this.cache.has(key)) {
//             this.cache.delete(key)
//         } else if (this.cache.size >= this.maxSize) {
//             const oldestKey = this.cache.keys().next().value
//             this.cache.delete(oldestKey)
//         }
//         this.cache.set(key, { value, timestamp: this._now() })
//         this._saveToStorage()
//     }

//     has(key) {
//         const entry = this.cache.get(key)
//         if (!entry) return false
//         if (this._isExpired(entry)) {
//             this.delete(key)
//             return false
//         }
//         return true
//     }

//     delete(key) {
//         const deleted = this.cache.delete(key)
//         this._saveToStorage()
//         return deleted
//     }

//     clear() {
//         this.cache.clear()
//         this._saveToStorage()
//     }

//     size() {
//         return this.cache.size
//     }

//     _saveToStorage() {
//         if (!this.persistKey) return
//         try {
//             localStorage.setItem(this.persistKey, JSON.stringify([...this.cache.entries()]))
//         } catch (e) {
//             console.warn('[LRUCache] Failed to save to storage', e)
//         }
//     }

//     _loadFromStorage() {
//         try {
//             const raw = localStorage.getItem(this.persistKey)
//             if (!raw) return
//             const entries = JSON.parse(raw)
//             this.cache = new Map(entries)
//         } catch (e) {
//             console.warn('[LRUCache] Failed to load from storage', e)
//         }
//     }
// }

// ~/composables/cache/lruCache.js
export class LRUCache {
    constructor(maxSize = 50, ttlMs = 0, persistKey = null) {
        if (maxSize <= 0) throw new Error("LRUCache: maxSize must be > 0")
        this.maxSize = maxSize
        this.ttlMs = ttlMs
        this.persistKey = persistKey
        this.cache = new Map()

        if (this.persistKey && process.client) {
            this._loadFromStorage()
        }
    }

    _now() {
        return Date.now()
    }

    _isExpired(entry) {
        return this.ttlMs > 0 && this._now() - entry.timestamp > this.ttlMs
    }

    get(key) {
        const entry = this.cache.get(key)
        if (!entry) return undefined
        if (this._isExpired(entry)) {
            this.delete(key)
            return undefined
        }
        // refresh recency
        this.cache.delete(key)
        this.cache.set(key, entry)
        return entry.value
    }

    set(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key)
        } else if (this.cache.size >= this.maxSize) {
            const oldestKey = this.cache.keys().next().value
            this.cache.delete(oldestKey)
        }
        this.cache.set(key, { value, timestamp: this._now() })
        if (process.client) this._saveToStorage()
    }

    has(key) {
        const entry = this.cache.get(key)
        if (!entry) return false
        if (this._isExpired(entry)) {
            this.delete(key)
            return false
        }
        return true
    }

    delete(key) {
        const deleted = this.cache.delete(key)
        if (process.client) this._saveToStorage()
        return deleted
    }

    clear() {
        this.cache.clear()
        if (process.client) this._saveToStorage()
    }

    size() {
        return this.cache.size
    }

    _saveToStorage() {
        if (!this.persistKey || !process.client) return
        try {
            localStorage.setItem(
                this.persistKey,
                JSON.stringify([...this.cache.entries()])
            )
        } catch (e) {
            console.warn("[LRUCache] Failed to save to storage", e)
        }
    }

    _loadFromStorage() {
        if (!process.client) return
        try {
            const raw = localStorage.getItem(this.persistKey)
            if (!raw) return
            const entries = JSON.parse(raw)
            this.cache = new Map(entries)
        } catch (e) {
            console.warn("[LRUCache] Failed to load from storage", e)
        }
    }
}
