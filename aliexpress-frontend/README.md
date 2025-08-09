# AliExpress Clone / (aliexpress-clone)

### Learn how to build this!
### Searching STORE with Reuseable Codebase
├── composables/
│   └── debounce/
│       └── useDebouncedSearch.js      # shared debounce composable for search
│   └── useThrottle.js                 # optional, throttling
│   └── usePaginatedFetch.js           # optional, pagination logic
│
├── stores/
│   └── searchStore/
│       ├── useProductSearchStore.js
│       ├── useUserSearchStore.js
│       └── useCategorySearchStore.js
// https://collectionapi.metmuseum.org/public/collection/v1/departments