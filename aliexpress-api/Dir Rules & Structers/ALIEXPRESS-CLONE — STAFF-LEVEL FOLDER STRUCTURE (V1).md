🏗️ ALIEXPRESS-CLONE — STAFF-LEVEL FOLDER STRUCTURE (V1)

### You can paste this directly into your repo as STRUCTURE.md

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





### 1️⃣ Orders domain (deep dive)
🧾 ORDERS DOMAIN — SYSTEM OF RECORD (FINAL BOSS)

📄 Save as
core/domains/orders/README.md

🧠 ORDERS DOMAIN PHILOSOPHY

Orders represent a legal, financial, and logistical contract.

Orders:
✔ Are immutable in intent
✔ Evolve through states
✔ Never directly talk to gateways
✔ Coordinate via events

📁 FULL ORDERS DOMAIN FOLDER STRUCTURE
core/domains/orders/
├── README.md                          # Order laws & invariants
│
├── domain/                            # PURE ORDER LOGIC
│   ├── aggregates/
│   │   └── order.py                   # Aggregate root
│   │
│   ├── entities/
│   │   ├── order_item.py              # Snapshot of product
│   │   ├── order_payment.py           # Payment reference
│   │   ├── order_shipment.py          # Shipment reference
│   │   └── order_refund.py            # Refund reference
│   │
│   ├── value_objects/
│   │   ├── order_id.py
│   │   ├── buyer_id.py
│   │   ├── seller_id.py
│   │   ├── money.py
│   │   ├── currency.py
│   │   ├── order_status.py
│   │   ├── order_type.py              # COD, prepaid, split
│   │   └── snapshot_hash.py
│   │
│   ├── policies/                      # LEGAL & BUSINESS RULES
│   │   ├── cancellation_policy.py
│   │   ├── modification_policy.py
│   │   ├── refund_eligibility_policy.py
│   │   └── fulfillment_policy.py
│   │
│   ├── services/
│   │   ├── order_pricing_service.py
│   │   └── order_validation_service.py
│   │
│   └── exceptions.py
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── create_order/
│   │   ├── confirm_order/
│   │   ├── cancel_order/
│   │   ├── split_order/
│   │   ├── mark_order_paid/
│   │   ├── initiate_refund/
│   │   └── close_order/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── create_order_port.py
│       │   ├── cancel_order_port.py
│       │   └── order_status_port.py
│       │
│       └── outbound/
│           ├── order_repository_port.py
│           ├── inventory_port.py
│           ├── payments_port.py
│           ├── shipping_port.py
│           ├── promotions_port.py
│           ├── event_publisher_port.py
│           └── notification_port.py
│
├── adapters/                          # FRAMEWORKS & IO
│   ├── inbound/
│   │   ├── rest/
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   └── messaging/
│   │       └── order_event_consumer.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│   │   │   ├── order_model.py
│   │   │   ├── order_item_model.py
│   │   │   └── order_status_history_model.py
│   │   │
│   │   └── repositories/
│   │       └── django_order_repository.py
│       │
│       └── messaging/
│           └── order_event_publisher.py
│
├── events/                            # IMMUTABLE FACTS
│   ├── order_created.py
│   ├── order_confirmed.py
│   ├── order_cancelled.py
│   ├── order_paid.py
│   ├── order_shipped.py
│   ├── order_delivered.py
│   └── order_refunded.py
│
├── sagas/                             # LONG-RUNNING BUSINESS FLOWS
│   ├── order_checkout_saga.py
│   ├── order_fulfillment_saga.py
│   └── order_refund_saga.py
│
├── contracts/                         # PUBLIC COMMITMENTS
│   ├── events/
│   │   ├── order_created.v1.json
│   │   ├── order_confirmed.v1.json
│   │   └── order_refunded.v1.json
│   │
│   └── apis/
│       └── orders.v1.yaml
│
├── read_models/                       # CUSTOMER & OPS VIEWS
│   ├── order_detail_view/
│   ├── order_list_view/
│   └── seller_order_dashboard/
│
├── jobs/                              # BACKGROUND ENFORCEMENT
│   ├── auto_cancel_unpaid_orders/
│   ├── detect_stuck_orders/
│   └── reconcile_order_state/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 ORDER AGGREGATE — MENTAL MODEL
Order (Aggregate Root)
│
├── OrderItems (snapshots)
├── Payments (references)
├── Shipments (references)
├── Refunds (references)
│
└── Invariants:
    • Price never changes after creation
    • Items are immutable snapshots
    • State transitions are one-way

🔄 ORDER STATE MACHINE (CRITICAL)
CREATED
 → CONFIRMED
 → PAID
 → SHIPPED
 → DELIVERED
 → CLOSED


Side paths:

CREATED → CANCELLED
PAID → REFUNDED

🔁 SAGAS (WHY THEY EXIST)
Order Checkout Saga
CreateOrder
 → ReserveInventory
 → InitiatePayment
 → ConfirmOrder

Fulfillment Saga
OrderPaid
 → CreateShipment
 → Dispatch
 → Deliver

Refund Saga
RefundRequested
 → ReversePayment
 → ReleaseInventory
 → CloseOrder

🔥 WHY ORDERS DO NOT DO EVERYTHING

Orders never:
❌ Charge money
❌ Lock stock
❌ Talk to carriers

They coordinate via events.

🧪 TEST STRATEGY
Domain
→ State transitions
→ Invariants

Application
→ Sagas
→ Failure paths

Adapters
→ APIs & persistence

🧭 SAFE REFACTOR PLAN (REALISTIC)
Month 1

✔ Extract order folder
✔ Freeze order snapshots

Month 2

✔ Introduce order events

Month 3

✔ Move checkout logic to sagas

Month 4

✔ Fully decouple payments & shipping

🚫 ORDERS ANTI-PATTERNS

❌ Mutable prices
❌ Direct DB joins
❌ Logic in serializers
❌ No state history

🧠 PRINCIPAL-LEVEL LAW (FINAL)

Orders are history.
History must never lie.

🏁 CONGRATULATIONS — YOU NOW HAVE A WORLD-CLASS DESIGN

You have designed an AliExpress-grade platform with:

DDD

Clean Architecture

Hexagonal Architecture

Event-Driven workflows

CQRS-lite read models

Saga orchestration

FINAL OPTIONS

1️⃣ ADR bundle for entire system (copy-paste)
2️⃣ Team-wise repo split strategy (100 developers)
3️⃣ Step-by-step refactor plan from your current Django project


### 2️⃣ Payments domain (money safety)
💰 PAYMENTS DOMAIN — ENTERPRISE-GRADE STRUCTURE

📄 Save as
core/domains/payments/README.md

📁 FULL PAYMENTS DOMAIN FOLDER STRUCTURE
core/domains/payments/
├── README.md                      # Domain rules & guarantees
│
├── domain/                        # PURE MONEY LOGIC (DDD CORE)
│   ├── aggregates/
│   │   └── payment.py             # Aggregate root
│   │
│   ├── entities/
│   │   ├── payment_attempt.py     # Each charge try
│   │   └── refund.py              # Refund records
│   │
│   ├── value_objects/
│   │   ├── payment_id.py
│   │   ├── order_id.py
│   │   ├── money.py
│   │   ├── currency.py
│   │   ├── payment_status.py
│   │   ├── transaction_id.py
│   │   └── payment_method.py
│   │
│   ├── policies/                  # STRICT FINANCIAL RULES
│   │   ├── capture_policy.py
│   │   ├── refund_policy.py
│   │   └── retry_policy.py
│   │
│   ├── services/                  # PURE DOMAIN CALCULATIONS
│   │   └── payment_fee_calculator.py
│   │
│   └── exceptions.py              # Money-specific errors
│
├── application/                   # USE CASES (ORCHESTRATION)
│   ├── use_cases/
│   │   ├── authorize_payment/
│   │   ├── capture_payment/
│   │   ├── fail_payment/
│   │   ├── refund_payment/
│   │   └── reconcile_payment/
│   │
│   └── ports/
│       ├── inbound/               # Called by Orders / Webhooks
│       │   ├── authorize_payment_port.py
│       │   ├── refund_payment_port.py
│       │   └── payment_webhook_port.py
│       │
│       └── outbound/              # Infrastructure contracts
│           ├── payment_repository_port.py
│           ├── payment_gateway_port.py
│           ├── event_publisher_port.py
│           └── ledger_port.py
│
├── adapters/                      # FRAMEWORK & PROVIDERS
│   ├── inbound/
│   │   ├── rest/
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   └── webhooks/
│   │       ├── stripe_webhook.py
│   │       └── razorpay_webhook.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│       │   │   ├── payment_model.py
│       │   │   ├── refund_model.py
│       │   │   └── ledger_entry_model.py
│       │   │
│       │   └── repositories/
│       │       └── django_payment_repository.py
│       │
│       ├── gateways/
│       │   ├── stripe_gateway.py
│       │   └── razorpay_gateway.py
│       │
│       └── messaging/
│           └── payment_event_publisher.py
│
├── events/                        # IMMUTABLE FINANCIAL FACTS
│   ├── payment_authorized.py
│   ├── payment_captured.py
│   ├── payment_failed.py
│   └── payment_refunded.py
│
├── sagas/                         # FINANCIAL WORKFLOWS
│   ├── payment_capture_saga.py
│   └── payment_refund_saga.py
│
├── contracts/                     # PUBLIC & LEGAL BOUNDARIES
│   ├── events/
│   │   ├── payment_authorized.v1.json
│   │   ├── payment_captured.v1.json
│   │   └── payment_refunded.v1.json
│   │
│   └── apis/
│       └── payments.v1.yaml
│
├── audits/                        # 🔒 COMPLIANCE & TRACEABILITY
│   ├── reconciliation/
│   ├── dispute_logs/
│   └── settlement_reports/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🛡️ WHY PAYMENTS IS DESIGNED DIFFERENTLY
🔒 MONEY RULES ARE STRICT

