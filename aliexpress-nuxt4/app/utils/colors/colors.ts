// Basic mapping for known color names → hex
export const COLOR_MAP: Record<string, string> = {
    red: "#ef4444",
    green: "#10b981",
    blue: "#3b82f6",
    black: "#000000",
    white: "#ffffff",
    yellow: "#facc15",
    purple: "#a855f7",
    gray: "#9ca3af",
}

// Detect hex
export function isHexColor(val: string) {
    return /^#([0-9A-F]{3}){1,2}$/i.test(val)
}

// Generic fallback name from hex (e.g. "#10b981" → "Greenish")
export function hexToApproxName(hex: string) {
    try {
        const c = hex.replace("#", "")
        const r = parseInt(c.substring(0, 2), 16)
        const g = parseInt(c.substring(2, 4), 16)
        const b = parseInt(c.substring(4, 6), 16)

        if (g > r && g > b) return "Greenish"
        if (r > g && r > b) return "Reddish"
        if (b > r && b > g) return "Bluish"
        return "Color"
    } catch {
        return "Color"
    }
}

// Convert admin value → proper color code
export function resolveColor(value: string) {
    if (!value) return "#ccc"

    const v = value.trim().toLowerCase()

    if (isHexColor(v)) return v
    if (COLOR_MAP[v]) return COLOR_MAP[v]

    // Browser supports many color names automatically
    return value
}
