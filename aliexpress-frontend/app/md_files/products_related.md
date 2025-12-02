┌─────────────────────────┐
│       Component         │
│-------------------------│
│ - binds to productStore │
│ - binds scroll event    │ # with infinteScrollPagination Composable
│ - calls store.loadMore()
  - fetchFirst()
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
│ - knows API response     │     using helper/response_fetctory for normalization
│   shape (data.products,  │
│   data.pagination)       │
│ - wraps Base calls      │
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






Porducts Detail Flow

User opens Product Page
          │
          ▼
 ┌───────────────────────────────┐
 │  GET /products/{product_id}/  │
 │  → Product info (name, price, │
 │    category, description)     │
 └───────────────────────────────┘
          │
          ▼
User needs variants (color, size, etc.)
          │
          ▼
 ┌─────────────────────────────────────────────┐
 │  GET /products/{product_id}/variants/        │
 │  → All variants of this product              │
 │    (e.g. 128GB Black, 256GB Silver, …)       │
 └─────────────────────────────────────────────┘
          │
User selects one variant (e.g. 256GB Black)
          │
          ▼
 ┌──────────────────────────────────────────────────────────┐
 │  GET /products/{product_id}/variants/{variant_id}/attributes/ │
 │  → Attributes of this specific variant                     │
 │    (RAM = 8GB, Camera = 48MP, Warranty = 1 Year, …)        │
 └──────────────────────────────────────────────────────────┘
          │
          ▼
If user clicks a single attribute for details (rare case)
          │
          ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │  GET /products/{product_id}/variants/{variant_id}/attributes/{attribute_id}/ │
 │  → One attribute detail (e.g. Warranty → terms & conditions text)            │
 └─────────────────────────────────────────────────────────────────────────────┘
