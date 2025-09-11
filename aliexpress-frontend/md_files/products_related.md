┌─────────────────────────┐
│       Component         │
│-------------------------│
│ - binds to productStore │
│ - binds scroll event    │ # with infinteScrollPagination Composable
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
│ - keeps nextCursor       │ # with basePagination Composable
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


🔹 Key Idea

useApi = fetcher only

usePagination = reusable cursor-based logic

productStore = domain brain 🧠 (owns infinite scroll + products state)

Components = only render 📺

So your components don’t import useInfiniteScroll anymore.
They just ref="productStore.sentinelRef" → store handles everything.
