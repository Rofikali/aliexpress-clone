BROWSER (UI)
─────────────────────────────
Components:

- ProductList.vue
- ProductCard.vue
- InfiniteScrollTrigger (div + sentinelRef)
- Header, Navbar, Cart, Wishlist
        │
        ▼
Nuxt 3 Page / Layout
- Mounted → calls composable/store
        │
        ▼
Pinia Store: productStore.js
─────────────────────────────
- products (reactive array)
- isLoading, error, hasNext
- loadMore() → triggers fetch
- reset(), reload() for filters/search
- fetchProductById(id)
- sentinelRef, bindSentinel, unbindSentinel
        │
        ▼
Composable: useInfiniteScrollProducts.js
─────────────────────────────
- Wraps generic createInfiniteScrollResource()
- fetchProducts(offset, pageSize) → calls getProducts()
- Handles cursor → page calculation
- Updates:
    • results → products array
    • next → hasNext
- Errors & loading state reactive
        │
        ▼
Composable: createInfiniteScrollResource.js
─────────────────────────────
- Generic infinite scroll logic:
    • items, isLoading, error, hasNext
    • loadMore() with sentinel ref
- Works for any resource (products, users, comments, etc.)
- Infinite scroll hook integration
        │
        ▼
Service: ~/services/api/products.js
─────────────────────────────
- getProducts({ page, page_size }) → useApi("/products/")
- Handles DRF pagination params
- Returns { data, error }
        │
        ▼
Composable: core/useApi.js
─────────────────────────────
- Base API wrapper:
    • Authorization headers
    • JWT access tokens
    • Circuit breaker / retry / exponential backoff
    • Returns { data, error, status }
- Backend-agnostic → works with any endpoint
        │
        ▼
DRF Backend: ProductsViewSet
─────────────────────────────
- Cursor pagination (BaseCursorPagination)
- Returns:
    {
        results: [...products],
        next: "<cursor-token>" | null,
        previous: "<cursor-token>" | null,
        count: total,
    }
- Caching layer for performance
- Handles single product retrieval
- Handles category, brand, variant, inventory, images
─────────────────────────────
Database
- Product, Category, Brand, Inventory, Attributes, Variants
- Optimized queries + indexes
- Cache (Redis/Memcached) for hot items
─────────────────────────────



┌───────────────────┐
│   useApi          │   <-- low-level HTTP (axios/fetch wrapper)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   usePagination   │   <-- generic cursor pagination (knows /products/?cursor=)
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  productStore     │   <-- combines usePagination + useInfiniteScroll
│                   │       - holds products state
│                   │       - manages infinite scroll
│                   │       - exposes sentinelRef
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│   Component       │   <-- dumb UI
│   - Renders list  │
│   - Uses store    │
│   - sentinel <div>│
└───────────────────┘
🔹 Key Idea

useApi = fetcher only

usePagination = reusable cursor-based logic

productStore = domain brain 🧠 (owns infinite scroll + products state)

Components = only render 📺

So your components don’t import useInfiniteScroll anymore.
They just ref="productStore.sentinelRef" → store handles everything.