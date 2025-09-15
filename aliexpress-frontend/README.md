# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
<!-- // https://collectionapi.metmuseum.org/public/collection/v1/departments -->

## aliexpressclone nuxt3 frontend with drf api composition api style *** New Way ***
nuxt3-frontend/
│
├── app.vue
├── nuxt.config.js                  # Nuxt configuration (JS only)
│
├── pages/                          # Route-driven views
│   ├── index.vue
│   ├── auth/
│   │   ├── login.vue
│   │   ├── register.vue
│   │   └── profile.vue
│   ├── products/
│   │   ├── index.vue               # product list
│   │   └── [id]-[slug].vue         # product detail
│   ├── cart.vue
│   ├── orders.vue
│   └── wishlist.vue
│
├── components/                     # Dumb UI components
         /products/      # Only product-related components
            detail/
               ProductGallery.vue     # Main product images (carousel/zoom)
               ProductThumbnail.vue   # Thumbnails selector
               ProductInfo.vue        # Title, price, stock, description
               ProductSpecs.vue       # Technical details/specs table
               ProductActions.vue     # Add to cart, wishlist, share, etc.
               ProductMeta.vue        # SKU, category, tags, etc.
               ProductTabs.vue        # Tabbed layout: Description / Reviews / Q&A
               ProductReviewList.vue  # Paginated reviews (uses usePagination)
               ProductReviewItem.vue  # Single review card
               ProductRelated.vue     # Related products carousel/grid
│   ├── common/
│   │   ├── Header.vue
│   │   ├── Footer.vue
│   │   ├── Sidebar.vue
│   │   └── Navbar.vue
│   └── ui/
│       ├── Button.vue
│       ├── Input.vue
│       ├── Select.vue
│       ├── Pagination.vue
│       └── SearchDropdown.vue
│
├── stores/                         # Pinia: centralized state
│   ├── authStore.js
│   ├── productStore.js
│   └── search/
│       ├── product.js
│       ├── user.js
│       └── category.js
│
├── composables/                    # Smart hooks (Composition API)
│   ├── core/
│   │   ├── base.js               # handleError(e) # authHeaders(token) 
│   ├── observer/
│   │   └── useObserverCore.js
│   ├── pagination/
│   │   ├── useBasePagination.js
│   │   └── useInfiniteScroll.js
│   └── search/
│       ├── useBaseSearch.js
│       ├── useInfiniteSearch.js
│       └── useSearchFilters.js
│
├── services/                       # API service layer (business logic)
│   └── api/
│       ├── auth.js                 # login, register, verify email
│       ├── cart.js
│       ├── products.js
│       ├── category.js
│       ├── orders.js
│       ├── wishlist.js
│       └── index.js                # export all services from here
│
├── plugins/                        # Nuxt app-level plugins
│   ├── axios.js               # inject $api from base
│
├── middleware/                     # Route guards
│   ├── auth.global.js              # block unauth users
│   └── guest.global.js             # block logged-in users from login/register
│
├── utils/                          # Pure utility functions
│   ├── format/
│   │   └── money.js
│   └── search/
│       └── fuzzy.js
│
├── assets/                         # Tailwind & static assets
│   └── css/
│       └── main.css
│
├── public/                         # static public files
│
├── tests/                          # Vitest / Playwright
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── tailwind.config.js
└── package.json


UI (pages/components)
   ▼
Composables (logic, hooks)
   ▼
Services (API calls → DRF)
   ▼
Stores (Pinia state management)
   ▼
Plugins/Middleware (auth, toast, utils)
   ▼
Backend (Django DRF)



🔑 Flow now looks like:
UI → Composable → Store → Service → API



Browser
   │
   ▼
Nuxt 3 Server/Client Boot
   │
   ▼
Plugins Run → $api, $toast, $dayjs
   │
   ▼
Pinia Store Init → authStore, productStore, etc.
   │
   ▼
Middleware Execution
   ├─ auth.global.js → check tokens, refresh, redirect
   └─ guest.global.js → redirect logged-in users away from login/register
   │
   ▼
Page Component Mounts
   │
   ▼
Composables / Services
   ├─ useApi() → API calls (DRF backend)
   ├─ useInfiniteProductScroll() → load products
   └─ useSearchFilters() → apply filters
   │
   ▼
Pinia Store Updates
   ├─ authStore.user populated
   ├─ productStore.list updated
   └─ cartStore updated
   │
   ▼
Components Render Reactively
   ├─ Header, Navbar → show user/cart info
   ├─ ProductList → infinite scroll
   └─ Cart/Wishlist → display current items
   │
   ▼
User Interaction → triggers actions → repeat composables/API → store → components
