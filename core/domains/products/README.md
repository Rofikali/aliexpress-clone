🛍️ PRODUCTS DOMAIN — CATALOG AT SCALE

📄 Save as
core/domains/products/README.md

📁 FULL PRODUCTS DOMAIN FOLDER STRUCTURE
core/domains/products/
├── README.md                          # Domain vision & rules
│
├── domain/                            # PURE CATALOG LOGIC
│   ├── aggregates/
│   │   └── product.py                 # Aggregate root
│   │
│   ├── entities/
│   │   ├── product_variant.py         # SKU-level
│   │   ├── product_image.py
│   │   ├── product_attribute.py
│   │   ├── product_price.py
│   │   └── product_inventory_link.py
│   │
│   ├── value_objects/
│   │   ├── product_id.py
│   │   ├── sku.py
│   │   ├── money.py
│   │   ├── currency.py
│   │   ├── attribute_key.py
│   │   └── attribute_value.py
│   │
│   ├── policies/
│   │   ├── pricing_policy.py
│   │   ├── visibility_policy.py
│   │   └── publish_policy.py
│   │
│   ├── services/
│   │   ├── product_pricing_service.py
│   │   └── product_visibility_service.py
│   │
│   └── exceptions.py
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── create_product/
│   │   ├── update_product/
│   │   ├── add_variant/
│   │   ├── update_pricing/
│   │   ├── update_inventory_link/
│   │   ├── publish_product/
│   │   └── archive_product/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── create_product_port.py
│       │   └── update_product_port.py
│       │
│       └── outbound/
│           ├── product_repository_port.py
│           ├── inventory_port.py
│           ├── search_index_port.py
│           └── event_publisher_port.py
│
├── adapters/                          # FRAMEWORKS & EXTERNAL
│   ├── inbound/
│   │   └── rest/
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── urls.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│       │   │   ├── product_model.py
│       │   │   ├── variant_model.py
│       │   │   ├── image_model.py
│       │   │   └── attribute_model.py
│       │   │
│       │   └── repositories/
│       │       └── django_product_repository.py
│       │
│       ├── search/
│       │   └── elasticsearch_adapter.py
│       │
│       └── messaging/
│           └── product_event_publisher.py
│
├── events/                            # DOMAIN FACTS
│   ├── product_created.py
│   ├── product_updated.py
│   ├── product_published.py
│   └── product_archived.py
│
├── contracts/                         # PUBLIC BOUNDARIES
│   ├── events/
│   │   ├── product_created.v1.json
│   │   └── product_published.v1.json
│   │
│   └── apis/
│       └── products.v1.yaml
│
├── read_models/                       # 🔥 READ-OPTIMIZED VIEWS
│   ├── product_listing/
│   └── product_detail/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 PRODUCT AGGREGATE — MENTAL MODEL
Product (Aggregate Root)
│
├── Variants (SKUs)
│   ├── Price
│   ├── Attributes
│   └── Inventory link
│
├── Images
├── Visibility status
│
└── Invariants:
    • Cannot publish without price
    • SKU must be unique
    • Variant must have attributes

🧩 WHY PRODUCT IS COMPLEX (AND WHY THIS WORKS)
❌ BAD DESIGN

One giant Product table

JSON attributes

Pricing everywhere

Logic in serializers

✅ GOOD DESIGN (THIS)

Variants are first-class entities

Prices are explicit

Attributes are structured

Read models separated

🔄 PRODUCTS ↔ INVENTORY ↔ SEARCH

Products NEVER:
❌ Track stock
❌ Update inventory

They emit:

ProductPublished
 → Inventory subscribes
 → Search subscribes


Loose coupling = infinite scale.

🔥 READ MODELS (CQRS-LITE)
products/read_models/
├── product_listing/
└── product_detail/


Used for:
• Search
• Fast reads
• UI APIs

Write model stays clean.

🧪 TEST STRATEGY
Domain
→ Pricing rules
→ Publish rules

Application
→ Use cases

Adapters
→ ORM, search, messaging

🧭 SAFE REFACTOR PATH
Week 1

✔ Create folders
✔ No logic moved

Week 2

✔ Extract product rules

Week 3

✔ Separate variants

Week 4

✔ Add read models

🚫 PRODUCT ANTI-PATTERNS

❌ Product + Inventory mix
❌ Price in many places
❌ Business logic in admin
❌ No SKU uniqueness

🧠 PRINCIPAL-LEVEL LAW

Catalog grows forever.
Design it as if it will outlive every developer here.

✅ NEXT STEPS (CHOOSE ONE)

1️⃣ Inventory domain (stock & reservations)
2️⃣ Checkout domain (orchestration)
3️⃣ Coupons & promotions
4️⃣ Search & read models deep dive
5️⃣ Map your current product models into this structure