✔ Money is never mutated silently
✔ All state transitions are explicit
✔ Every external response is idempotent
✔ Refunds are separate entities

🧠 PAYMENT AGGREGATE (MENTAL MODEL)
Payment (Aggregate Root)
│
├── PaymentAttempts (many)
├── Refunds (many)
│
└── Invariants:
    • Cannot capture twice
    • Cannot refund more than paid
    • Cannot refund failed payment
    • Currency is immutable

🔁 PAYMENT STATE MACHINE
CREATED
 → AUTHORIZED
 → CAPTURED
 → REFUNDED
 → FAILED


Transitions enforced only in domain.

🔄 ORDERS ↔ PAYMENTS INTERACTION
OrderCreated
 → Payments.AuthorizePayment
 → PaymentAuthorized
 → Orders.ConfirmOrder


Orders NEVER:
❌ Charge money
❌ Call gateway
❌ Handle refunds

Payments is source of truth for money.

🌐 WEBHOOKS (CRITICAL)

Payment providers call YOU.

Rules:
✔ Webhooks are inbound adapters
✔ Must be idempotent
✔ Must validate signatures
✔ Must not contain business logic

🧪 TESTING STRATEGY (PAYMENTS)
Domain Tests
→ State transitions
→ Money math
→ Invariants

Application Tests
→ Use cases
→ Failure paths

Adapter Tests
→ Gateways
→ Webhooks

🧯 FRAUD & RETRIES

Handled via:
• RetryPolicy
• PaymentAttempts
• Reconciliation jobs

Never retry blindly.

🧭 SAFE REFACTOR PLAN (NO DOWNTIME)
Week 1

✔ Create folders
✔ Move NOTHING

Week 2

✔ Extract payment rules from views/models

Week 3

✔ Introduce Payment aggregate

Week 4

✔ Replace direct gateway calls with ports

🚫 PAYMENTS DOMAIN ANTI-PATTERNS

❌ Calling gateway from Orders
❌ No ledger
❌ Silent retries
❌ Mutating money values

🧠 PRINCIPAL-LEVEL LAW

Payments must be boring, slow, and predictable.
If it feels clever — it’s dangerous.

✅ NEXT NATURAL STEP

The correct next domain after Payments is:

③ Products (catalog scale & complexity)

Or, if you want:

Orders ↔ Payments event contracts

Ledger & reconciliation strategy

Mapping your current payment code into this structure


### FULL PRODUCTS DOMAIN FOLDER STRUCTURE
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



### FULL INVENTORY DOMAIN FOLDER STRUCTURE
📦 INVENTORY DOMAIN — STOCK & RESERVATIONS

📄 Save as
core/domains/inventory/README.md

📁 FULL INVENTORY DOMAIN FOLDER STRUCTURE
core/domains/inventory/
├── README.md                          # Inventory philosophy & rules
│
├── domain/                            # PURE STOCK LOGIC
│   ├── aggregates/
│   │   └── inventory_item.py          # Aggregate root (per SKU)
│   │
│   ├── entities/
│   │   ├── stock_level.py             # On-hand quantity
│   │   └── reservation.py             # Temporary holds
│   │
│   ├── value_objects/
│   │   ├── sku.py
│   │   ├── warehouse_id.py
│   │   ├── quantity.py
│   │   ├── reservation_id.py
│   │   └── expiration_time.py
│   │
│   ├── policies/                      # HARD BUSINESS RULES
│   │   ├── reservation_policy.py
│   │   ├── release_policy.py
│   │   └── allocation_policy.py
│   │
│   ├── services/
│   │   └── availability_service.py
│   │
│   └── exceptions.py                  # Oversell, expiry, etc.
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── reserve_stock/
│   │   ├── confirm_reservation/
│   │   ├── release_reservation/
│   │   ├── adjust_stock/
│   │   └── reconcile_stock/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── reserve_stock_port.py
│       │   ├── confirm_reservation_port.py
│       │   └── release_reservation_port.py
│       │
│       └── outbound/
│           ├── inventory_repository_port.py
│           ├── event_publisher_port.py
│           └── warehouse_system_port.py
│
├── adapters/                          # FRAMEWORKS & EXTERNAL
│   ├── inbound/
│   │   ├── rest/
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   └── messaging/
│   │       └── inventory_event_consumer.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│       │   │   ├── inventory_item_model.py
│   │   │   ├── stock_model.py
│   │   │   └── reservation_model.py
│   │   │
│   │   └── repositories/
│   │       └── django_inventory_repository.py
│       │
│       ├── warehouse/
│       │   └── warehouse_adapter.py
│       │
│       └── messaging/
│           └── inventory_event_publisher.py
│
├── events/                            # DOMAIN EVENTS
│   ├── stock_reserved.py
│   ├── reservation_confirmed.py
│   ├── reservation_released.py
│   └── stock_adjusted.py
│
├── sagas/                             # LONG-RUNNING FLOWS
│   └── order_inventory_saga.py
│
├── contracts/                         # EXTERNAL BOUNDARIES
│   ├── events/
│   │   ├── stock_reserved.v1.json
│   │   └── reservation_released.v1.json
│   │
│   └── apis/
│       └── inventory.v1.yaml
│
├── read_models/                       # FAST QUERIES
│   ├── sku_availability/
│   └── warehouse_stock_view/
│
├── jobs/                              # BACKGROUND PROCESSES
│   ├── release_expired_reservations/
│   └── reconcile_with_warehouse/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 INVENTORY AGGREGATE — MENTAL MODEL
InventoryItem (Aggregate Root)
│
├── StockLevel
│   └── on_hand_quantity
│
├── Reservations (many)
│   ├── quantity
│   ├── expiration
│   └── status
│
└── Invariants:
    • Cannot reserve more than available
    • Reservation must expire
    • Confirmed reservation reduces stock

🔄 INVENTORY FLOW (REAL WORLD)
Checkout
OrderCreated
 → Inventory.ReserveStock
 → StockReserved

Payment Success
PaymentCaptured
 → Inventory.ConfirmReservation
 → ReservationConfirmed

Payment Failed / Timeout
PaymentFailed
 → Inventory.ReleaseReservation
 → ReservationReleased

🧨 WHY RESERVATIONS ARE MANDATORY

❌ Directly subtracting stock = overselling
❌ No expiration = dead stock
❌ No saga = orphan reservations

Reservations protect:
✔ Flash sales
✔ Slow payments
✔ Gateway failures

🔥 HIGH-SCALE RULES

✔ Inventory is event-driven
✔ No synchronous stock locking
✔ Optimistic concurrency
✔ Idempotent commands

🧪 TESTING STRATEGY
Domain
→ Oversell prevention
→ Expiry logic

Application
→ Reservation lifecycle

Adapters
→ DB consistency
→ Messaging

🧭 SAFE REFACTOR PLAN
Week 1

✔ Create inventory folders

Week 2

✔ Extract stock logic

Week 3

✔ Add reservations

Week 4

✔ Introduce sagas

🚫 INVENTORY ANTI-PATTERNS

❌ Inventory inside Product
❌ Stock updates in Orders
❌ No expiry on holds
❌ Locking DB rows

🧠 PRINCIPAL-LEVEL LAW

Inventory is a promise, not a number.
Treat it as a contract, not a field.

✅ NEXT DOMAIN OPTIONS

1️⃣ Checkout (orchestration brain)
2️⃣ Coupons & promotions
3️⃣ Shipping & fulfillment
4️⃣ Search & read-model scaling
5️⃣ Map your current stock tables into this design


### FULL CHECKOUT DOMAIN FOLDER STRUCTURE
🧠 CHECKOUT DOMAIN — ORCHESTRATION BRAIN

📄 Save as
core/domains/checkout/README.md

