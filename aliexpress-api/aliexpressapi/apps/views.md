Got it ✅ — you want a full .md documentation file for all the viewsets in products/api/viewsets.py, not just ProductsViewSet.

I’ll describe each ViewSet with:

Purpose

Endpoints (list/retrieve)

Response format

Caching (where applicable)

Simple flow diagram (only where it makes sense, like Products).

Here’s the full file:

# Products API – ViewSets Documentation

This document describes all the API **ViewSets** available in `products/api/viewsets.py`.  
Each section covers **purpose, endpoints, behavior, and responses**.

---

## 📦 Products

### `ProductsViewSet`
**Purpose:**  
Retrieve a **paginated list of products** with cursor-based pagination.  
Uses **caching** for better performance.

**Endpoints:**
- `GET /api/products/` → List all products (paginated, cached).
- `GET /api/products/{id}/` → Retrieve a single product by ID.

#### `list`
- Parameters:  
  - `cursor` (optional, string) – Cursor for pagination. Use `"first"` or empty for the first page.
- Behavior:
  1. Checks cache for the given cursor.  
  2. If cache hit → returns cached results.  
  3. If cache miss → queries DB, paginates, serializes, stores in cache.  
- Responses:  
  - `200 OK` – Paginated product list.  
  - `500 Internal Server Error` – Unexpected errors.

#### `retrieve`
- Parameters:  
  - `id` (path param) – Product ID.  
- Behavior:  
  1. Fetches product by ID.  
  2. Serializes and returns it.  
- Responses:  
  - `200 OK` – JSON object with product.  
  - `404 Not Found` – Product doesn’t exist.  
  - `400 Bad Request` – Error occurred.

