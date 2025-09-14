# 🌐 E-Commerce API Wireframes

---

# 🏠 Homepage APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/home/featured/` → Returns featured products, banners, and quick category links.  
- `GET /api/v1/home/categories/` → Returns top-level categories with subcategories.

</details>

<details>
<summary>📦 Models</summary>

### Homepage
| Field       | Type       | Notes                     |
|------------|-----------|---------------------------|
| id         | UUIDField | Primary key               |
| banner     | CharField | Banner image/title        |
| featured   | Boolean   | Is featured               |
| created_at | DateTime  | Auto timestamp            |
| updated_at | DateTime  | Auto timestamp            |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class HomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homepage
        fields = ["id", "banner", "featured"]
        read_only_fields = ["id"]
```

</details>

---

# 📂 Category APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/categories/` → List all categories in tree structure.  
- `GET /api/v1/categories/{id}/` → Retrieve a single category with subcategories.  
- `GET /api/v1/categories/{id}/products/` → List products inside a category.  
  **Query params:** `?brand=`, `?price_min=`, `?price_max=`, `?color=`, `?size=`, `?sort=`, `?page=`, `?page_size=`

</details>

<details>
<summary>📦 Models</summary>

### Category
| Field       | Type        | Notes                        |
|-------------|------------|-------------------------------|
| id          | UUIDField  | Primary key                  |
| name        | CharField  | Category name                |
| slug        | SlugField  | Unique, indexed              |
| description | TextField  | Optional                     |
| parent      | FK(self)   | Nullable, for subcategories |
| is_active   | Boolean    | Show/hide category           |
| created_at  | DateTime   | Auto timestamp               |
| updated_at  | DateTime   | Auto timestamp               |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description", "children"]
        read_only_fields = ["id", "children"]

    def get_children(self, obj):
        return CategorySerializer(obj.children.filter(is_active=True), many=True).data
```

</details>

---

# 📦 Product APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/products/` → List all products.  
  **Query params:** `?cursor=`, `?page_size=`, `?brand=`, `?category=`  

- `GET /api/v1/products/{id}/` → Retrieve full product detail.  

- `GET /api/v1/products/{id}/variants/` → Return product variants (size, color, SKU).  

- `GET /api/v1/products/{id}/attributes/` → Return product attributes/specifications.

</details>

<details>
<summary>📦 Models</summary>

### Product
| Field          | Type          | Notes                               |
|----------------|---------------|-------------------------------------|
| id             | UUIDField     | Primary key                          |
| title          | CharField     | Product title                        |
| slug           | SlugField     | Unique                               |
| description    | TextField     | Full description                     |
| sku            | CharField     | Unique                               |
| price          | Decimal(12,2) | Base price                            |
| discount_price | Decimal(12,2) | Nullable                             |
| currency       | CharField(3)  | Defaults "USD"                        |
| image          | ImageField    | Main product image                    |
| stock          | IntegerField  | Stock count                           |
| is_active      | BooleanField  | Show/hide product                     |
| rating         | FloatField    | Average rating                        |
| review_count   | IntegerField  | Number of reviews                     |
| seller         | FK(User)      | Linked seller                         |
| category       | FK(Category)  | Product category                      |
| brand          | FK(Brand)     | Nullable                              |
| created_at     | DateTime      | Auto timestamp                         |
| updated_at     | DateTime      | Auto timestamp                         |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, source="product_images", read_only=True)
    variants = ProductVariantSerializer(many=True, source="productvariant_set", read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "price", "image",
            "images", "category", "brand", "variants",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        if request:
            return request.build_absolute_uri(url)
        return f"{settings.MEDIA_URL}{url.lstrip('/')}"
```

</details>

---

# 🛒 Cart APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/cart/` → Get user's cart.  
- `POST /api/v1/cart/` → Add product/variant. Body: `{ "product_id": "", "variant_id": "", "quantity": 1 }`  
- `PATCH /api/v1/cart/{item_id}/` → Update quantity.  
- `DELETE /api/v1/cart/{item_id}/` → Remove item.

</details>

<details>
<summary>📦 Models</summary>

### CartItem
| Field       | Type        | Notes                         |
|-------------|------------|-------------------------------|
| id          | UUIDField  | Primary key                  |
| user        | FK(User)   | Owner of cart item           |
| product     | FK(Product)| Linked product               |
| variant     | FK(Variant)| Optional                     |
| quantity    | Integer    | Item quantity                |
| created_at  | DateTime   | Auto timestamp               |
| updated_at  | DateTime   | Auto timestamp               |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "variant", "quantity", "created_at", "updated_at"]
```

</details>

---

# 💳 Orders / Checkout APIs

<details>
<summary>Endpoints</summary>

- `POST /api/v1/checkout/` → Start checkout.  
- `POST /api/v1/orders/` → Place order after payment.  
- `GET /api/v1/orders/` → List user orders.  
- `GET /api/v1/orders/{id}/` → Order details (status, items, shipping info).

</details>

<details>
<summary>📦 Models</summary>

### Order
| Field        | Type        | Notes                     |
|--------------|------------|---------------------------|
| id           | UUIDField  | Primary key              |
| user         | FK(User)   | Order owner              |
| status       | CharField  | Pending / Completed      |
| total_amount | Decimal    | Total order price        |
| created_at   | DateTime   | Auto timestamp           |
| updated_at   | DateTime   | Auto timestamp           |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "user", "status", "total_amount", "items", "created_at", "updated_at"]
```