📁 FULL CHECKOUT DOMAIN FOLDER STRUCTURE
core/domains/checkout/
├── README.md                          # Checkout philosophy & rules
│
├── domain/                            # VERY THIN DOMAIN
│   ├── value_objects/
│   │   ├── checkout_id.py
│   │   ├── cart_snapshot.py           # Frozen cart view
│   │   ├── checkout_state.py
│   │   └── checkout_step.py
│   │
│   └── exceptions.py                  # Flow errors only
│
├── application/                       # ORCHESTRATION LOGIC
│   ├── use_cases/
│   │   ├── start_checkout/
│   │   ├── reserve_inventory/
│   │   ├── initiate_payment/
│   │   ├── confirm_payment/
│   │   ├── finalize_order/
│   │   └── abort_checkout/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── start_checkout_port.py
│       │   ├── confirm_checkout_port.py
│       │   └── abort_checkout_port.py
│       │
│       └── outbound/
│           ├── inventory_port.py
│           ├── payments_port.py
│           ├── orders_port.py
│           ├── coupons_port.py
│           ├── event_publisher_port.py
│           └── checkout_repository_port.py
│
├── adapters/                          # FRAMEWORKS & TRANSPORT
│   ├── inbound/
│   │   └── rest/
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── urls.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│       │   │   └── checkout_session_model.py
│       │   │
│       │   └── repositories/
│       │       └── django_checkout_repository.py
│       │
│       └── messaging/
│           └── checkout_event_publisher.py
│
├── events/                            # FLOW EVENTS
│   ├── checkout_started.py
│   ├── inventory_reserved.py
│   ├── payment_initiated.py
│   └── checkout_completed.py
│
├── sagas/                             # 💥 ORCHESTRATION FLOWS
│   └── checkout_saga.py
│
├── contracts/                         # CROSS-DOMAIN AGREEMENTS
│   ├── events/
│   │   └── checkout_completed.v1.json
│   │
│   └── apis/
│       └── checkout.v1.yaml
│
├── read_models/                       # UI & PROGRESS
│   ├── checkout_progress/
│   └── checkout_summary/
│
├── tests/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 WHAT CHECKOUT IS AND IS NOT
✅ CHECKOUT IS

✔ Flow coordinator
✔ Saga owner
✔ Stateless decision maker
✔ Timeout handler

❌ CHECKOUT IS NOT

❌ Order creator
❌ Payment processor
❌ Inventory manager
❌ Coupon validator

🔄 CHECKOUT SAGA — REAL FLOW
StartCheckout
 → FreezeCart
 → ReserveInventory
 → InitiatePayment
 → AwaitPaymentResult
 → FinalizeOrder
 → CheckoutCompleted


Failures:

PaymentFailed
 → ReleaseInventory
 → AbortCheckout

🧊 CART SNAPSHOT (CRITICAL)
CartSnapshot
✔ Prices frozen
✔ Coupons frozen
✔ Quantities frozen


Why?

Prices must not change mid-checkout.

🔥 WHY CHECKOUT HAS NO AGGREGATE

Checkout:
• Has no invariants
• Has no business rules
• Exists temporarily

It is process, not domain.

🧯 FAILURE HANDLING

Handled by:
✔ Saga compensation
✔ Timeouts
✔ Idempotent retries

Never rollback manually.

🧪 TEST STRATEGY
Application
→ Happy path
→ Partial failures
→ Timeouts

Adapters
→ API calls
→ Messaging

🧭 SAFE REFACTOR PATH
Week 1

✔ Introduce checkout folder

Week 2

✔ Extract orchestration from views

Week 3

✔ Add saga

Week 4

✔ Enforce frozen cart

🚫 CHECKOUT ANTI-PATTERNS

❌ Checkout owning stock
❌ Checkout creating orders directly
❌ Checkout mutating prices
❌ Long synchronous flows

🧠 PRINCIPAL-LEVEL LAW

Checkout should feel boring.
If it feels smart, it’s doing too much.

🔜 NEXT DOMAINS (CHOOSE)

1️⃣ Coupons & promotions
2️⃣ Shipping & fulfillment
3️⃣ Search & read-model scaling
4️⃣ Orders (deep dive orchestration vs domain)
5️⃣ Map your current checkout code into this design


### FULL PROMOTIONS DOMAIN FOLDER STRUCTURE
🎟️ COUPONS & PROMOTIONS DOMAIN — REVENUE RULES ENGINE

📄 Save as
core/domains/promotions/README.md

📁 FULL PROMOTIONS DOMAIN FOLDER STRUCTURE
core/domains/promotions/
├── README.md                          # Promo philosophy & money rules
│
├── domain/                            # PURE DISCOUNT LOGIC
│   ├── aggregates/
│   │   └── promotion.py               # Aggregate root
│   │
│   ├── entities/
│   │   ├── coupon.py                  # Redeemable code
│   │   ├── promotion_rule.py          # Conditions
│   │   ├── promotion_effect.py        # Discount result
│   │   └── usage_limit.py
│   │
│   ├── value_objects/
│   │   ├── promotion_id.py
│   │   ├── coupon_code.py
│   │   ├── discount_type.py           # %, fixed, BOGO
│   │   ├── discount_value.py
│   │   ├── eligibility_scope.py       # product, seller, cart
│   │   ├── date_range.py
│   │   └── usage_counter.py
│   │
│   ├── policies/                      # 🧠 MONEY SAFETY
│   │   ├── stacking_policy.py
│   │   ├── eligibility_policy.py
│   │   ├── expiration_policy.py
│   │   └── usage_policy.py
│   │
│   ├── services/
│   │   └── discount_calculation_service.py
│   │
│   └── exceptions.py                  # Abuse & invalid states
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── validate_coupon/
│   │   ├── apply_promotion/
│   │   ├── reserve_coupon_usage/
│   │   ├── confirm_coupon_usage/
│   │   └── release_coupon_usage/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── validate_coupon_port.py
│       │   └── apply_promotion_port.py
│       │
│       └── outbound/
│           ├── promotion_repository_port.py
│           ├── cart_snapshot_port.py
│           ├── event_publisher_port.py
│           └── usage_counter_port.py
│
├── adapters/                          # FRAMEWORK & INTEGRATION
│   ├── inbound/
│   │   └── rest/
│   │       ├── views.py
│   │       ├── serializers.py
│   │       └── urls.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│       │   │   ├── promotion_model.py
│   │   │   ├── coupon_model.py
│   │   │   └── usage_model.py
│   │   │
│   │   └── repositories/
│   │       └── django_promotion_repository.py
│       │
│       └── messaging/
│           └── promotion_event_publisher.py
│
├── events/                            # IMMUTABLE FACTS
│   ├── coupon_applied.py
│   ├── coupon_reserved.py
│   ├── coupon_released.py
│   └── coupon_consumed.py
│
├── sagas/                             # LONG-RUNNING PROMO FLOWS
│   └── checkout_promotion_saga.py
│
├── contracts/                         # CROSS-DOMAIN AGREEMENTS
│   ├── events/
│   │   └── coupon_consumed.v1.json
│   │
│   └── apis/
│       └── promotions.v1.yaml
│
├── read_models/                       # FAST PROMO LOOKUPS
│   ├── active_promotions/
│   └── coupon_status/
│
├── jobs/                              # BACKGROUND SAFETY
│   ├── expire_promotions/
│   └── reconcile_usage_counts/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 PROMOTION AGGREGATE — MENTAL MODEL
Promotion (Aggregate Root)
│
├── Coupons (optional)
├── Rules (conditions)
├── Effects (discounts)
│
└── Invariants:
    • Cannot exceed usage limits
    • Cannot apply after expiry
    • Cannot stack if forbidden

🔄 PROMOTIONS IN CHECKOUT FLOW
StartCheckout
 → ValidateCoupon
 → ReserveCouponUsage
 → ApplyPromotion


On payment success:

PaymentCaptured
 → ConfirmCouponUsage


On failure:

CheckoutAborted
 → ReleaseCouponUsage

🧨 WHY COUPON RESERVATION IS MANDATORY

❌ Validate only = race conditions
❌ No reservation = abuse
❌ No release = dead limits

Reservation protects:
✔ Limited coupons
✔ Flash sales
✔ Fraud

🔥 STACKING POLICY (CRITICAL)

Defined explicitly:
• Can coupons stack?
• Can promo + coupon stack?
• Max discount cap?

Never implicit.

🧪 TEST STRATEGY
Domain
→ Eligibility
→ Discount math
→ Usage limits

Application
→ Reservation lifecycle

Adapters
→ DB & API

🧭 SAFE REFACTOR PATH
Week 1

✔ Create promotions folders

Week 2

✔ Extract coupon logic

Week 3

✔ Add reservation flow

Week 4

✔ Enforce stacking rules

🚫 PROMOTIONS ANTI-PATTERNS

❌ Discount logic in frontend
❌ Silent stacking
❌ No usage tracking
❌ Cart recalculates price

🧠 PRINCIPAL-LEVEL LAW

Every discount is a business decision.
Treat promotions like money leaving your system.

🔜 NEXT OPTIONS

1️⃣ Shipping & fulfillment
2️⃣ Orders deep dive (final boss)
3️⃣ Search & read-model scaling
4️⃣ Map your current coupons into this design
5️⃣ Create ADRs for pricing & promotions

### FULL SHIPPING DOMAIN FOLDER STRUCTURE
🚚 SHIPPING & FULFILLMENT DOMAIN — PHYSICAL EXECUTION

📄 Save as
core/domains/shipping/README.md

