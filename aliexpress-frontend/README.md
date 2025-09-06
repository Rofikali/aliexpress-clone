# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
<!-- // https://collectionapi.metmuseum.org/public/collection/v1/departments -->

## aliexpressclone nuxt3 frontend with drf api composition api style *** New Way ***
nuxt3-frontend/
│
├── app.vue
├── nuxt.config.js                  # use JS since your codebase is JS-only
│
├── pages/
│   ├── index.vue
│   ├── auth/
│   │   ├── login.vue
│   │   ├── register.vue
│   │   └── profile.vue
│   ├── products/
│   │   ├── index.vue               # list
│   │   └── [id]-[slug].vue         # detail (choose ONE dynamic file)
│   ├── cart.vue
│   ├── orders.vue
│   └── wishlist.vue
│
├── components/
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
├── stores/                         # Pinia (single source of truth)
│   ├── authStore.js
│   ├── productStore.js
│   └── search/
│       ├── product.js
│       ├── user.js
│       └── category.js
│
├── composables/
│   ├── core/
│   │   ├── useApi.js               # auth + retry + circuit breaker (you have this)
│   │   ├── useDebounce.js
│   │   └── useThrottle.js
│   ├── observer/
│   │   └── useObserverCore.js
│   ├── pagination/
│   │   ├── useInfiniteProductScroll.js  # integrates with productStore
│   │   └── useFillViewport.js
│   └── search/
│       ├── useBaseSearch.js
│       ├── useInfiniteSearch.js
│       └── useSearchFilters.js
│
├── plugins/
│   ├── api.client.js               # provides $api -> wraps useApi
│   ├── fetch-retry.client.js       # global $fetch retry/backoff (optional if $api everywhere)
│   ├── dayjs.client.js
│   └── toast.client.js
│
├── middleware/
│   ├── auth.global.js              # protect auth-only routes
│   └── guest.global.js             # redirect logged-in users away from login/register
│
├── utils/
│   ├── format/
│   │   └── money.js
│   └── search/
│       └── fuzzy.js
│
├── assets/
│   └── css/
│       └── main.css                # tailwind entry if you prefer
│
├── public/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── tailwind.config.js
└── package.json



🔑 Flow now looks like:
UI → Composable → Store → Service → API
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
