# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
<!-- // https://collectionapi.metmuseum.org/public/collection/v1/departments -->

## aliexpressclone nuxt3 frontend with drf api composition api style
nuxt3-frontend/
│
├── assets/                                      # Static assets like CSS, fonts, images
│   ├── css/
│   │   ├── main.css                             # Tailwind + global styles
│   │   └── components/                          # Component-specific styles
│   └── images/                                  # Static images/icons
│
├── components/                                 # Reusable Vue UI components
│   ├── ui/                                     # Generic UI
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Select.vue
│   │   └── Pagination.vue
│   │
│   ├── layout/                                 # Layout primitives
│   │   ├── Header.vue
│   │   ├── Footer.vue
│   │   ├── Sidebar.vue
│   │   └── Navbar.vue
│   │
│   ├── product/                                # Product-related components
│   │   ├── ProductCard.vue
│   │   ├── ProductList.vue
│   │   ├── ProductDetails.vue
│   │   └── ProductImageGallery.vue
│   │
│   └── category/                               # Categories
│       ├── CategoryList.vue
│       ├── CategoryFilter.vue
│       └── CategorySidebar.vue
│
├── composables/                                # Auto-imported reusable logic
    products/
        useInfiniteProducts.js
│   ├── cache/
│   │   ├── LRUCache.js
│   │   └── useSearchCache.js
│   │
│   ├── debounce/
│   │   └── useDebouncedSearch.js
│   │
│   ├── observer/
│   │   └── useObserverCore.js
│   │
│   ├── pagination/
│   │   ├── usePagination.js
│   │   ├── useObserver.js
│   │   └── useInfiniteScroll.js
│   │
│   ├── search/
│   │   ├── useBaseSearch.js
│   │   ├── useSearch.js
│   │   ├── useInfiniteSearch.js
│   │   └── useSearchFilters.js
│   │
│   ├── throttle/
│   │   └── useBaseThrottle.js
│   │
│   ├── useApi.js                              # DRF API wrapper
│   └── useAuth.js                             # JWT auth handling
│
├── layouts/                                    # Nuxt layouts
│   ├── default.vue                             # Main layout
│   └── auth.vue                                # Auth pages
│
├── middleware/                                 # Route guards
│   ├── auth.global.js                          # Require login
│   └── guest.global.js                         # Block logged-in users from auth pages
│
├── pages/                                      # Auto-generated Nuxt routes
│   ├── index.vue                               # Home
│   ├── login.vue                               # Login
│   ├── register.vue                            # Register
│   ├── products/
│   │   ├── index.vue                           # Product listing
│   │   └── [id].vue                            # Product details
│   ├── categories/
│   │   ├── index.vue
│   │   └── [slug].vue
│   ├── cart.vue
│   ├── orders.vue
│   └── wishlist.vue
│
├── plugins/                                    # Nuxt plugins
│   ├── axios.js                                # Axios wrapper for DRF
│   ├── toast.js                                # Toast/notification plugin
│   └── dayjs.js                                # Date formatting helper
        api.client.js
        auth-init.client.js
        fetch-retry.js
│
├── services/                                   # External integrations
│   └── api/                                    # DRF API modules
│       ├── auth.js
│       ├── products.js
│       ├── categories.js
│       ├── cart.js
│       ├── orders.js
│       └── wishlist.js
│
├── stores/                                     # Pinia stores
│   ├── modules/                                # Domain modules composition api style
                authStore.js
                cartStore.js
                orderStore.js
                productStore.js
                wishlistStore.js

│   └── notifications/
│   │       ├── index.js
│   │       ├── state.js
│   │       ├── getters.js
│   │       ├── actions.js
│   │       └── mutations.js
│   │
│   └── search/                                # Global search state
│       ├── products/
│       │   ├── index.js
│       │   ├── state.js
│       │   ├── getters.js
│       │   ├── actions.js
│       │   └── mutations.js
│       ├── users/
│       │   ├── index.js
│       │   ├── state.js
│       │   ├── getters.js
│       │   ├── actions.js
│       │   └── mutations.js
│       └── categories/
│           ├── index.js
│           ├── state.js
│           ├── getters.js
│           ├── actions.js
│           └── mutations.js
│
├── utils/                                      # Helpers/utilities
│   ├── fuzzySearch.js
│   └── moneyFormatter.js
│
├── public/                                     # Static files served as-is
│
├── nuxt.config.ts
├── tailwind.config.js
└── package.json




## aliexpressclone nuxt3 frontend with drf api composition api style *** New Way ***
nuxt3-frontend/
│
├── modules/                                     # Feature-first organization
│   ├── auth/
│   │   ├── login.vue
│   │   └── register.vue
│   │   └── profile.vue
│   │
│   ├── products/
│   │   ├── index.vue
│   │   └── [id].vue
│   │
│   ├── products/
│   │   ├── index.vue
│   │   └── [slug].vue
│   ├── cart/
│   │   └── cart.vue
│   ├── orders/
│   │   └── orders.vue
│   ├── wishlist/
│   │   └── wishlist.vue
│   │
│   └── search/                                 # Dedicated search module
│       ├── store/
│       │   ├── productSearch.js
│       │   ├── userSearch.js
│       │   └── categorySearch.js
│       ├── composables/
│       │   ├── useBaseSearch.js
│       │   ├── useInfiniteSearch.js
│       │   └── useSearchFilters.js
│       └── components/
│           └── SearchDropdown.vue
│
├── components/                                 # Global (non-domain) components
│   ├── ui/                                     # Reusable UI library
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Select.vue
│   │   └── Pagination.vue
│   └── common/                                 # Layout primitives
│       ├── Header.vue
│       ├── Footer.vue
│       ├── Sidebar.vue
│       └── Navbar.vue
│
├── composables/                                # Global/core composables
│   ├── core/
│   │   ├── useApi.js
│   │   ├── useObserver.js
│   │   ├── useInfiniteScroll.js
│   │   ├── useDebouncedSearch.js
│   │   └── useBaseThrottle.js
│   └── cache/
│       ├── LRUCache.js
│       └── useSearchCache.js
│
├── layouts/
│   ├── default.vue
│   └── auth.vue
│
├── middleware/
│   ├── auth.global.js
│   └── guest.global.js
│
├── plugins/
│   ├── core/
│   │   ├── axios.js
│   │   └── fetch-retry.js
│   ├── integrations/
│   │   ├── toast.js
│   │   └── dayjs.js
│   └── auth/
│       ├── api.client.js
│       └── auth-init.client.js
│
├── utils/
│   ├── format/
│   │   └── moneyFormatter.js
│   └── search/
│       └── fuzzySearch.js
│
├── public/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── nuxt.config.ts
├── tailwind.config.js
└── package.json