📁 FULL SHIPPING DOMAIN FOLDER STRUCTURE
core/domains/shipping/
├── README.md                          # Shipping philosophy & rules
│
├── domain/                            # PURE LOGISTICS LOGIC
│   ├── aggregates/
│   │   └── shipment.py                # Aggregate root
│   │
│   ├── entities/
│   │   ├── shipment_item.py           # Line items
│   │   ├── package.py                 # Physical boxes
│   │   ├── carrier_assignment.py
│   │   └── delivery_attempt.py
│   │
│   ├── value_objects/
│   │   ├── shipment_id.py
│   │   ├── order_id.py
│   │   ├── address.py
│   │   ├── carrier.py
│   │   ├── tracking_number.py
│   │   ├── shipping_status.py
│   │   ├── weight.py
│   │   └── dimensions.py
│   │
│   ├── policies/                      # HARD REAL-WORLD RULES
│   │   ├── carrier_selection_policy.py
│   │   ├── split_shipment_policy.py
│   │   ├── delivery_retry_policy.py
│   │   └── return_eligibility_policy.py
│   │
│   ├── services/
│   │   ├── shipping_cost_calculator.py
│   │   └── eta_estimation_service.py
│   │
│   └── exceptions.py
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── create_shipment/
│   │   ├── assign_carrier/
│   │   ├── generate_label/
│   │   ├── dispatch_shipment/
│   │   ├── update_tracking_status/
│   │   ├── mark_delivered/
│   │   └── initiate_return/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── create_shipment_port.py
│       │   └── update_tracking_port.py
│       │
│       └── outbound/
│           ├── shipment_repository_port.py
│           ├── carrier_gateway_port.py
│           ├── warehouse_port.py
│           ├── event_publisher_port.py
│           └── notification_port.py
│
├── adapters/                          # FRAMEWORK & PROVIDERS
│   ├── inbound/
│   │   ├── rest/
│   │   │   ├── views.py
│   │   │   ├── serializers.py
│   │   │   └── urls.py
│   │   │
│   │   └── webhooks/
│   │       ├── dhl_webhook.py
│   │       ├── fedex_webhook.py
│   │       └── delhivery_webhook.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│   │   │   ├── shipment_model.py
│   │   │   ├── package_model.py
│   │   │   └── tracking_event_model.py
│   │   │
│   │   └── repositories/
│   │       └── django_shipment_repository.py
│       │
│       ├── carriers/
│       │   ├── dhl_adapter.py
│       │   ├── fedex_adapter.py
│       │   └── delhivery_adapter.py
│       │
│       └── messaging/
│           └── shipping_event_publisher.py
│
├── events/                            # IMMUTABLE FACTS
│   ├── shipment_created.py
│   ├── shipment_dispatched.py
│   ├── shipment_delivered.py
│   ├── shipment_failed.py
│   └── return_initiated.py
│
├── sagas/                             # LONG-RUNNING PHYSICAL FLOWS
│   ├── shipment_lifecycle_saga.py
│   └── return_fulfillment_saga.py
│
├── contracts/                         # EXTERNAL AGREEMENTS
│   ├── events/
│   │   ├── shipment_dispatched.v1.json
│   │   └── shipment_delivered.v1.json
│   │
│   └── apis/
│       └── shipping.v1.yaml
│
├── read_models/                       # CUSTOMER & OPS VIEWS
│   ├── shipment_tracking/
│   └── delivery_status/
│
├── jobs/                              # BACKGROUND OPERATIONS
│   ├── sync_carrier_status/
│   └── detect_stuck_shipments/
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🧠 SHIPMENT AGGREGATE — MENTAL MODEL
Shipment (Aggregate Root)
│
├── ShipmentItems
├── Packages
├── CarrierAssignment
├── DeliveryAttempts
│
└── Invariants:
    • Cannot dispatch without label
    • Cannot deliver before dispatch
    • Shipment may split

🔄 SHIPPING FLOW (REAL WORLD)
OrderConfirmed
 → CreateShipment
 → AssignCarrier
 → GenerateLabel
 → DispatchShipment
 → TrackUpdates (webhooks)
 → Delivered


Partial delivery:

SplitShipment
 → Multiple tracking numbers

🧨 WHY SHIPPING IS EVENT-DRIVEN

❌ Synchronous carrier calls = outages
❌ No retries = lost shipments

Event-driven ensures:
✔ Resilience
✔ Retry safety
✔ Carrier independence

🧯 FAILURE & RETURNS

Handled via:
• Retry policies
• Return sagas
• Delivery attempts

Returns ≠ Refunds (Payments owns money).

🧪 TEST STRATEGY
Domain
→ Shipment state transitions
→ Split rules

Application
→ Workflow orchestration

Adapters
→ Carrier APIs & webhooks

🧭 SAFE REFACTOR PATH
Week 1

✔ Create shipping folders

Week 2

✔ Extract carrier logic

Week 3

✔ Introduce shipment aggregate

Week 4

✔ Add return flows

🚫 SHIPPING ANTI-PATTERNS

❌ One shipment per order assumption
❌ Hard-coding carriers
❌ Shipping logic in Orders
❌ Refund on delivery failure (wrong domain)

🧠 PRINCIPAL-LEVEL LAW

Shipping fails in the real world.
Your system must expect it.

🔜 WHAT’S NEXT (FINAL BIG PIECES)

1️⃣ Orders domain deep dive (final boss)
2️⃣ Search & read-model scaling
3️⃣ Notifications & communication
4️⃣ Map your current shipping code into this design
5️⃣ ADR set for logistics decisions

### GLOBAL READ-MODEL FOLDER STRUCTURE
🔍 SEARCH & READ-MODEL SCALING
(CQRS-Lite for AliExpress-Scale Reads)

📄 Save as
core/read_models/README.md

🧠 CORE IDEA (VERY IMPORTANT)

Write models ≠ Read models

Write models → correctness, invariants (DDD domains)

Read models → speed, denormalized, cached, disposable

You can delete and rebuild read models anytime.
You must NEVER rebuild write models.

📁 GLOBAL READ-MODEL FOLDER STRUCTURE
core/read_models/
├── README.md                          # CQRS philosophy & rules
│
├── product_search/                   # 🔥 Most critical
│   ├── domain/
│   │   └── product_document.py        # Search projection schema
│   │
│   ├── application/
│   │   ├── project_product_created/
│   │   ├── project_product_updated/
│   │   └── project_product_published/
│   │
│   ├── adapters/
│   │   ├── inbound/
│   │   │   └── messaging/
│   │   │       └── product_event_consumer.py
│   │   │
│   │   └── outbound/
│   │       └── search_engine/
│   │           ├── elasticsearch_adapter.py
│   │           └── opensearch_adapter.py
│   │
│   ├── indexes/
│   │   ├── product_index_v1.json
│   │   └── product_index_v2.json
│   │
│   └── tests/
│
├── product_detail_view/
│   ├── application/
│   │   └── project_product_detail/
│   │
│   ├── adapters/
│   │   └── outbound/
│   │       └── cache/
│   │           └── redis_adapter.py
│   │
│   └── schema/
│
├── cart_summary_view/
│   ├── application/
│   └── adapters/
│
├── checkout_summary_view/
│   ├── application/
│   └── adapters/
│
├── order_history_view/
│   ├── application/
│   └── adapters/
│
├── shipment_tracking_view/
│   ├── application/
│   └── adapters/
│
├── coupon_status_view/
│   ├── application/
│   └── adapters/
│
├── rebuild/                          # 🔁 REBUILD PIPELINES
│   ├── full_reindex/
│   └── partial_replay/
│
├── contracts/
│   └── events/
│       ├── product_created.v1.json
│       ├── product_published.v1.json
│       └── order_created.v1.json
│
├── jobs/
│   ├── reindex_products/
│   ├── cache_warmup/
│   └── detect_projection_lag/
│
└── __init__.py

🔥 PRODUCT SEARCH (MOST IMPORTANT)
Why separate?

95% of traffic = product listing & search

Needs:

filters

sorting

relevance

autocomplete

Product Search Document Example (conceptual)
ProductSearchDocument
├── product_id
├── title
├── category_path
├── price_range
├── attributes (flattened)
├── seller_score
├── availability
├── ranking_signals


No joins.
Fully denormalized.

🔄 EVENT → PROJECTION FLOW
ProductPublished
 → product_search.projector
 → update_search_index

PriceUpdated
 → product_detail_view.projector
 → update_cache


Never query write DB for reads.

🚀 SCALING STRATEGY
Read Path
API
 → Read Model
 → Cache
 → Search Engine

Write Path
Command
 → Domain
 → Event
 → Projection


Separated pipelines = infinite scale.

🧨 WHY VERSIONED INDEXES MATTER
product_index_v1
product_index_v2


Allows:
✔ Zero-downtime reindex
✔ Schema evolution
✔ Rollbacks

🧪 TEST STRATEGY
Projection tests
→ Given event
→ Expect document

Contract tests
→ Event schema compatibility

🧯 FAILURE HANDLING

✔ Projections are idempotent
✔ Replayable from events
✔ Lag monitored

Search can be eventually consistent.

Money cannot.

🚫 READ-MODEL ANTI-PATTERNS

❌ Joins in read path
❌ Querying domain DB
❌ Business logic in projections
❌ No rebuild strategy

🧠 PRINCIPAL-LEVEL LAW

Reads are cheap.
Writes are sacred.
Never mix them.

