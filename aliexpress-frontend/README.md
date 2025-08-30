# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
<!-- // https://collectionapi.metmuseum.org/public/collection/v1/departments -->

## aliexpressclone nuxt3 frontend with drf api
nuxt3-frontend/
│
├── utils/                                      # General utility functions
│   └── fuzzySearch.js                          # Simple fuzzy filter helper
│
├── composables/                                # Global reusable logic (auto-imported by Nuxt)
│   ├── cache/
│   │   ├── LRUCache.js                         # Updated cache with TTL + persistence
│   │   └── useSearchCache.js                   # Cache wrapper for search-specific logic
│   │
│   ├── debounce/
│   │   └── useDebouncedSearch.js               # Debounce helper for search inputs
│   │
│   ├── observer/
│   │   └── useObserverCore.js                  # IntersectionObserver logic
│   │
│   ├── pagination/
│   │   ├── usePagination.js                    # Pagination state & logic
│   │   ├── useObserver.js                      # Infinite scroll observer
│   │   └── useInfiniteScroll.js                # Infinite scrolling helper
│   │
│   ├── search/
│   │   ├── useBaseSearch.js                    # Base search using cache & concurrency guard
│   │   ├── useSearch.js                        # Simple search
│   │   ├── useInfiniteSearch.js                # Cursor-based infinite search
│   │   └── useSearchFilters.js                 # Manage filters/facets
│   │
│   ├── useThrottle.js                          # Throttle helper
│   ├── usePaginatedFetch.js                    # Universal fetch for paginated data
│   ├── useAuth.js                              # JWT authentication handler
│   ├── useApi.js                               # API fetch wrapper for DRF
│   └── useNotifications.js                     # Toast/alert system
│
├── stores/                                     # Pinia state stores
│   ├── searchStore/
│   │   ├── useProductSearchStore.js            # Product search
│   │   ├── useUserSearchStore.js               # User search
│   │   └── useCategorySearchStore.js           # Category search
│   │
│   ├── productStore.js                         # Product CRUD & listing
│   ├── categoryStore.js                        # Categories & filters
│   ├── cartStore.js                            # Shopping cart
│   ├── orderStore.js                           # Orders & tracking
│   └── authStore.js                            # Auth & user info
│
├── components/                                 # UI components
│   ├── ui/                                     # Reusable Tailwind UI elements
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Select.vue
│   │   └── Pagination.vue
│   │
│   ├── layout/                                 # Layout parts
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
    throttle
        useBaseThrottle.js
│
├── pages/                                      # Auto-generated Nuxt routes
│   ├── index.vue                               # Home
│   ├── login.vue                               # Login
│   ├── register.vue                            # Register
│   ├── products/
│   │   ├── index.vue                           # Product listing
│   │   └── [id].vue                            # Product detail
│   ├── categories/
│   │   ├── index.vue
│   │   └── [slug].vue
│   ├── cart.vue
│   └── orders.vue
│
├── layouts/                                    # App layouts
│   ├── default.vue                             # Main layout
│   └── auth.vue                                # Auth pages layout
│
├── assets/                                     # Styles, fonts, images
│   ├── css/
│   │   └── main.css                            # Tailwind & custom styles
│   └── images/
│
├── middleware/                                 # Route guards
│   ├── auth.global.js                          # Require login
│   └── guest.global.js                         # Block logged-in users from auth pages
│
├── plugins/                                    # Nuxt plugins
│   ├── axios.js                                # Axios instance (DRF)
│   ├── toast.js                                # Toast notifications
│   └── dayjs.js                                # Date formatting
│
├── public/                                     # Static files (favicon, robots.txt)
│
├── nuxt.config.ts
├── package.json
└── tailwind.config.js
