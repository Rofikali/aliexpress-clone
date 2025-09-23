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
│   ├── index.vue                   # Landing page
│   ├── auth/
│   │   ├── login.vue
│   │   ├── register.vue
│   │   └── profile.vue
│   ├── products/
│   │   ├── index.vue               # Product list
│   │   └── [id]-[slug].vue        # Product detail
│   ├── cart.vue
│   ├── orders.vue
│   ├── wishlist.vue

│   ├── index.vue               # Homepage main page
│       └── sections/               # Modular homepage sections
│           ├── HeroSection.vue
│           ├── FeaturedProducts.vue
│           ├── CategoriesSection.vue
│           ├── BannerSection.vue
│           └── Testimonials.vue
│
├── components/                     # Dumb UI components
│   ├── products/                   # Only product-related components
│   │   └── detail/
│   │       ├── ProductGallery.vue
│   │       ├── ProductThumbnail.vue
│   │       ├── ProductInfo.vue
│   │       ├── ProductSpecs.vue
│   │       ├── ProductActions.vue
│   │       ├── ProductMeta.vue
│   │       ├── ProductTabs.vue
│   │       ├── ProductReviewList.vue
│   │       ├── ProductReviewItem.vue
│   │       ├── ProductRelated.vue
│   │       ├── VariantSelection.vue
│   │       └── VariantAttributes.vue
│   │
│   ├── common/                     # Global layout components
│   │   ├── Header.vue
│   │   ├── Footer.vue
│   │   ├── Sidebar.vue
│   │   └── Navbar.vue
│   │
│   ├── ui/                         # Reusable UI elements
│   │   ├── Button.vue
│   │   ├── Input.vue
│   │   ├── Select.vue
│   │   ├── Pagination.vue
│   │   └── SearchDropdown.vue
│   │
│   └── homepage/                   # NEW: Homepage-specific components
│       ├── Hero.vue
│       ├── FeaturedProducts.vue
│       ├── Banner.vue
│       ├── Categories.vue
│       └── Testimonials.vue
│
├── stores/                          # Pinia: centralized state
│   ├── authStore.js
│   ├── productStore.js
│   ├── homepageStore.js            # NEW: Homepage state
│   └── search/
│       ├── product.js
│       ├── user.js
│       └── category.js
│
├── composables/                     # Smart hooks (Composition API)
│   ├── core/
│   │   └── base.js                 # handleError(e), authHeaders(token)
│   ├── observer/
│   │   └── useObserverCore.js
│   ├── pagination/
│   │   ├── useBasePagination.js
│   │   └── useInfiniteScroll.js
│   ├── search/
│   │   ├── useBaseSearch.js
│   │   ├── useInfiniteSearch.js
│   │   └── useSearchFilters.js
│   └── homepage/                   # NEW: Homepage hooks did not use it for now later i will 
│       ├── useHomepageData.js
│       └── useFeaturedProducts.js
│
├── services/                        # API service layer (business logic)
│   └── api/
│       ├── auth.js
│       ├── cart.js
│       ├── products.js
│       ├── category.js
│       ├── orders.js
│       ├── wishlist.js
│       └── homepage.js             # NEW: Homepage API
│       └── index.js                # Export all services
│
├── plugins/                         # Nuxt app-level plugins
│   └── axios.js                     # Inject $api
│
├── middleware/                      # Route guards
│   ├── auth.global.js               # Block unauthenticated users
│   └── guest.global.js              # Block logged-in users from login/register
│
├── utils/                           # Pure utility functions
│   ├── format/
│   │   └── money.js
│   ├── search/
│   │   └── fuzzy.js
│   └── homepage/                    # NEW: Homepage utilities
│       └── transformHomepageData.js
│
├── assets/                           # Tailwind & static assets
│   └── css/
│       └── main.css
│
├── public/                           # Static public files
│   └── images/homepage/             # NEW: banners, hero, category images
│
├── tests/                            # Vitest / Playwright
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
