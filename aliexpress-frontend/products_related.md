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


### working on it ( Best ever )
✅ Why this works better

useApi = generic HTTP (never changes).

productService = knows about API shape (data.products, data.pagination).

store = manages state, error/loading, delegates to service.

usePagination = UI logic only (page state, next/prev).

Components = dumb consumers of store + composables.


┌─────────────────────────┐
│       Component         │
│-------------------------│
│ - binds to productStore │
│ - binds scroll event    │
│ - calls store.loadMore()│
└─────────▲───────────────┘
          │
          │
          │ uses reactive state
          │ products, loading, error
          │
┌─────────┴───────────────┐
│      productStore        │
│--------------------------│
│ - keeps products[]       │
│ - keeps nextCursor       │
│ - keeps hasNext          │
│ - fetchFirst()           │
│ - loadMore()             │
└─────────▲───────────────┘
          │ delegates
          │ to service
          │
┌─────────┴───────────────┐
│    productService        │
│--------------------------│
│ - knows API response     │    not using helper/response_fetctory
│   shape (data.products,  │
│   data.pagination)       │
│ - wraps useApi call      │
│ - normalizes data        │
└─────────▲───────────────┘
          │
          │ makes HTTP request
          │
┌─────────┴──────────────-----─┐
│Composable ( useApi / Base )     │
│--------------------------│
│ - generic fetch wrapper  │
│ - handles retries        │
│ - circuit breaker        │
│ - token refresh          │
│ - returns { data, error }│
└─────────────────────────┘
          |
        Axios

Add rate limiting: don’t fire loadMore multiple times at once.






🔹 Key Idea

useApi = fetcher only

usePagination = reusable cursor-based logic

productStore = domain brain 🧠 (owns infinite scroll + products state)

Components = only render 📺

So your components don’t import useInfiniteScroll anymore.
They just ref="productStore.sentinelRef" → store handles everything.