normalizedResponse
        |
        ▼
    Services
        |
        ▼
    Stores
        |
        ▼
    Componensts ( Composables also would be there maybe )
        |
        ▼
    Page/UI 

### 🏗️ FINAL ARCHITECTURE (CLEAN) 

UI
 ├─ Add to Cart
 │    └─ cart/add_item
 │
 ├─ Buy Now
 │    ├─ cart/clear   (optional)
 │    ├─ cart/add_item
 │    └─ redirect → /checkout
 │
 └─ Checkout Page
      └─ POST /checkout/