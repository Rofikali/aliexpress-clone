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