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