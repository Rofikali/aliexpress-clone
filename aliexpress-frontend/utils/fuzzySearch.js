// ~/utils/fuzzySearch.js
export function fuzzySearch(items, searchTerm, fields = []) {
    if (!searchTerm) return items
    const term = searchTerm.toLowerCase()
    return items.filter(item =>
        fields.some(field => String(item[field] || '').toLowerCase().includes(term))
    )
}