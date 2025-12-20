### ORDERS DOMAIN — SYSTEM OF RECORD (FINAL BOSS)

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