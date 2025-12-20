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