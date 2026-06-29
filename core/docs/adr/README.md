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