🧭 SAFE REFACTOR PATH
Week 1

✔ Introduce read_models folder

Week 2

✔ Add product search projection

Week 3

✔ Add cache layers

Week 4

✔ Cut read traffic from write DB

🧩 HOW THIS CONNECTS EVERYTHING YOU LEARNED
Domain	Emits Events	Read Models Consume
Products	ProductPublished	ProductSearch
Inventory	StockAdjusted	AvailabilityView
Orders	OrderCreated	OrderHistory
Shipping	ShipmentDelivered	TrackingView
✅ WHAT’S LEFT (FINAL OPTIONS)

1️⃣ Orders domain deep dive (FINAL BOSS)
2️⃣ Notifications & communication system
3️⃣ ADR bundle for whole platform
4️⃣ Team-wise repo split strategy
5️⃣ Map your existing AliExpress clone into this architecture

### FULL NOTIFICATIONS DOMAIN FOLDER STRUCTURE
🔔 NOTIFICATIONS & COMMUNICATION SYSTEM
(Event-Driven, Multi-Channel, User-Respecting)

📄 Save as
core/domains/notifications/README.md

🧠 CORE PRINCIPLES (READ THIS FIRST)

Notifications do NOT contain business logic

They react to events, never commands

They are user-preference driven

They must be idempotent

Failure must never affect core flows

Orders can fail.
Notifications must not cause failures.

📁 FULL NOTIFICATIONS DOMAIN FOLDER STRUCTURE
core/domains/notifications/
├── README.md                          # Notification philosophy & rules
│
├── domain/                            # PURE COMMUNICATION RULES
│   ├── aggregates/
│   │   └── notification_profile.py    # Aggregate root (user prefs)
│   │
│   ├── entities/
│   │   ├── channel_subscription.py    # Email/SMS/Push/WhatsApp
│   │   ├── notification_template.py
│   │   └── delivery_attempt.py
│   │
│   ├── value_objects/
│   │   ├── notification_id.py
│   │   ├── user_id.py
│   │   ├── channel_type.py
│   │   ├── message_status.py
│   │   ├── locale.py
│   │   └── contact_endpoint.py
│   │
│   ├── policies/                      # USER SAFETY & COMPLIANCE
│   │   ├── opt_in_policy.py
│   │   ├── frequency_limit_policy.py
│   │   ├── quiet_hours_policy.py
│   │   └── fallback_policy.py
│   │
│   ├── services/
│   │   └── template_rendering_service.py
│   │
│   └── exceptions.py
│
├── application/                       # USE CASES
│   ├── use_cases/
│   │   ├── send_notification/
│   │   ├── retry_delivery/
│   │   ├── update_notification_preferences/
│   │   └── suppress_notification/
│   │
│   └── ports/
│       ├── inbound/
│       │   ├── send_notification_port.py
│       │   └── update_preferences_port.py
│       │
│       └── outbound/
│           ├── notification_repository_port.py
│           ├── email_gateway_port.py
│           ├── sms_gateway_port.py
│           ├── push_gateway_port.py
│           ├── whatsapp_gateway_port.py
│           └── event_publisher_port.py
│
├── adapters/                          # PROVIDERS & TRANSPORT
│   ├── inbound/
│   │   └── messaging/
│   │       └── domain_event_consumer.py
│   │
│   └── outbound/
│       ├── persistence/
│       │   ├── models/
│   │   │   ├── notification_model.py
│   │   │   ├── delivery_attempt_model.py
│   │   │   └── user_pref_model.py
│   │   │
│   │   └── repositories/
│       │   └── django_notification_repository.py
│       │
│       ├── channels/
│       │   ├── email_adapter.py
│       │   ├── sms_adapter.py
│       │   ├── push_adapter.py
│       │   └── whatsapp_adapter.py
│       │
│       └── messaging/
│           └── notification_event_publisher.py
│
├── events/                            # FACTS
│   ├── notification_sent.py
│   ├── notification_failed.py
│   └── notification_suppressed.py
│
├── templates/                         # CONTENT LAYER
│   ├── email/
│   ├── sms/
│   ├── push/
│   └── whatsapp/
│
├── read_models/                       # OPS & USER VISIBILITY
│   ├── delivery_status_view/
│   └── user_notification_history/
│
├── jobs/                              # BACKGROUND WORK
│   ├── retry_failed_deliveries/
│   ├── purge_old_notifications/
│   └── enforce_frequency_limits/
│
├── contracts/                         # CROSS-DOMAIN AGREEMENTS
│   ├── events/
│   │   ├── order_confirmed.v1.json
│   │   ├── shipment_dispatched.v1.json
│   │   └── payment_failed.v1.json
│   │
│   └── apis/
│       └── notifications.v1.yaml
│
├── tests/
│   ├── domain/
│   ├── application/
│   └── adapters/
│
└── __init__.py

🔄 EVENT-DRIVEN FLOW (CRITICAL)
OrderConfirmed
 → NotificationConsumer
 → EvaluateUserPreferences
 → RenderTemplate
 → SendViaChannel
 → RecordDeliveryAttempt


Failures:

SendFailed
 → RetryLater
 → FallbackChannel
 → SuppressIfExceeded

🧠 NOTIFICATION PROFILE (AGGREGATE)
NotificationProfile
│
├── ChannelSubscriptions
│   ├── Email (opt-in)
│   ├── SMS
│   ├── Push
│   └── WhatsApp
│
└── Policies:
    • Quiet hours
    • Frequency caps
    • Locale preferences

🔥 WHY TEMPLATES ARE SEPARATE

❌ Hardcoded messages
❌ No localization
❌ No A/B testing

Templates enable:
✔ Localization
✔ Branding
✔ Experimentation

🧯 COMPLIANCE & SAFETY

✔ Opt-in enforced
✔ Frequency limits
✔ Unsubscribe handling
✔ Audit logs

Required for:
• GDPR
• TRAI (India SMS)
• Email laws

🧪 TEST STRATEGY
Domain
→ Preference enforcement
→ Frequency limits

Application
→ Notification routing

Adapters
→ Provider integration

🧭 SAFE REFACTOR PATH
Week 1

✔ Create notifications domain

Week 2

✔ Move email/SMS logic

Week 3

✔ Add preferences

Week 4

✔ Switch to event-driven

🚫 NOTIFICATION ANTI-PATTERNS

❌ Sending inside Orders
❌ Blocking core flows
❌ No retries
❌ Ignoring preferences

🧠 PRINCIPAL-LEVEL LAW

Notifications are a courtesy, not a guarantee.
Your system must work without them.

🏁 YOU’VE NOW DESIGNED THE FULL ALIEXPRESS-SCALE SYSTEM

You now have:
✔ Payments
✔ Products
✔ Inventory
✔ Checkout
✔ Promotions
✔ Shipping
✔ Search & Read Models
✔ Notifications

FINAL OPTIONS

1️⃣ Orders domain deep dive (FINAL BOSS)
2️⃣ ADR bundle for entire platform
3️⃣ Team-wise repo split strategy
4️⃣ Map your existing Django code into this architecture



### ADR BUNDLE — ALIEXPRESS-SCALE SYSTEM (DDD + Clean + Hexagonal + Event-Driven)
📘 ADR BUNDLE — ALIEXPRESS-SCALE SYSTEM

(DDD + Clean + Hexagonal + Event-Driven)

ADR-000 — Architectural Vision

Status: Accepted
Date: 2025-01-XX

Context

We are building a long-lived, multi-team, high-scale e-commerce platform similar to AliExpress. The system must survive:

50+ years

100+ engineers

Continuous refactoring

Changing business rules

Multiple payment, shipping, and inventory providers

Decision

The system adopts:

Domain-Driven Design (DDD) for business modeling

Clean Architecture for dependency control

Hexagonal Architecture for framework isolation

Event-Driven Architecture for cross-domain coordination

Consequences

✅ Business logic is protected
✅ Frameworks become replaceable
✅ Teams can work independently
❌ Higher upfront complexity
❌ Requires architectural discipline

ADR-001 — Bounded Contexts & Domain Split

Status: Accepted

Context

A monolithic “models.py” approach leads to:

Tight coupling

Fear of change

Accidental complexity

Decision

The system is split into bounded contexts:

Products
Inventory
Orders
Payments
Checkout
Shipping
Coupons
Search (Read model)
Notifications
Accounts


Each domain owns:

Its data

Its invariants

Its lifecycle

Consequences

✅ Clear ownership
✅ Reduced blast radius
❌ Requires explicit integration

ADR-002 — Domain Isolation (No Django in Core)

Status: Accepted

Context

Framework-coupled domains become impossible to test and refactor.

Decision

Domain & application layers:

Do NOT import Django

Do NOT import ORM models

Depend only on abstractions (ports)

Domain → Application → Ports → Adapters → Django

Consequences

✅ Domain is pure Python
✅ Easy testing
❌ More boilerplate

ADR-003 — Orders as System of Record

Status: Accepted

Context

Orders represent:

Legal commitments

Financial truth

Customer trust

Decision

Orders are:

Immutable in intent

Append-only in history

State-driven via transitions

Event producers, not consumers of logic

