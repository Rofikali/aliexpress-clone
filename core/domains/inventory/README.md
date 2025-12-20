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