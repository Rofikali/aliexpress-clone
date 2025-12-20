🏗️ ALIEXPRESS-CLONE — STAFF-LEVEL FOLDER STRUCTURE (V1)

📄 You can paste this directly into your repo as STRUCTURE.md

aliexpress/
├── README.md
├── manage.py
├── pyproject.toml / requirements.txt
├── .env
├── .gitignore
│
├── core/                       # 🧠 HEART OF THE SYSTEM
│   │
│   ├── domains/                # BUSINESS CAPABILITIES (DDD)
│   │   ├── products/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── carts/
│   │   ├── checkout/
│   │   ├── inventory/
│   │   ├── shipping/
│   │   ├── coupons/
│   │   ├── refunds/
│   │   ├── accounts/
│   │   └── reviews/
│   │
│   ├── shared_kernel/          # VERY SMALL SHARED CODE
│   │   ├── money/
│   │   ├── ids/
│   │   ├── time/
│   │   └── exceptions/
│   │
│   ├── observability/          # LOGS, METRICS, TRACING
│   │   ├── logging/
│   │   ├── tracing/
│   │   └── metrics/
│   │
│   ├── platform/               # INFRASTRUCTURE & TOOLS
│   │   ├── database/
│   │   ├── messaging/
│   │   ├── auth/
│   │   └── settings/
│   │
│   └── governance/             # ARCHITECTURE CONTROL
│       ├── adr/
│       ├── architecture_reviews/
│       ├── ownership/
│       └── principles/
│
├── apps/                       # DJANGO INTEGRATION LAYER
│   ├── api/
│   ├── admin/
│   └── health/
│
├── scripts/
├── tests/
└── docker/

🔑 WHY THIS STRUCTURE IS SAFE TO START WITH

✔ You don’t break Django
✔ You don’t force microservices
✔ You isolate business logic early
✔ You can extract repos later

This is how Stripe, Shopify, Amazon started.

🧩 DOMAIN STRUCTURE (APPLIES TO EVERY DOMAIN)

Now let’s define ONE domain properly.
All others copy this pattern.

📦 Example: core/domains/orders/
orders/
├── domain/                     # PURE BUSINESS LOGIC
│   ├── aggregates/
│   │   └── order.py
│   ├── entities/
│   │   └── order_item.py
│   ├── value_objects/
│   │   ├── order_status.py
│   │   └── address.py
│   ├── services/
│   └── exceptions.py
│
├── application/                # USE CASES
│   ├── use_cases/
│   │   ├── create_order/
│   │   ├── cancel_order/
│   │   ├── complete_order/
│   │   └── refund_order/
│   │
│   └── ports/
│       ├── inbound/
│       └── outbound/
│
├── adapters/                   # DJANGO + EXTERNAL
│   ├── inbound/
│   │   └── rest/
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── urls.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models.py
│       │   └── repositories.py
│       ├── messaging/
│       └── payments/
│
├── events/
│   ├── order_created.py
│   ├── order_cancelled.py
│   └── order_completed.py
│
├── sagas/
│   └── order_checkout_saga.py
│
├── contracts/
│   ├── events/
│   └── apis/
│
└── tests/

🧠 KEY RULES (MEMORIZE THESE)
❌ What NEVER goes in domain/

Django models

HTTP requests

DB queries

External APIs

✔ What MUST go in domain/

Business rules

Validations

Invariants

🧱 PRODUCT DOMAIN (ALIEXPRESS-LEVEL)

Products are complex.
They deserve many sub-models, not one file.

products/
├── domain/
│   ├── aggregates/
│   │   └── product.py
│   ├── entities/
│   │   ├── product_variant.py
│   │   ├── product_image.py
│   │   ├── product_attribute.py
│   │   └── product_price.py
│   ├── value_objects/
│   │   ├── sku.py
│   │   └── money.py
│   └── exceptions.py
│
├── application/
├── adapters/
├── events/
├── contracts/
└── tests/


👉 NO single “models.py” with 2,000 lines.

🛒 OTHER DOMAINS (A–Z YOU ASKED)
core/domains/
├── carts/
├── checkout/
├── coupons/
├── refunds/
├── payments/
├── inventory/
├── shipping/
├── accounts/
├── reviews/


All follow the same internal structure.

🧪 TEST STRATEGY (START SIMPLE)
tests/
├── unit/          # domain logic
├── integration/   # adapters
└── contract/      # events & APIs

🧭 HOW YOU REFACTOR SLOWLY (IMPORTANT)
Week 1–2

✔ Create folders
✔ Move NOTHING yet

Week 3–4

✔ Extract domain logic
✔ Keep Django models

Month 2

✔ Introduce use cases
✔ Thin views

Month 3+

✔ Add events & sagas
✔ Extract repos if needed

🏁 FINAL PRINCIPAL-LEVEL ADVICE
Architecture is not built in one sprint.
It is protected over many years.


You now have a rock-solid foundation.

NEXT STEP (I recommend this order)

1️⃣ Orders domain (deep dive)
2️⃣ Payments domain (money safety)
3️⃣ Product domain (catalog scale)
4️⃣ Event contracts
5️⃣ Repo split