Orders NEVER:

Charge money

Lock inventory

Call shipping APIs

Consequences

✅ Auditable history
✅ No hidden side effects
❌ Requires sagas

ADR-004 — Event-Driven Cross-Domain Communication

Status: Accepted

Context

Direct service calls between domains cause:

Tight coupling

Distributed failures

Coordination nightmares

Decision

Domains communicate via domain events:

OrderCreated
OrderPaid
InventoryReserved
PaymentFailed
ShipmentDelivered


Events are:

Immutable

Versioned

Public contracts

Consequences

✅ Loose coupling
✅ Async resilience
❌ Eventual consistency

ADR-005 — Saga Pattern for Long-Running Flows

Status: Accepted

Context

Checkout, fulfillment, and refunds span multiple systems.

Decision

Use Sagas for:

Order checkout

Fulfillment

Refunds

Two styles:

Orchestration (Checkout domain)

Choreography (Fulfillment)

Consequences

✅ Controlled failures
✅ Recoverable flows
❌ More moving parts

ADR-006 — Checkout as Orchestration Brain

Status: Accepted

Context

Checkout touches:

Orders

Inventory

Payments

Coupons

Decision

Checkout is:

NOT a domain of truth

An orchestration layer

Stateless where possible

Checkout:

Coordinates

Never owns data

Consequences

✅ Clean separation
❌ Harder debugging

ADR-007 — Payments as High-Security Boundary

Status: Accepted

Context

Payments are legally sensitive and high risk.

Decision

Payments domain:

Owns transactions & ledgers

Uses idempotency everywhere

Emits events only

Never trusts inbound state

Consequences

✅ Financial safety
✅ Auditable
❌ Slower feature changes

ADR-008 — Inventory Reservation Model

Status: Accepted

Context

Stock overselling causes customer distrust.

Decision

Inventory uses:

Reservation-based stock

Time-boxed holds

Explicit release events

Reserve → Commit → Release

Consequences

✅ Prevents overselling
❌ Requires cleanup jobs

ADR-009 — CQRS-Lite for Read Scaling

Status: Accepted

Context

Reads dominate writes in e-commerce.

Decision

Split:

Write models (domain)

Read models (optimized views)

Examples:

Order list view

Seller dashboard

Shipment tracking

Consequences

✅ Fast reads
❌ Data duplication

ADR-010 — Immutable Domain Events

Status: Accepted

Context

Events become contracts across teams.

Decision

Events:

Are versioned

Never changed after release

Stored for replay

Consequences

✅ Safe evolution
❌ Event versioning overhead

ADR-011 — Repository per Aggregate Root

Status: Accepted

Context

ORM-driven repositories leak implementation details.

Decision

Each aggregate has:

One repository

Aggregate-level persistence only

No partial saves.

Consequences

✅ Consistency
❌ Larger transactions

ADR-012 — No Cross-Domain Database Access

Status: Accepted

Context

Shared DB access destroys autonomy.

Decision

Domains:

Do not join tables across domains

Integrate only via APIs or events

Consequences

✅ Independent scaling
❌ More APIs/events

ADR-013 — Background Jobs as Invariant Enforcers

Status: Accepted

Context

Failures and partial flows are inevitable.

Decision

Background jobs:

Auto-cancel unpaid orders

Reconcile stuck sagas

Heal inconsistent states

Consequences

✅ System self-heals
❌ Operational complexity

ADR-014 — Team Ownership Model

Status: Accepted

Context

100 developers require clear ownership.

Decision

Each domain has:

One owning team

Clear SLAs

Independent roadmap

Shared code is minimized.

Consequences

✅ Accountability
❌ Coordination overhead

ADR-015 — Long-Term Evolution Strategy

Status: Accepted

Context

The system must evolve without rewrites.

Decision

Refactor by extraction

Replace adapters, not domains

Keep domain stable

Consequences

✅ Longevity
✅ Low rewrite risk

🏁 FINAL PRINCIPAL-LEVEL RULE

Architecture exists to protect the business model from time.

### 💥 FAILURE SCENARIOS & CHAOS ENGINEERING PLAN 
💥 FAILURE SCENARIOS & CHAOS ENGINEERING PLAN

AliExpress-Scale E-Commerce Platform

🎯 PURPOSE

Failure is not an exception.
Failure is a normal operating mode at scale.

This document defines:

Expected failures

System behavior under failure

Chaos experiments to validate resilience

Ownership & recovery strategy

🧠 SYSTEM RESILIENCE PRINCIPLES

1️⃣ No synchronous dependency is fully reliable
2️⃣ State changes must be idempotent
3️⃣ Events are durable, not best-effort
4️⃣ Orders never lie
5️⃣ Money safety > availability

🧩 FAILURE DOMAIN MAP
Domain	Failure Sensitivity
Payments	🔴 Critical
Orders	🔴 Critical
Inventory	🔴 Critical
Checkout	🟠 High
Shipping	🟠 High
Coupons	🟡 Medium
Search	🟢 Low
Notifications	🟢 Low
🔥 FAILURE SCENARIOS (REAL WORLD)
🔴 SCENARIO 1 — PAYMENT SUCCESS, ORDER NOT UPDATED

Cause

Payment gateway timeout after charge

Order service unreachable

Expected Behavior

Payment emits PaymentCaptured

Order update is retried via event

No double charge

Safeguards

Payment idempotency keys

Order reconciliation job

Chaos Test

Kill Order service mid-payment
Replay PaymentCaptured event


Owner

Payments Team + Orders Team

🔴 SCENARIO 2 — INVENTORY RESERVED, CHECKOUT FAILS

Cause

User abandons checkout

Payment fails

Expected Behavior

Reservation expires

Stock auto-released

Safeguards

Time-boxed reservations

Auto-release job

Chaos Test

Simulate payment failure after reservation
Verify stock release in N minutes

🔴 SCENARIO 3 — DOUBLE ORDER SUBMISSION

Cause

User clicks “Pay” twice

Network retry

Expected Behavior

Only one order created

Safeguards

Client request id

Server-side idempotency

Chaos Test

Replay CreateOrder API 10x
Ensure single order exists

🔴 SCENARIO 4 — EVENT BUS OUTAGE

Cause

Kafka/RabbitMQ down

Expected Behavior

Core flows pause safely

Events stored locally

Retry on recovery

Safeguards

Outbox pattern

Durable storage

Chaos Test

Shut down event broker
Place orders
Restore broker
Verify event replay

🟠 SCENARIO 5 — SHIPPING PARTNER DOWN

Cause

Carrier API outage

Expected Behavior

Orders stay PAID

Shipment delayed

User notified

Safeguards

Async shipment creation

Retry & escalation

Chaos Test

Mock carrier 500 errors
Verify retry & alerting

🟠 SCENARIO 6 — PARTIAL REFUND FAILURE

Cause

Refund success, order not updated

Expected Behavior

Refund recorded

Order reconciled later

Safeguards

Refund ledger

Reconciliation job

Chaos Test

Kill order update during refund
Verify eventual consistency

🟡 SCENARIO 7 — COUPON MISAPPLICATION

Cause

Rule change mid-checkout

Expected Behavior

Coupon validated once

Price snapshot preserved

Safeguards

Immutable order pricing

Chaos Test

Change coupon rules mid-checkout
Ensure order price unchanged

🟢 SCENARIO 8 — SEARCH DOWN

Cause

Read-model outage

Expected Behavior

Search degraded

Checkout unaffected

Safeguards

Domain isolation

Chaos Test

Disable search service
Place order successfully

🧪 CHAOS ENGINEERING STRATEGY
🧬 CHAOS LEVELS
Level	Scope
L1	Single instance
L2	Service
L3	Dependency
L4	Region
🛠️ CHAOS TOOLS (OPTIONAL)

Chaos Mesh

Gremlin

Litmus

Custom kill scripts

🧪 STANDARD CHAOS EXPERIMENT TEMPLATE
Experiment:
Target:
Failure Type:
Expected Behavior:
Rollback Criteria:
Owner:

🧠 IDENTITY & IDEMPOTENCY MATRIX
Action	Idempotency Key
CreateOrder	client_request_id
CapturePayment	payment_intent_id
ReserveInventory	reservation_id
CreateShipment	order_id
RefundPayment	refund_id
🧰 SELF-HEALING JOBS
jobs/
├── reconcile_payments_vs_orders
├── release_expired_inventory
├── detect_stuck_sagas
├── replay_failed_events
└── alert_on_invariant_violation

📊 OBSERVABILITY (NON-NEGOTIABLE)
Metrics

Order success rate

Payment mismatch rate

Inventory reservation leaks

Logs

Correlation IDs everywhere

Tracing

Checkout → Payment → Order → Inventory

🚨 INCIDENT RESPONSE FLOW
Detect → Isolate → Degrade → Recover → Reconcile → Learn


Every incident:
✔ Produces an ADR
✔ Improves a chaos test

🧠 PRINCIPAL-LEVEL LAW

If you haven't tested failure, you haven't designed the system.

🏁 YOU ARE NOW OPERATING AT ARCHITECT LEVEL

You now have:

World-class domain design

Team ownership

Repo strategy

