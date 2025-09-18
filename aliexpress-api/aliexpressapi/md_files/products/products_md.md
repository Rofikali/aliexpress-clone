# All Products Response

## 🛒 All Products Response

```json
{
  "success": true,
  "code": 200,
  "message": "Products fetched successfully (cache)",
  "request": {
    "id": "2d5e292b-0c39-411f-a60d-ce50e6fa8f57",
    "timestamp": "2025-09-09T08:14:06.011532Z",
    "latency_ms": 0.13,
    "region": "Nepal-01",
    "cache": "HIT"
  },
  "meta": {
    "next_cursor": "cD0yMDI1LTA5LTA3KzA5JTNBMTElM0EyMS4yNTI0NTclMkIwMCUzQTAw",
    "has_next": true
  },
  "errors": null,
  "data": [
    {
      "id": "574ac81c-3eb2-4173-b048-68472c501952",
      "title": "Street range",
      "description": "Total now large learn these marriage rich its. Stand thank type state. Performance class fact speech.",
      "price": "479.33",
      "image": "http://localhost:8000/media/products/images/picture-participant.jpg",
      "images": [
        {
          "id": 2246,
          "product": "574ac81c-3eb2-4173-b048-68472c501952",
          "image": "http://localhost:8000/media/products/images/picture-participant-1.jpg"
        }
      ],
      "category": {
        "id": 1,
        "name": "Default Category",
        "description": "Auto-created default category"
      },
      "brand": {
        "id": 1,
        "name": "Default Brand",
        "description": "Auto-created default brand"
      },
      "created_at": "2025-09-07T09:11:21.497504Z",
      "updated_at": "2025-09-07T11:24:36.017785Z"
    }
  ]
}
```

---

## 🛍️ Single Product Response

```json
{
  "success": true,
  "code": 200,
  "message": "Single Product fetched successfully",
  "request": {
    "id": "546306ea-c907-4021-9c8e-c22b1efd6bc2",
    "timestamp": "2025-09-11T05:37:09.181412Z",
    "latency_ms": 0.05,
    "region": "Nepal-01",
    "cache": "MISS"
  },
  "meta": {},
  "errors": null,
  "data": {
    "id": "753c1017-2735-42a6-afab-5d771cbc70a7",
    "title": "Before student none",
    "description": "Hot style newspaper citizen hour. Quite over future rock.\nSet already American movie. Political rich probably once somebody raise job performance.",
    "price": "317.26",
    "image": "http://localhost:8000/media/products/images/of-religious.jpg",
    "images": [
      {
        "id": 246,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-1.jpg"
      },
      {
        "id": 247,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-2.jpg"
      },
      {
        "id": 248,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-3.jpg"
      },
      {
        "id": 249,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-4.jpg"
      },
      {
        "id": 250,
        "product": "753c1017-2735-42a6-afab-5d771cbc70a7",
        "image": "http://localhost:8000/media/products/images/of-religious-5.jpg"
      }
    ],
    "category": {
      "id": 1,
      "name": "Default Category",
      "description": "Auto-created default category"
    },
    "brand": {
      "id": 1,
      "name": "Default Brand",
      "description": "Auto-created default brand"
    },
    "created_at": "2025-09-06T05:53:01.782086Z",
    "updated_at": "2025-09-06T05:53:01.790535Z"
  }
}
```

---

## ❌ Error Layers

```json
{
  "success": false,
  "code": 400,
  "message": "Validation failed",
  "request": {
    "id": "d70b2330-c7c3-4e21-a2d7-1bfde448c735",
    "timestamp": "2025-09-09T08:18:40.915393Z",
    "latency_ms": 0.13,
    "region": "Nepal-01",
    "cache": "MISS"
  },
  "meta": {},
  "errors": [
    { "code": "USERNAME", "message": "user with this username already exists." },
    { "code": "EMAIL", "message": "Enter a valid email address." },
    { "code": "PHONE_NUMBER", "message": "Enter a valid phone number (digits only, 7-15)." },
    { "code": "PASSWORD", "message": "Ensure this field has at least 8 characters." },
    { "code": "ROLE", "message": "\"b\" is not a valid choice." }
  ],
  "data": null
}
```

---

## 📑 Overview

The product system supports:

- **Hierarchical Categories** (e.g., Electronics → Mobile Phones → Accessories)
- **Brands** (logos, descriptions, metadata)
- **Products** (pricing, discounts, stock, seller references)
- **Product Images** (multiple images per product)
- **Product Variants** (size, color, material, custom attributes)
- **Product Attributes** (extra metadata per product/variant)
- **Inventory Tracking** (adjustments, restocks, returns, orders)

---

## 📂 Models

### 1. Category

| Field        | Type           | Notes                        |
|--------------|----------------|------------------------------|
| name         | CharField(255) | Category name                |
| slug         | SlugField      | Unique, indexed slug         |
| parent       | FK(Category)   | Self-referencing hierarchy   |
| description  | TextField      | Optional description         |
| created_at   | DateTime       | Auto timestamp               |
| updated_at   | DateTime       | Auto timestamp               |

> ✅ Use for building category trees (nested categories).

---

### 2. Brand

| Field        | Type           | Notes                        |
|--------------|----------------|------------------------------|
| name         | CharField(255) | Unique brand name            |
| slug         | SlugField      | Unique, indexed slug         |
| logo         | URLField       | Logo (stored remotely)       |
| description  | TextField      | Optional description         |
| created_at   | DateTime       | Auto timestamp               |
| updated_at   | DateTime       | Auto timestamp               |

> ✅ Example: Nike, Apple, Samsung.

---

### 3. Product

