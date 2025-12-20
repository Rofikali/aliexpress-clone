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