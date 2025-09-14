# 🌐 E-Commerce Frontend Wireframes

---

# 🏠 Homepage

<details>
<summary>Components</summary>

### HeroBanner
- Props: `banners: Array<{id, image, link}>`
- Events: `onClickBanner(link)`
- Notes: Rotating banner with CTA buttons.

### FeaturedProducts
- Props: `products: Product[]`
- Events: `onClickProduct(id)`
- Notes: Carousel of featured products.

### QuickCategoryLinks
- Props: `categories: Category[]`
- Events: `onClickCategory(id)`
- Notes: Quick links to top categories.

### HomepageLayout
- Uses: `HeroBanner`, `FeaturedProducts`, `QuickCategoryLinks`
- States: `loading: boolean`, `error: string|null`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/home/featured/` → fetch banners & featured products  
- `GET /api/v1/home/categories/` → fetch top-level categories  

</details>

---

# 📂 Category Page

<details>
<summary>Components</summary>

### CategoryList
- Props: `categories: Category[]`
- Events: `onClickCategory(id)`
- Notes: Tree-view of categories.

### ProductGrid
- Props: `products: Product[]`
- Events: `onClickProduct(id)`, `onAddToCart(productId, variantId)`
- Notes: Grid with filters & pagination.

### FiltersSidebar
- Props: `filters: {brand[], priceRange, color[], size[]}`
- Events: `onFilterChange(filters)`

### CategoryLayout
- Uses: `CategoryList`, `FiltersSidebar`, `ProductGrid`
- States: `selectedCategory: Category|null`, `filters: FiltersState`, `loading: boolean`, `products: Product[]`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/categories/` → list all categories  
- `GET /api/v1/categories/{id}/` → single category + subcategories  
- `GET /api/v1/categories/{id}/products/` → products inside category (supports filters & pagination)  

</details>

---

# 📦 Product Page

<details>
<summary>Components</summary>

### ProductGallery
- Props: `images: string[]`
- Notes: Main image + thumbnails.

### ProductDetails
- Props: `product: Product`
- Events: `onAddToCart(productId, variantId, quantity)`
- Notes: Show title, price, description, rating, stock.

### ProductVariants
- Props: `variants: Variant[]`
- Events: `onSelectVariant(variantId)`

### ProductAttributes
- Props: `attributes: Attribute[]`

### ProductLayout
- Uses: `ProductGallery`, `ProductDetails`, `ProductVariants`, `ProductAttributes`
- States: `selectedVariant: Variant|null`, `quantity: number`, `loading: boolean`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/products/` → list all products  
- `GET /api/v1/products/{id}/` → full product detail  
- `GET /api/v1/products/{id}/variants/` → variants  
- `GET /api/v1/products/{id}/attributes/` → product attributes  

</details>

---

# 🛒 Cart Page

<details>
<summary>Components</summary>

### CartItemCard
- Props: `item: CartItem`
- Events: `onUpdateQuantity(itemId, quantity)`, `onRemove(itemId)`

### CartSummary
- Props: `items: CartItem[]`
- Notes: Shows subtotal, taxes, total.

### CartLayout
- Uses: `CartItemCard`, `CartSummary`
- States: `items: CartItem[]`, `loading: boolean`, `error: string|null`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/cart/` → fetch cart items  
- `POST /api/v1/cart/` → add item  
- `PATCH /api/v1/cart/{item_id}/` → update quantity  
- `DELETE /api/v1/cart/{item_id}/` → remove item  

</details>

---

# 💳 Checkout / Orders Page

<details>
<summary>Components</summary>

### CheckoutForm
- Props: `userAddress: Address|null`
- Events: `onSubmitCheckout(data)`

### OrderSummary
- Props: `items: CartItem[]`, `total: number`

### OrdersList
- Props: `orders: Order[]`
- Events: `onViewOrder(id)`

### OrderLayout
- Uses: `CheckoutForm`, `OrderSummary`, `OrdersList`
- States: `loading: boolean`, `error: string|null`, `orders: Order[]`

</details>

<details>
<summary>API Calls</summary>

- `POST /api/v1/checkout/` → start checkout  
- `POST /api/v1/orders/` → place order  
- `GET /api/v1/orders/` → list user orders  
- `GET /api/v1/orders/{id}/` → order details  

</details>

---

# 👤 User Page

<details>
<summary>Components</summary>

### UserProfile
- Props: `user: User`
- Events: `onUpdateProfile(data)`

### WishlistGrid
- Props: `products: Product[]`
- Events: `onRemoveWishlist(productId)`, `onClickProduct(id)`

### UserLayout
- Uses: `UserProfile`, `WishlistGrid`
- States: `user: User|null`, `wishlist: Product[]`, `loading: boolean`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/users/me/` → profile  
- `PATCH /api/v1/users/me/` → update profile  
- `GET /api/v1/users/me/orders/` → user orders  
- `GET /api/v1/users/me/wishlist/` → wishlist  
- `POST /api/v1/users/me/wishlist/` → add product  
- `DELETE /api/v1/users/me/wishlist/{product_id}/` → remove product  

</details>

---

# 🏷 Brands Page

<details>
<summary>Components</summary>

### BrandCard
- Props: `brand: Brand`
- Events: `onClickBrand(id)`

### BrandLayout
- Uses: `BrandCard`
- States: `brands: Brand[]`, `loading: boolean`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/brands/` → fetch all brands  
- `GET /api/v1/brands/{id}/` → brand details + products  

</details>

---

# 📊 Inventory Page (Admin)

<details>
<summary>Components</summary>

### InventoryTable
- Props: `items: Inventory[]`
- Events: `onUpdateStock(sku, quantity)`

### InventoryLayout
- Uses: `InventoryTable`
- States: `items: Inventory[]`, `loading: boolean`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/inventory/` → fetch stock overview  
- `PATCH /api/v1/inventory/{sku}/` → update stock  

</details>

---

# 🔍 Search Page

<details>
<summary>Components</summary>

### SearchBar
- Props: `query: string`
- Events: `onSearch(q)`

### SearchResultsGrid
- Props: `products: Product[]`
- Events: `onClickProduct(id)`

### SearchLayout
- Uses: `SearchBar`, `SearchResultsGrid`
- States: `query: string`, `results: Product[]`, `loading: boolean`

</details>

<details>
<summary>API Calls</summary>

- `GET /api/v1/search/` → search products, categories, brands  
  **Query params:** `?q=`, `?category=`, `?brand=`, `?sort=`

</details>