| Field           | Type              | Notes                                 |
|-----------------|-------------------|---------------------------------------|
| id              | UUIDField (PK)    | Stable unique ID (UUIDv4)             |
| title           | CharField(255)    | Product title                         |
| slug            | SlugField         | Unique slug                           |
| description     | TextField         | Full description                      |
| sku             | CharField(100)    | Unique stock keeping unit             |
| price           | Decimal(12,2)     | Base price                            |
| discount_price  | Decimal(12,2)     | Nullable, optional discount           |
| currency        | CharField(3)      | Defaults to "USD"                     |
| image           | ImageField        | Primary image                         |
| stock           | IntegerField      | Current stock                         |
| is_active       | BooleanField      | Visible in storefront                 |
| rating          | FloatField        | Average rating                        |
| review_count    | IntegerField      | Count of reviews                      |
| seller          | FK(User)          | Reference to account/user             |
| category        | FK(Category)      | Category assignment                   |
| brand           | FK(Brand)         | Optional brand reference              |
| created_at      | DateTime          | Auto timestamp                        |
| updated_at      | DateTime          | Auto timestamp                        |

> ✅ Supports sellers, multiple categories, brand linking, and marketplace setup.

---

### 4. ProductImage

| Field      | Type           | Notes                        |
|------------|----------------|------------------------------|
| product    | FK(Product)    | Related product              |
| image      | ImageField     | Path: products/images/       |
| alt_text   | CharField(255) | For accessibility/SEO        |
| position   | IntegerField   | Sort order                   |
| created_at | DateTime       | Auto timestamp               |

> ✅ Example: Product galleries, thumbnails.

---

### 5. ProductVariant

| Field          | Type           | Notes                                 |
|----------------|----------------|---------------------------------------|
| product        | FK(Product)    | Parent product                        |
| price          | Decimal(12,2)  | Variant price                         |
| variant_type   | CharField(20)  | Choices: size, color, material, custom|
| value          | CharField(100) | e.g., "Red", "XL"                     |
| price_override | Decimal(12,2)  | Optional price override               |
| stock          | IntegerField   | Variant stock                         |
| sku            | CharField(100) | Unique SKU                            |
| created_at     | DateTime       | Auto timestamp                        |
| updated_at     | DateTime       | Auto timestamp                        |

> ✅ Example: A T-shirt available in S, M, L.

---

### 6. ProductAttribute

| Field           | Type           | Notes                        |
|-----------------|----------------|------------------------------|
| product         | FK(Product)    | Related product              |
| variant         | FK(ProductVariant)| Related variant           |
| attribute_name  | CharField(100) | e.g., "Material"             |
| attribute_value | CharField(255) | e.g., "Cotton"               |
| name            | CharField(100) | Indexable key                |
| key             | CharField(100) | Attribute key                |
| value           | CharField(255) | Attribute value              |
| created_at      | DateTime       | Auto timestamp               |
| updated_at      | DateTime       | Auto timestamp               |

> ✅ Example: Weight: 200g, Waterproof: Yes.

---

### 7. Inventory

| Field        | Type           | Notes                        |
|--------------|----------------|------------------------------|
| stock        | IntegerField   | Current stock                |
| sku          | CharField(100) | SKU reference                |
| product      | FK(Product)    | Product link                 |
| change       | IntegerField   | + / - stock movement         |
| reason       | CharField(20)  | Choices: order, restock, return, adjustment |
| quantity     | IntegerField   | Quantity involved            |
| location     | CharField(255) | Warehouse/location info      |
| reference_id | UUIDField      | Order or external reference  |
| created_at   | DateTime       | Auto timestamp               |

> ✅ Enables auditing of stock movements.

---

## 🗂️ Entity-Relationship Diagram (ERD)

```
Category ───< Product >─── Brand
                │
                │ has many
                ▼
          ProductImage
                │
                │ has many
                ▼
          ProductVariant ───< ProductAttribute
                │
                │ stock tracked by
                ▼
             Inventory
```

---

## 🔄 Frontend Data Flow

Shows how JSON from API → frontend components.

```
[API Response]
   |
   v
+-----------------+     +-----------------+
| Category JSON   | --> | Sidebar Menu    |
+-----------------+     +-----------------+

+-----------------+     +-----------------+
| Brand JSON      | --> | Brand Filter    |
+-----------------+     +-----------------+

+-----------------+     +-----------------+
| Product JSON    | --> | Product List    |
|                 | --> | Product Detail  |
+-----------------+     +-----------------+

+-----------------+     +-----------------+
| ProductImage    | --> | Image Carousel  |
+-----------------+     +-----------------+

+-----------------+     +-----------------+
| Variants JSON   | --> | Variant Selector|
+-----------------+     +-----------------+

+-----------------+     +-----------------+
| Attributes JSON | --> | Specs Tab       |
+-----------------+     +-----------------+

+-----------------+     +-----------------+
| Inventory JSON  | --> | Stock / AddCart |
+-----------------+     +-----------------+
```

---

## 🖼️ UI Wireframe Mapping

Imagine one Product Detail Page:

```
 ------------------------------------------------
|  [ Product Gallery ]   [ Product Title ]       |
|                        [ Price / Discount ]    |
|                        [ Brand Logo ]          |
|                        [ Rating & Reviews ]    |
|                                                |
|  [ Variant Selector (Size, Color) ]            |
|  [ Stock Status ] [ Add to Cart Button ]       |
|                                                |
|  --- Tabs ----------------------------------   |
|   [ Description ] [ Specifications ] [ Reviews]|
|   -> Description = Product.description         |
|   -> Specifications = ProductAttribute         |
|   -> Reviews = (future)                        |
|                                                |
 ------------------------------------------------
```

---