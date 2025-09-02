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

Composable (useInfiniteScrollProducts): Handles viewport & triggers loading.

Store (productStore): Holds products, pagination state, errors.

Service (productService): Talks to API, no state.

Composable useApi: Handles auth, refresh token, base URL.

This is already a tiered, enterprise-style architecture —
UI ➝ Composables ➝ Store ➝ Service ➝ API ➝ Backend


🧩 Layer-by-Layer Explanation
1. UI Layer 
    (Pages & Components)

2. Composables
    Composables handle “how to interact with data”, not “where data comes from.”

3. Pinia Store (State Layer)
    Think of the store as the brain of the frontend. Composables and UI ask the store for data instead of calling APIs directly.

4. Service Layer (Transport Wrappers)
    Services = translators. They normalize raw API responses and provide a consistent contract to the store.

