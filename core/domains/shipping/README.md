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