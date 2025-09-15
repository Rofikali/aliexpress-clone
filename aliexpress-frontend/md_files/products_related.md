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
│Composable ( Base )     │
│--------------------------│
│ - generic normalize response wrapper  │
└─────────────────────────┘
          |
        Axios
