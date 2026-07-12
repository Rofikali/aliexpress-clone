# Django to DDD Architecture Migration Checklist

Goal:
Gradually migrate an existing Django project to a
DDD + Clean + Hexagonal + Event-Driven architecture
without stopping feature delivery.

---

## PHASE 0 — PREPARATION (MANDATORY)

☐ Freeze major refactors (feature work continues)
☐ Identify core business domains (Products, Orders, Payments, etc.)
☐ Assign temporary domain ownership (even if teams are small)
☐ Add ARCHITECTURE.md to repo root
☐ Add governance/ folder (empty is fine initially)

Outcome:
Everyone understands WHERE the system is going.

---

## PHASE 1 — FOLDER REALIGNMENT (SAFE)

☐ Create `core/` folder
☐ Move Django apps logically into `core/domains/`
☐ Do NOT change logic yet
☐ One domain per folder

Example:
- products_app → core/domains/products
- orders_app → core/domains/orders

☐ Keep Django settings unchanged

Outcome:
Structure changes, behavior stays identical.

---

## PHASE 2 — DOMAIN LAYER EXTRACTION

For each domain:

☐ Identify business rules in models/services
☐ Create `domain/` folder
☐ Move pure business logic into domain layer
☐ Leave Django ORM models in adapters layer

Rules:
- Domain must not import Django
- No database access in domain

Outcome:
Business logic becomes framework-independent.

---

## PHASE 3 — APPLICATION USE CASES

For each domain:

☐ Create `application/use_cases/`
☐ Wrap existing service logic into use cases
☐ Controllers/views now call use cases
☐ No ORM access in use cases directly

Outcome:
Explicit business workflows emerge.

---

## PHASE 4 — HEXAGONAL ADAPTERS

☐ Create adapters/inbound/rest/
☐ Move Django views/serializers here
☐ Create adapters/outbound/persistence/
☐ ORM access only allowed here

Rules:
- Adapters depend on application/domain
- Never the reverse

Outcome:
Framework isolation achieved.

---

## PHASE 5 — INTRODUCE EVENTS (NON-BREAKING)

☐ Identify state changes (OrderCreated, PaymentCompleted)
☐ Emit domain events (in-process initially)
☐ Add event handlers inside same codebase
☐ No message broker yet

Outcome:
Event-driven mindset without infra complexity.

---

## PHASE 6 — SAGA INTRODUCTION (ORDERS FIRST)

☐ Identify multi-step workflows (checkout)
☐ Create `application/sagas/`
☐ Move orchestration logic out of views
☐ Define compensation paths

Rules:
- No try/except spaghetti
- All failures explicit

Outcome:
Failures become predictable and manageable.

---

## PHASE 7 — OBSERVABILITY (CRITICAL)

☐ Add correlation_id middleware
☐ Add saga_id tracking
☐ Add structured logging
☐ Track saga steps & compensations

Outcome:
You can debug production incidents safely.

---

## PHASE 8 — GOVERNANCE ACTIVATION

☐ Add ADR template
☐ Write first 3 ADRs
☐ Add architecture review checklist
☐ Define code ownership
☐ Add CI guardrail rules (initially soft)

Outcome:
Architecture becomes enforceable.

---

## PHASE 9 — TEAM BOUNDARIES

☐ Assign each domain to one team
☐ Lock cross-domain imports
☐ Require contract-based communication
☐ Introduce event versioning

Outcome:
Teams can scale independently.

---

## PHASE 10 — OPTIONAL SCALE STEPS

☐ Introduce message broker (Kafka/RabbitMQ)
☐ Split read/write models (CQRS)
☐ Extract domains into services if needed
☐ Add distributed tracing

Outcome:
System becomes AliExpress-scale ready.

---

## RULES DURING MIGRATION (NON-NEGOTIABLE)

- Never rewrite everything
- Migrate domain by domain
- Ship continuously
- Architecture > speed > perfection
- Documentation is part of the work

---

## DEFINITION OF DONE

✔ Domain logic framework-free
✔ Use cases explicit
✔ Adapters isolated
✔ Events observable
✔ Governance active
✔ Teams autonomous


### refector
Structure first.
Logic second.
Infrastructure last.