**Flow (list):**
```mermaid
sequenceDiagram
    participant Client
    participant ViewSet as ProductsViewSet.list
    participant Cache as ProductCache
    participant DB as Database

    Client->>ViewSet: GET /api/products/?cursor=abc
    ViewSet->>Cache: get_results("abc")
    alt Cache hit
        Cache-->>ViewSet: Cached results
        ViewSet-->>Client: 200 OK
    else Cache miss
        ViewSet->>DB: Query Products
        DB-->>ViewSet: Product queryset
        ViewSet->>ViewSet: Paginate + Serialize
        ViewSet->>Cache: cache_results("abc", data)
        ViewSet-->>Client: 200 OK
    end

🏷️ Categories
CategoryViewSet

## 🏷️ Categories

### `CategoryViewSet`
**Purpose:**  
Retrieve product categories, either as a list or a single category.

**Endpoints:**
- `GET /api/categories/` → List all categories.
- `GET /api/categories/{id}/` → Retrieve a category by ID.

#### `list`
- Behavior:  
    1. Fetches all categories from the database, ordered by `created_at` descending.
    2. Serializes and returns the category list.
- Responses:  
    - `200 OK` – JSON array of categories.

#### `retrieve`
- Parameters:  
    - `id` (path param) – Category ID.
- Behavior:  
    1. Fetches category by ID.
    2. Serializes and returns the category.
- Responses:  
    - `200 OK` – JSON object with category.
    ---

    ## 🏢 Brands

    ### `BrandViewSet`
    **Purpose:**  
    Retrieve brands, either as a list or a single brand.

    **Endpoints:**
    - `GET /api/brands/` → List all brands.
    - `GET /api/brands/{id}/` → Retrieve a brand by ID.

    #### `list`
    - Behavior:  
        1. Fetches all brands from the database, ordered by `created_at` descending.
        2. Serializes and returns the brand list.
    - Responses:  
        - `200 OK` – JSON array of brands.

    #### `retrieve`
    - Parameters:  
        - `id` (path param) – Brand ID.
    - Behavior:  
        1. Fetches brand by ID.
        2. Serializes and returns the brand.
    - Responses:  
        - `200 OK` – JSON object with brand.
        - `404 Not Found` – Brand not found.

    ---

    ## 🖼️ Product Images

    ### `ProductImageViewSet`
    **Purpose:**  
    Retrieve product images, either as a list or a single image.

    **Endpoints:**
    - `GET /api/product-images/` → List all images.
    - `GET /api/product-images/{id}/` → Retrieve a single image by ID.

    #### `list`
    - Behavior:  
        1. Fetches all product images from the database.
        2. Serializes and returns the image list.
    - Responses:  
        - `200 OK` – JSON array of images.

    #### `retrieve`
    - Parameters:  
        - `id` (path param) – Image ID.
    - Behavior:  
        1. Fetches image by ID.
        2. Serializes and returns the image.
    - Responses:  
        - `200 OK` – JSON object with image.
        - `404 Not Found` – Image not found.

    ---

    ## 🔀 Product Variants

    ### `ProductVariantViewSet`
    **Purpose:**  
    Retrieve product variants, either as a list or a single variant.

    **Endpoints:**
    - `GET /api/variants/` → List all variants.
    - `GET /api/variants/{id}/` → Retrieve a single variant by ID.

    #### `list`
    - Behavior:  
        1. Fetches all product variants from the database.
        2. Serializes and returns the variant list.
    - Responses:  
        - `200 OK` – JSON array of variants.

    #### `retrieve`
    - Parameters:  
        - `id` (path param) – Variant ID.
    - Behavior:  
        1. Fetches variant by ID.
        2. Serializes and returns the variant.
    - Responses:  
        - `200 OK` – JSON object with variant.
        - `404 Not Found` – Variant not found.

    ---

    ## 🎛️ Product Attributes

    ### `ProductAttributeViewSet`
    **Purpose:**  
    Retrieve product attributes, either as a list or a single attribute.

    **Endpoints:**
    - `GET /api/attributes/` → List all attributes.
    - `GET /api/attributes/{id}/` → Retrieve a single attribute by ID.

    #### `list`
    - Behavior:  
        1. Fetches all product attributes from the database.
        2. Serializes and returns the attribute list.
    - Responses:  
        - `200 OK` – JSON array of attributes.

    #### `retrieve`
    - Parameters:  
        - `id` (path param) – Attribute ID.
    - Behavior:  
        1. Fetches attribute by ID.
        2. Serializes and returns the attribute.
    - Responses:  
        - `200 OK` – JSON object with attribute.
        - `404 Not Found` – Attribute not found.

    ---

    ## 📦 Inventory

    ### `InventoryViewSet`
    **Purpose:**  
    Retrieve inventory/stock records, either as a list or a single record.

    **Endpoints:**
    - `GET /api/inventory/` → List all inventory records.
    - `GET /api/inventory/{id}/` → Retrieve a stock entry by ID.

    #### `list`
    - Behavior:  
        1. Fetches all inventory records from the database.
        2. Serializes and returns the inventory list.
    - Responses:  
        - `200 OK` – JSON array of inventory records.

    #### `retrieve`
    - Parameters:  
        - `id` (path param) – Inventory record ID.
    - Behavior:  
        1. Fetches inventory record by ID.
        2. Serializes and returns the record.
    - Responses:  
        - `200 OK` – JSON object with inventory data.
        - `404 Not Found` – Inventory record not found.

    ---

---

## 🏷️ Categories

### `CategoryViewSet`

**Purpose:**  
Retrieve product categories (list and single).

**Endpoints:**
- `GET /api/categories/` — List all categories.
- `GET /api/categories/{id}/` — Retrieve a category by ID.

**Behavior:**
- **list:**  
    Fetch all categories, ordered by `created_at` (descending), serialize and return.
- **retrieve:**  
    Fetch category by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with category/categories.
- `404 Not Found` — Category not found.

---

## 🏢 Brands

### `BrandViewSet`

**Purpose:**  
Retrieve brands (list and single).

**Endpoints:**
- `GET /api/brands/` — List all brands.
- `GET /api/brands/{id}/` — Retrieve a brand by ID.

**Behavior:**
- **list:**  
    Fetch all brands, ordered by `created_at` (descending), serialize and return.
- **retrieve:**  
    Fetch brand by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with brand/brands.
- `404 Not Found` — Brand not found.

---

## 🖼️ Product Images

### `ProductImageViewSet`

**Purpose:**  
Retrieve product images (list and single).

**Endpoints:**
- `GET /api/product-images/` — List all images.
- `GET /api/product-images/{id}/` — Retrieve a single image by ID.

**Behavior:**
- **list:**  
    Fetch all product images, serialize and return.
- **retrieve:**  
    Fetch image by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with image(s).
- `404 Not Found` — Image not found.

---

## 🔀 Product Variants

### `ProductVariantViewSet`

**Purpose:**  
Retrieve product variants (list and single).

**Endpoints:**
- `GET /api/variants/` — List all variants.
- `GET /api/variants/{id}/` — Retrieve a single variant by ID.

**Behavior:**
- **list:**  
    Fetch all variants, serialize and return.
- **retrieve:**  
    Fetch variant by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with variant(s).
- `404 Not Found` — Variant not found.

---

## 🎛️ Product Attributes

### `ProductAttributeViewSet`

**Purpose:**  
Retrieve product attributes (list and single).

**Endpoints:**
- `GET /api/attributes/` — List all attributes.
- `GET /api/attributes/{id}/` — Retrieve a single attribute by ID.

**Behavior:**
- **list:**  
    Fetch all attributes, serialize and return.
- **retrieve:**  
    Fetch attribute by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with attribute(s).
- `404 Not Found` — Attribute not found.

---

## 📦 Inventory

### `InventoryViewSet`

**Purpose:**  
Retrieve inventory/stock records (list and single).

**Endpoints:**
- `GET /api/inventory/` — List all inventory records.
- `GET /api/inventory/{id}/` — Retrieve a stock entry by ID.

**Behavior:**
- **list:**  
    Fetch all inventory records, serialize and return.
- **retrieve:**  
    Fetch inventory record by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with inventory data.
- `404 Not Found` — Inventory record not found.

## 🏷️ Categories

### `CategoryViewSet`

**Purpose:**  
Retrieve product categories, either as a list or a single category.

**Endpoints:**
- `GET /api/categories/` — List all categories.
- `GET /api/categories/{id}/` — Retrieve a category by ID.

**Behavior:**
- **list:**  
    Fetch all categories, ordered by `created_at` (descending), serialize and return.
- **retrieve:**  
    Fetch category by ID, serialize and return.

**Responses:**
- `200 OK` — JSON array/object with category/categories.
- `404 Not Found` — Category not found.

---

### Endpoints

| ViewSet                   | List Endpoint                      | Retrieve Endpoint                      |
|---------------------------|------------------------------------|----------------------------------------|
| **ProductsViewSet**       | `GET /api/products/`               | `GET /api/products/{id}/`              |
| **CategoryViewSet**       | `GET /api/categories/`             | `GET /api/categories/{id}/`            |
| **BrandViewSet**          | `GET /api/brands/`                 | `GET /api/brands/{id}/`                |
| **ProductImageViewSet**   | `GET /api/product-images/`         | `GET /api/product-images/{id}/`        |
| **ProductVariantViewSet** | `GET /api/variants/`               | `GET /api/variants/{id}/`              |
| **ProductAttributeViewSet** | `GET /api/attributes/`           | `GET /api/attributes/{id}/`            |
| **InventoryViewSet**      | `GET /api/inventory/`              | `GET /api/inventory/{id}/`             |

---

## 📚 API ViewSets – Quick Reference

Below is a concise summary of all viewsets in `products/api/viewsets.py`, their endpoints, and behaviors.

### ProductsViewSet
- **Purpose:** List/retrieve products (paginated, cached).
- **Endpoints:**
    - `GET /api/products/` — Paginated product list (uses cache).
    - `GET /api/products/{id}/` — Retrieve single product.
- **Special:** Only this viewset uses caching and cursor-based pagination.

### CategoryViewSet
- **Purpose:** List/retrieve product categories.
- **Endpoints:**
    - `GET /api/categories/` — List all categories.
    - `GET /api/categories/{id}/` — Retrieve category by ID.

### BrandViewSet
- **Purpose:** List/retrieve brands.
- **Endpoints:**
    - `GET /api/brands/` — List all brands.
    - `GET /api/brands/{id}/` — Retrieve brand by ID.

### ProductImageViewSet
- **Purpose:** List/retrieve product images.
- **Endpoints:**
    - `GET /api/product-images/` — List all images.
    - `GET /api/product-images/{id}/` — Retrieve image by ID.

### ProductVariantViewSet
- **Purpose:** List/retrieve product variants.
- **Endpoints:**
    - `GET /api/variants/` — List all variants.
    - `GET /api/variants/{id}/` — Retrieve variant by ID.

### ProductAttributeViewSet
- **Purpose:** List/retrieve product attributes.
- **Endpoints:**
    - `GET /api/attributes/` — List all attributes.
    - `GET /api/attributes/{id}/` — Retrieve attribute by ID.

### InventoryViewSet
- **Purpose:** List/retrieve inventory records.
- **Endpoints:**
    - `GET /api/inventory/` — List all inventory records.
    - `GET /api/inventory/{id}/` — Retrieve inventory record by ID.

---

### ⚡️ Behavior & Responses

- **List endpoints:** Return all records (except Products, which is paginated and cached).
- **Retrieve endpoints:** Return single record by ID.
- **Responses:**  
    - `200 OK` — Success (JSON data).  
    - `404 Not Found` — Record not found.

---

### 📝 Summary Table

| ViewSet                   | List Endpoint                      | Retrieve Endpoint                      | Special Features         |
|---------------------------|------------------------------------|----------------------------------------|-------------------------|
| **ProductsViewSet**       | `GET /api/products/`               | `GET /api/products/{id}/`              | Cache + Pagination      |
| **CategoryViewSet**       | `GET /api/categories/`             | `GET /api/categories/{id}/`            |                         |
| **BrandViewSet**          | `GET /api/brands/`                 | `GET /api/brands/{id}/`                |                         |
| **ProductImageViewSet**   | `GET /api/product-images/`         | `GET /api/product-images/{id}/`        |                         |
| **ProductVariantViewSet** | `GET /api/variants/`               | `GET /api/variants/{id}/`              |                         |
| **ProductAttributeViewSet** | `GET /api/attributes/`           | `GET /api/attributes/{id}/`            |                         |
| **InventoryViewSet**      | `GET /api/inventory/`              | `GET /api/inventory/{id}/`             |                         |

---

## 🎨 Pretty Quick Reference

Below is a visually enhanced summary of all viewsets in `products/api/viewsets.py`.

---

### 🚀 ProductsViewSet

| Endpoint                      | Description                        | Special Features         |
|-------------------------------|------------------------------------|-------------------------|
| `GET /api/products/`          | Paginated product list (cached)    | Cache + Pagination      |
| `GET /api/products/{id}/`     | Retrieve single product            |                         |

---

### 🏷️ CategoryViewSet

| Endpoint                      | Description                        |
|-------------------------------|------------------------------------|
| `GET /api/categories/`        | List all categories                |
| `GET /api/categories/{id}/`   | Retrieve category by ID            |

---

### 🏢 BrandViewSet

| Endpoint                      | Description                        |
|-------------------------------|------------------------------------|
| `GET /api/brands/`            | List all brands                    |
| `GET /api/brands/{id}/`       | Retrieve brand by ID               |

---

### 🖼️ ProductImageViewSet

| Endpoint                          | Description                        |
|------------------------------------|------------------------------------|
| `GET /api/product-images/`         | List all images                    |
| `GET /api/product-images/{id}/`    | Retrieve image by ID               |

---

### 🔀 ProductVariantViewSet

| Endpoint                      | Description                        |
|-------------------------------|------------------------------------|
| `GET /api/variants/`          | List all variants                  |
| `GET /api/variants/{id}/`     | Retrieve variant by ID             |

---

### 🎛️ ProductAttributeViewSet

| Endpoint                      | Description                        |
|-------------------------------|------------------------------------|
| `GET /api/attributes/`        | List all attributes                |
| `GET /api/attributes/{id}/`   | Retrieve attribute by ID           |

---

### 📦 InventoryViewSet

| Endpoint                      | Description                        |
|-------------------------------|------------------------------------|
| `GET /api/inventory/`         | List all inventory records         |
| `GET /api/inventory/{id}/`    | Retrieve inventory record by ID    |

---

## ⚡️ Behavior & Responses

- **List endpoints:** Return all records (except Products, which is paginated and cached).
- **Retrieve endpoints:** Return single record by ID.
- **Responses:**  
    - `200 OK` — Success (JSON data)  
    - `404 Not Found` — Record not found

## 🌟 API ViewSets – Styled Reference

### 📦 ProductsViewSet
- **Purpose:** List/retrieve products (paginated, cached).
- **Endpoints:**
    - `GET /api/products/` — Paginated product list <br> <span style="color: #4caf50;">(uses cache)</span>
    - `GET /api/products/{id}/` — Retrieve single product
- **Special:** <span style="color: #2196f3;">Cache + Cursor-based Pagination</span>

---

### 🏷️ CategoryViewSet
- **Purpose:** List/retrieve product categories.
- **Endpoints:**
    - `GET /api/categories/` — List all categories
    - `GET /api/categories/{id}/` — Retrieve category by ID

---

### 🏢 BrandViewSet
- **Purpose:** List/retrieve brands.
- **Endpoints:**
    - `GET /api/brands/` — List all brands
    - `GET /api/brands/{id}/` — Retrieve brand by ID

---

### 🖼️ ProductImageViewSet
- **Purpose:** List/retrieve product images.
- **Endpoints:**
    - `GET /api/product-images/` — List all images
    - `GET /api/product-images/{id}/` — Retrieve image by ID

---

### 🔀 ProductVariantViewSet
- **Purpose:** List/retrieve product variants.
- **Endpoints:**
    - `GET /api/variants/` — List all variants
    - `GET /api/variants/{id}/` — Retrieve variant by ID

---

### 🎛️ ProductAttributeViewSet
- **Purpose:** List/retrieve product attributes.
- **Endpoints:**
    - `GET /api/attributes/` — List all attributes
    - `GET /api/attributes/{id}/` — Retrieve attribute by ID

---

### 📦 InventoryViewSet
- **Purpose:** List/retrieve inventory/stock records.
- **Endpoints:**
    - `GET /api/inventory/` — List all inventory records
    - `GET /api/inventory/{id}/` — Retrieve inventory record by ID

---

### ⚡️ Behavior & Responses

| Endpoint Type   | Behavior                                                                 | Responses                                   |
|-----------------|--------------------------------------------------------------------------|---------------------------------------------|
| **List**        | Returns all records (Products: paginated & cached)                       | `200 OK` – JSON array                       |
| **Retrieve**    | Returns single record by ID                                              | `200 OK` – JSON object<br>`404 Not Found`   |

---

> **ℹ️ Note:**  
> - Only `ProductsViewSet.list` uses cache and pagination.  
> - All other endpoints query the database directly.


## ✅ Summary

- **ProductsViewSet:** Product list (cached + paginated) & single product.
- **CategoryViewSet:** List/retrieve categories.
- **BrandViewSet:** List/retrieve brands.
- **ProductImageViewSet:** List/retrieve images.
- **ProductVariantViewSet:** List/retrieve variants.
- **ProductAttributeViewSet:** List/retrieve attributes.
- **InventoryViewSet:** List/retrieve inventory/stock.

> **Note:**  
> - Only `ProductsViewSet.list` uses cache + pagination.  
> - All other endpoints query the database directly.

---
GET /api/categories/ → List all categories.

GET /api/categories/{id}/ → Retrieve a category by ID.

Behavior:

list → Fetch all categories, order by created_at DESC, serialize and return.

retrieve → Fetch category by ID, serialize and return.

Responses:

200 OK – JSON with category/categories.

404 Not Found – Category not found.

🏢 Brands
BrandViewSet

Purpose:
Retrieve brands (list and single).

Endpoints:

GET /api/brands/ → List all brands.

GET /api/brands/{id}/ → Retrieve a brand by ID.

Behavior:

list → Fetch all brands, order by created_at DESC, serialize.

retrieve → Fetch brand by ID, serialize.

Responses:

200 OK – JSON with brand/brands.

404 Not Found – Brand not found.

🖼️ Product Images
ProductImageViewSet

Purpose:
Retrieve product images (list and single).

Endpoints:

GET /api/product-images/ → List all images.

GET /api/product-images/{id}/ → Retrieve a single image.

Behavior:

list → Return all product images.

retrieve → Return single product image by ID.

Responses:

200 OK – JSON with image(s).

404 Not Found – Image not found.

🔀 Product Variants
ProductVariantViewSet

Purpose:
Retrieve product variants (list and single).

Endpoints:

GET /api/variants/ → List all variants.

GET /api/variants/{id}/ → Retrieve a single variant.

Behavior:

list → Return all variants.

retrieve → Return variant by ID.

Responses:

200 OK – JSON with variant(s).

404 Not Found – Variant not found.

🎛️ Product Attributes
ProductAttributeViewSet

Purpose:
Retrieve product attributes (list and single).

Endpoints:

GET /api/attributes/ → List all attributes.

GET /api/attributes/{id}/ → Retrieve a single attribute.

Behavior:

list → Return all attributes.

retrieve → Return attribute by ID.

Responses:

200 OK – JSON with attribute(s).

404 Not Found – Attribute not found.

📦 Inventory
InventoryViewSet

Purpose:
Retrieve inventory/stock (list and single).

Endpoints:

GET /api/inventory/ → List all inventory records.

GET /api/inventory/{id}/ → Retrieve stock entry by ID.

Behavior:

list → Return all inventory records.

retrieve → Return inventory record by ID.

Responses:

200 OK – JSON with inventory data.

404 Not Found – Inventory record not found.

✅ Summary

ProductsViewSet → Product list (cached + paginated) & single product.

CategoryViewSet → List/retrieve categories.

BrandViewSet → List/retrieve brands.

ProductImageViewSet → List/retrieve images.

ProductVariantViewSet → List/retrieve variants.

ProductAttributeViewSet → List/retrieve attributes.

InventoryViewSet → List/retrieve inventory/stock.

👉 Only ProductsViewSet.list uses cache + pagination.
👉 All other endpoints query the database directly.