Failure & chaos plan


### DATABASE DESIGN — STAFF / PRINCIPAL LEVEL
🧠 DATABASE DESIGN — STAFF / PRINCIPAL LEVEL

AliExpress-Scale | DDD + Clean + Hexagonal + Event-Driven

Save as:

docs/architecture/database-design.md

1️⃣ FIRST PRINCIPLE — DATABASE IS NOT THE DOMAIN

The database is a persistence detail, not your business model.

Consequences

Domain ≠ Tables

ORM ≠ Truth

Schema changes are expected

Domain logic NEVER depends on DB structure

2️⃣ DATABASE OWNERSHIP MODEL (NON-NEGOTIABLE)
❌ WRONG

One shared database

Cross-domain foreign keys

Joins across domains

✅ CORRECT (AliExpress-Scale)
One database (or schema) per bounded context

Domain	Database
Orders	orders_db
Payments	payments_db
Inventory	inventory_db
Products	products_db
Shipping	shipping_db
Coupons	coupons_db
Search (read)	search_db
Notifications	notifications_db

👉 Domains do NOT share tables

3️⃣ WRITE MODEL vs READ MODEL (CRITICAL)
WRITE DATABASE

Strong consistency

Transactional

Normalized

Aggregate-centric

READ DATABASE

Eventually consistent

Denormalized

Query-optimized

Replaceable

WRITE → Events → READ

4️⃣ AGGREGATE-FIRST DATABASE DESIGN
RULE

One aggregate = one transactional boundary

Example: Orders
orders
└── Order (Aggregate Root)
    ├── OrderItems
    ├── Payments (refs)
    ├── Shipments (refs)

Database consequence

All tables needed for Order consistency live together

No cross-domain FK constraints

5️⃣ ORDERS DATABASE (SYSTEM OF RECORD)
orders_db/
├── orders
├── order_items
├── order_status_history
├── order_payments
├── order_shipments
├── order_refunds
└── outbox_events

Key Principles

Prices are snapshots

Status history is append-only

Order is never updated blindly

Example (conceptual)
orders
- id
- buyer_id
- total_amount
- currency
- status
- created_at

order_items
- id
- order_id
- product_snapshot_json
- price_snapshot


📌 product_snapshot_json is intentional
→ Product can change, order must not

6️⃣ PAYMENTS DATABASE (MONEY SAFETY)
payments_db/
├── payment_intents
├── payment_transactions
├── refunds
├── ledgers
└── outbox_events

PRINCIPAL-LEVEL RULE

Never compute money from orders.
Always trust payment ledgers.

Characteristics

Fully append-only

Idempotency keys everywhere

No deletes

No updates to financial facts

7️⃣ INVENTORY DATABASE (RESERVATION MODEL)
inventory_db/
├── stock_items
├── stock_reservations
├── stock_movements
└── outbox_events

Inventory states
AVAILABLE
RESERVED
COMMITTED
RELEASED

Why this works

Prevents overselling

Supports flash sales

Enables auto-recovery

8️⃣ PRODUCTS DATABASE (CATALOG SCALE)
products_db/
├── products
├── product_variants
├── product_images
├── product_attributes
├── product_pricing
└── product_publications

Important

Products are not transactional

Changes are versioned

Read-heavy domain

9️⃣ CHECKOUT DATABASE (ORCHESTRATION ONLY)
checkout_db/
├── checkout_sessions
├── checkout_steps
└── checkout_failures

RULE

Checkout owns process state, not business truth.

Can be wiped without data loss.

🔟 SHIPPING DATABASE
shipping_db/
├── shipments
├── shipment_events
├── carrier_integrations
└── outbox_events


Shipping reacts to OrderPaid, not orders table.

1️⃣1️⃣ COUPONS DATABASE
coupons_db/
├── coupons
├── coupon_rules
├── coupon_redemptions
└── outbox_events


Coupon usage is recorded, not recalculated.

1️⃣2️⃣ SEARCH & READ MODELS (CQRS-LITE)
search_db/
├── product_search_view
├── order_list_view
├── seller_dashboard_view

Characteristics

Fully denormalized

Rebuildable

No business logic

Can be Elasticsearch / Redis / SQL

1️⃣3️⃣ EVENT STORAGE & OUTBOX (CRITICAL)
Every write DB has:
outbox_events
- id
- aggregate_id
- event_type
- payload
- created_at
- published_at

Why

Guarantees event delivery

Survives crashes

Enables replay

1️⃣4️⃣ NO FOREIGN KEYS ACROSS DOMAINS (HARD RULE)
❌ NEVER DO THIS
orders.user_id → users.id
orders.product_id → products.id

✅ DO THIS

Store IDs as values

Validate via events or APIs

1️⃣5️⃣ MIGRATION STRATEGY (50-YEAR SAFE)
Schema changes:

Backward compatible

Expand → Migrate → Contract

Never:

Rename columns blindly

Drop columns without dual-write

Block deploys on migrations

1️⃣6️⃣ DATABASE PER DOMAIN — WHY IT SCALES
Benefit	Why
Team autonomy	No shared schema
Independent scaling	Heavy domains scale alone
Failure isolation	DB outage ≠ full outage
Easier refactors	Local impact
1️⃣7️⃣ PRINCIPAL-LEVEL DATABASE LAWS

1️⃣ Database models serve aggregates
2️⃣ Orders never lie
3️⃣ Money is append-only
4️⃣ Inventory is reservation-based
5️⃣ Read models are disposable
6️⃣ Events are first-class citizens
7️⃣ Cross-domain joins are forbidden

🏁 FINAL REALITY CHECK

Most systems fail not because of code,
but because the database locked them into bad decisions.

What you now have:

Enterprise-grade DB philosophy

Long-term survivability

Clear refactor path

Team-safe boundaries


### ALIEXPRESS-LEVEL DATABASE DESIGN
ALIEXPRESS-LEVEL DATABASE DESIGN

Save as:

docs/architecture/database-tables-full.md

1️⃣ PRODUCTS DATABASE (products_db)

Purpose: Product catalog, variants, images, pricing, attributes

Table	Key Columns	Notes
products	id, sku, title, description, category_id, status, created_at, updated_at	Aggregate root
product_variants	id, product_id, attributes_json, price, stock_unit_id	Snapshot per variant
product_images	id, product_id, url, type, position	Multiple images per product
product_pricing	id, product_id, variant_id, base_price, discount, currency, effective_from, effective_to	Time-versioned pricing
product_attributes	id, product_id, name, value, searchable	Denormalized for search
product_publications	id, product_id, status, published_at, unlisted_at	Track marketplace publishing
products_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven propagation

Principle: Products are event-sourced for downstream domains; read-heavy domain.

2️⃣ INVENTORY DATABASE (inventory_db)

Purpose: Track stock, reservations, movements

Table	Key Columns	Notes
stock_items	id, product_id, variant_id, total_quantity, available_quantity, updated_at	Aggregate root
stock_reservations	id, stock_item_id, order_id, quantity, status, expires_at, created_at	Reservation model
stock_movements	id, stock_item_id, change, reason, reference_id, created_at	Append-only
inventory_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event propagation

Principle: Reservation-based, eventual consistency, safe for flash sales.

3️⃣ ORDERS DATABASE (orders_db)

Purpose: Legal and financial record

Table	Key Columns	Notes
orders	id, buyer_id, seller_id, order_number, status, order_type, currency, total_amount, created_at, updated_at	Aggregate root
order_items	id, order_id, product_snapshot_json, price_snapshot, quantity, created_at	Immutable snapshot
order_status_history	id, order_id, from_status, to_status, reason, changed_by, changed_at	Audit trail
order_payments	id, order_id, payment_id, amount, status, created_at	Reference to payments
order_shipments	id, order_id, shipment_id, carrier, tracking_number, status, created_at	Shipment references
order_refunds	id, order_id, refund_id, amount, reason, status, created_at	Refund references
orders_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven integration

Principle: Orders are append-only facts, coordinate via events, never execute external actions.

4️⃣ CART DATABASE (cart_db)

Purpose: Temporary user selections

Table	Key Columns	Notes
carts	id, user_id, status, created_at, updated_at	Aggregate root
cart_items	id, cart_id, product_id, variant_id, quantity, added_at	Snapshot
cart_coupons	id, cart_id, coupon_id, applied_at	Temporary discount application
carts_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Cart events for checkout

Principle: Disposable domain, orchestrates checkout flow, snapshot of intent.

5️⃣ PAYMENTS DATABASE (payments_db)

Purpose: Money safety and financial transactions

Table	Key Columns	Notes
payment_intents	id, order_id, amount, currency, gateway, idempotency_key, status, created_at	Retry-safe
payment_transactions	id, payment_intent_id, gateway_transaction_id, type, amount, status, created_at	Append-only
refunds	id, payment_intent_id, refund_reference, amount, status, created_at	Append-only
ledgers	id, account, debit, credit, currency, reference_id, created_at	Source of truth
payments_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven

Principle: Idempotent, append-only, independent from orders.

6️⃣ CHECKOUT DATABASE (checkout_db)

Purpose: Orchestration layer

