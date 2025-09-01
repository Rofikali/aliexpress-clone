# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
<!-- // https://collectionapi.metmuseum.org/public/collection/v1/departments -->

## aliexpressclone nuxt3 frontend with drf api
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
│   ├── modules/                                # Domain modules
│   │   ├── auth/                               # Authentication & user
│   │   │   ├── index.js
│   │   │   ├── state.js
│   │   │   ├── getters.js
│   │   │   ├── actions.js
│   │   │   └── mutations.js
│   │   │
│   │   ├── cart/                               # Shopping cart
│   │   │   ├── index.js
│   │   │   ├── state.js
│   │   │   ├── getters.js
│   │   │   ├── actions.js
│   │   │   └── mutations.js
│   │   │
│   │   ├── orders/
│   │   │   ├── index.js
│   │   │   ├── state.js
│   │   │   ├── getters.js
│   │   │   ├── actions.js
│   │   │   └── mutations.js
│   │   │
│   │   ├── products/
│   │   │   ├── index.js
│   │   │   ├── state.js
│   │   │   ├── getters.js
│   │   │   ├── actions.js
│   │   │   └── mutations.js
│   │   │
│   │   ├── categories/
│   │   │   ├── index.js
│   │   │   ├── state.js
│   │   │   ├── getters.js
│   │   │   ├── actions.js
│   │   │   └── mutations.js
│   │   │
│   │   ├── wishlist/
│   │   │   ├── index.js
│   │   │   ├── state.js
│   │   │   ├── getters.js
│   │   │   ├── actions.js
│   │   │   └── mutations.js
│   │   │
│   │   └── notifications/
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