</details>

---

# 👤 User APIs

<details>
<summary>Endpoints</summary>

- `POST /api/v1/auth/register/` → Register user.  
- `POST /api/v1/auth/login/` → Login (JWT).  
- `POST /api/v1/auth/logout/` → Logout.  
- `GET /api/v1/users/me/` → Profile.  
- `PATCH /api/v1/users/me/` → Update profile.  
- `GET /api/v1/users/me/orders/` → List orders.  
- `GET /api/v1/users/me/wishlist/` → Wishlist.  
- `POST /api/v1/users/me/wishlist/` → Add product.  
- `DELETE /api/v1/users/me/wishlist/{product_id}/` → Remove product.

</details>

<details>
<summary>📦 Models</summary>

### User
| Field        | Type      | Notes               |
|--------------|----------|-------------------|
| id           | UUIDField| Primary key       |
| username     | CharField| Unique            |
| email        | EmailField| Unique           |
| password     | CharField| Hashed            |
| created_at   | DateTime | Auto timestamp    |
| updated_at   | DateTime | Auto timestamp    |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at", "updated_at"]
```

</details>

---

# 🏷 Brand APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/brands/` → List all brands.  
- `GET /api/v1/brands/{id}/` → Brand details + products.

</details>

<details>
<summary>📦 Models</summary>

### Brand
| Field       | Type        | Notes                |
|-------------|------------|--------------------|
| id          | UUIDField  | Primary key        |
| name        | CharField  | Brand name         |
| slug        | SlugField  | Unique              |
| description | TextField  | Optional            |
| is_active   | Boolean    | Show/hide           |
| created_at  | DateTime   | Auto timestamp      |
| updated_at  | DateTime   | Auto timestamp      |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug", "description"]
```

</details>

---

# 📊 Inventory APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/inventory/` → Stock overview.  
- `PATCH /api/v1/inventory/{sku}/` → Update stock (restock, return, adjust).

</details>

<details>
<summary>📦 Models</summary>

### Inventory
| Field      | Type       | Notes                   |
|------------|-----------|------------------------|
| id         | UUIDField | Primary key            |
| product    | FK(Product)| Linked product         |
| sku        | CharField | Stock Keeping Unit      |
| quantity   | Integer   | Current stock           |
| updated_at | DateTime  | Auto timestamp          |

</details>

<details>
<summary>🛠 Serializers</summary>

```python
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "product", "sku", "quantity", "updated_at"]
```

</details>

---

# 🔍 Search APIs

<details>
<summary>Endpoints</summary>

- `GET /api/v1/search/` → Search products, categories, brands.  
  **Query params:** `?q=`, `?category=`, `?brand=`, `?sort=`

</details>

