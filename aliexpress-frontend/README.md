# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
<!-- // https://collectionapi.metmuseum.org/public/collection/v1/departments -->
nuxt3-frontend/
├── utils/
│   ├── cache/
│   │   ├── LRUCache.js   <-- The actual cache implementation
│
├── composables/                               # Global composables (Nuxt auto-imports)
│   ├── debounce/
│   │   └── useDebouncedSearch.js              # Reusable debounce for search inputs
        pagination
            usePagination.js
            useObserver.js
            useInfinitScroll.js
            
│   ├── search/                           # All search-related logic
│   │   ├── useSearch.js                  # Simple search (non-infinite)
│   │   ├── useInfiniteSearch.js          # Infinite search with cursor pagination
│   │   └── useSearchFilters.js           # Optional: manage filters/facets

        ~/composables/cache/LRUCache.js       // Updated with TTL + persistence
~/composables/cache/useSearchCache.js // Cache wrapper for search-specific logic
~/utils/fuzzySearch.js                // Simple fuzzy filter helper
~/composables/search/useBaseSearch.js // Updated to use new cache + parallel guard

│   ├── useThrottle.js                         # Reusable throttle composable
│   ├── usePaginatedFetch.js                   # Universal pagination logic (infinite scroll / page)
│   ├── useAuth.js                             # JWT auth helper composable (get/set/remove token)
│   ├── useApi.js                              # DRF API fetch wrapper (base URL, headers)
│   └── useNotifications.js                    # Toast/alert composable
│
├── stores/                                    # Pinia stores (scoped & modular)
│   ├── searchStore/
│   │   ├── useProductSearchStore.js           # Product search store
│   │   ├── useUserSearchStore.js              # User search store
│   │   └── useCategorySearchStore.js          # Category search store
│   │
│   ├── productStore.js                        # Product CRUD & listing
│   ├── categoryStore.js                       # Categories & filters
│   ├── cartStore.js                           # Shopping cart
│   ├── orderStore.js                          # Orders history & tracking
│   └── authStore.js                           # JWT login/logout & user info
│
├── components/                                # UI building blocks
│   ├── ui/                                    # Reusable Tailwind UI elements
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Select.vue
│   │   └── Pagination.vue
│   │
│   ├── layout/                                # Page layout parts
│   │   ├── Header.vue
│   │   ├── Footer.vue
│   │   ├── Sidebar.vue
│   │   └── Navbar.vue
│   │
│   ├── product/
│   │   ├── ProductCard.vue
│   │   ├── ProductList.vue
│   │   └── ProductDetails.vue
│   │
│   └── category/
│       ├── CategoryList.vue
│       └── CategoryFilter.vue
│
├── pages/                                     # Nuxt pages (routes auto-generated)
│   ├── index.vue                              # Home
│   ├── login.vue                              # Login page
│   ├── register.vue                           # Registration
│   ├── products/
│   │   ├── index.vue                          # Product listing
│   │   └── [id].vue                           # Product detail
│   ├── categories/
│   │   ├── index.vue
│   │   └── [slug].vue
│   ├── cart.vue
│   └── orders.vue
│
├── layouts/                                   # Global layouts
│   ├── default.vue                            # Default site layout
│   └── auth.vue                               # Auth pages layout
│
├── assets/                                    # Tailwind config, images, fonts
│   ├── css/
│   │   └── main.css                           # Tailwind import & custom styles
│   └── images/
│
├── middleware/                                # Nuxt route guards
│   ├── auth.global.js                         # Protect pages (check JWT)
│   └── guest.global.js                        # Prevent logged-in users from auth pages
│
├── plugins/                                   # Client/server plugins
│   ├── axios.js                               # Axios instance with DRF base URL
│   ├── toast.js                               # Toast notifications plugin
│   └── dayjs.js                               # Date formatting plugin
│
├── public/                                    # Static files (favicon, robots.txt, etc.)
│
├── nuxt.config.ts
├── package.json
└── tailwind.config.js