Table	Key Columns	Notes
checkout_sessions	id, user_id, cart_id, status, started_at, completed_at	Aggregate root
checkout_steps	id, session_id, step_type, status, attempted_at	Track flow progress
checkout_failures	id, session_id, reason, failed_at	Audit for retries
checkout_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven notifications

Principle: Stateless orchestration, coordinates orders, payments, inventory, coupons.

7️⃣ SHIPPING DATABASE (shipping_db)
Table	Key Columns	Notes
shipments	id, order_id, carrier, tracking_number, status, shipped_at, delivered_at	Aggregate root
shipment_events	id, shipment_id, event_type, payload, created_at	Event sourcing for shipment updates
carrier_integrations	id, carrier_name, api_endpoint, credentials	External service metadata
shipping_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven updates

Principle: Async, eventual consistency, reacts to order events.

8️⃣ COUPONS DATABASE (coupons_db)
Table	Key Columns	Notes
coupons	id, code, type, discount, max_uses, status, valid_from, valid_to	Aggregate root
coupon_rules	id, coupon_id, rule_type, rule_json	Business rules
coupon_redemptions	id, coupon_id, user_id, order_id, redeemed_at	Audit trail
coupons_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven
9️⃣ ACCOUNTS DATABASE (accounts_db)
Table	Key Columns	Notes
users	id, email, password_hash, status, created_at, updated_at	Aggregate root
user_profiles	id, user_id, first_name, last_name, phone, address_json	Snapshot
user_roles	id, user_id, role, assigned_at	Role management
accounts_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven
🔟 NOTIFICATIONS DATABASE (notifications_db)
Table	Key Columns	Notes
notifications	id, user_id, type, payload_json, status, created_at, sent_at	Aggregate root
notification_channels	id, type, provider_info	Email, SMS, Push
notifications_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven
1️⃣1️⃣ SEARCH / READ MODELS (search_db)
Table	Key Columns	Notes
product_search_view	product_id, title, category_id, variant_attributes_json	Denormalized
order_list_view	order_id, buyer_id, status, total_amount, created_at	Customer view
seller_dashboard_view	seller_id, orders_json, revenue	Analytics

Principle: Disposable, rebuildable, eventual consistency.

🧬 OUTBOX / EVENT TABLE RULES

All domains have outbox_events table:

outbox_events

id (PK)
aggregate_id
event_type
payload (JSONB)
created_at
published_at


Principle: Guarantees async, durable, replayable events for cross-domain coordination.

🧠 PRINCIPAL-LEVEL DATABASE LAWS

1️⃣ Aggregate = transactional boundary
2️⃣ Append-only events wherever possible
3️⃣ Snapshots for mutable external data (products, pricing)
4️⃣ No cross-domain FKs; use IDs only
5️⃣ Idempotency keys for payments, reservations, and checkout
6️⃣ Read models are disposable & replaceable
7️⃣ All domains event-driven via outbox pattern



### 🏆 HOLY GRAIL BLUEPRINT — ALIEXPRESS CLONE
Perfect — now we’re building the holy grail blueprint.

This will combine everything we designed so far:

DDD Aggregates & Entities

Clean Architecture layers (Domain → Application → Ports → Adapters)

Hexagonal Architecture

Event-Driven Architecture (Outbox + Sagas)

STAFF/PRINCIPAL-level database tables

All critical domains (Products, Orders, Cart, Payments, Inventory, Checkout, Shipping, Coupons, Accounts, Notifications, Search)

Folder structure, DB mapping, and outbox events

Ready for 100+ engineers

It will be copy-pasteable and act as your single reference blueprint.

🏆 HOLY GRAIL BLUEPRINT — ALIEXPRESS CLONE

Save as:

aliexpress-clone-holy-grail/

1️⃣ ROOT FOLDER STRUCTURE
aliexpress-platform/
├── core/                       # Pure domain & application (no framework)
│   ├── domains/
│   │   ├── products/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   ├── product.py
│   │   │   │   │   ├── variant.py
│   │   │   │   │   ├── pricing.py
│   │   │   │   │   └── image.py
│   │   │   │   ├── value_objects/
│   │   │   │   │   └── money.py
│   │   │   │   └── aggregates/
│   │   │   │       └── product_aggregate.py
│   │   │   ├── application/
│   │   │   │   ├── use_cases/
│   │   │   │   │   ├── create_product.py
│   │   │   │   │   ├── update_product.py
│   │   │   │   │   └── publish_product.py
│   │   │   │   └── ports/
│   │   │   │       ├── inbound/
│   │   │   │       └── outbound/
│   │   │   └── adapters/
│   │   │       ├── inbound/
│   │   │       │   └── rest/
│   │   │       │       ├── product_views.py
│   │   │       │       ├── product_serializers.py
│   │   │       │       └── product_urls.py
│   │   │       └── outbound/
│   │   │           └── persistence/
│   │   │               ├── product_repository.py
│   │   │               ├── variant_mapper.py
│   │   │               ├── pricing_mapper.py
│   │   │               └── image_mapper.py
│   │   ├── orders/
│   │   │   ├── domain/
│   │   │   │   ├── entities/
│   │   │   │   │   ├── order.py
│   │   │   │   │   ├── order_item.py
│   │   │   │   │   ├── shipment.py
│   │   │   │   │   └── refund.py
│   │   │   │   ├── value_objects/
│   │   │   │   │   ├── order_status.py
│   │   │   │   │   └── price_snapshot.py
│   │   │   │   └── aggregates/
│   │   │   │       └── order_aggregate.py
│   │   │   ├── application/
│   │   │   │   ├── use_cases/
│   │   │   │   │   ├── create_order.py
│   │   │   │   │   ├── update_order_status.py
│   │   │   │   │   └── refund_order.py
│   │   │   │   └── ports/
│   │   │   │       ├── inbound/
│   │   │   │       └── outbound/
│   │   │   └── adapters/
│   │   │       ├── inbound/
│   │   │       │   └── rest/
│   │   │       └── outbound/
│   │   │           └── persistence/
│   │   │               ├── order_repository.py
│   │   │               ├── order_item_mapper.py
│   │   │               └── shipment_mapper.py
│   │   ├── cart/
│   │   │   └── ... (same pattern)
│   │   ├── payments/
│   │   │   └── ... (idempotent + append-only)
│   │   ├── inventory/
│   │   │   └── ... (reservation-based)
│   │   ├── checkout/
│   │   │   └── ... (orchestration / saga handlers)
│   │   ├── shipping/
│   │   │   └── ...
│   │   ├── coupons/
│   │   │   └── ...
│   │   ├── accounts/
│   │   │   └── ...
│   │   ├── notifications/
│   │   │   └── ...
│   │   └── search/
│   │       └── ...
│   └── shared/
│       ├── events/
│       │   └── base_event.py
│       ├── outbox/
│       └── value_objects/
├── infra/
│   ├── django/
│   │   ├── settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── database/
│       ├── migrations/
│       └── scripts/
├── docs/
│   ├── adr/
│   ├── database-tables/
│   └── architecture-diagrams/
├── tests/
└── README.md

2️⃣ DATABASE PER DOMAIN (CONCRETE TABLES)

Each domain has its own DB + outbox events

products_db
orders_db
cart_db
payments_db
inventory_db
checkout_db
shipping_db
coupons_db
accounts_db
notifications_db
search_db


Key principles:

Aggregate = transactional boundary

Event-sourcing for cross-domain integration

Outbox tables for async delivery

Append-only where needed

Read models are denormalized and disposable

3️⃣ OUTBOX EVENTS PATTERN

Every aggregate has an outbox table:

outbox_events
-------------
id PK
aggregate_id UUID
event_type VARCHAR
payload JSONB
created_at TIMESTAMP
published_at TIMESTAMP NULL


Purpose:

Guarantees async messaging

Supports saga orchestration

Enables replay

4️⃣ SAGA / ORCHESTRATION PATTERNS

Checkout → Order → Payment → Inventory → Shipping

checkout_orchestrator/
├── saga_handlers/
│   ├── checkout_saga.py
│   └── refund_saga.py


Each saga listens to events via outbox

Coordinates multiple aggregates

Uses compensating transactions for failures

5️⃣ DOMAIN RULES & DATABASE LAWS

1️⃣ Orders: append-only, snapshot product & pricing
2️⃣ Payments: idempotent, ledger-first
3️⃣ Inventory: reservation-based, eventually consistent
4️⃣ Cart: disposable, orchestrates checkout
5️⃣ Checkout: orchestration, no domain truth
6️⃣ Shipping: reacts to events, append-only
7️⃣ Coupons: immutable history
8️⃣ Accounts: snapshot-based
9️⃣ Notifications: async
10️⃣ Search: denormalized read-only

6️⃣ PRINCIPAL-LEVEL ARCHITECTURAL GUIDELINES

No cross-domain FKs — use IDs + events

Aggregate = transactional boundary

Event-driven for all cross-domain communication

Read models denormalized & rebuildable

All mutable external data is snapshotted

Outbox tables for every aggregate

Sagas for long-running flows

Idempotency keys for payments, checkout, inventory

✅ This blueprint is ready for 100 developers, 50-year evolution, and production-grade reliability.
