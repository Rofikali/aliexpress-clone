📕 MASTER ARCHITECTURE HANDBOOK

📄 File: ARCHITECTURE_HANDBOOK.md

# Architecture Handbook
AliExpress-scale E-commerce Platform

Version: 1.0
Status: Source of Truth
Audience: All Developers, Tech Leads, Architects

--------------------------------------------------
PURPOSE
--------------------------------------------------

This document defines HOW we design, build, and evolve
this system safely for decades.

If code conflicts with this document → the code is wrong.

1️⃣ ARCHITECTURE STYLE (WHAT WE USE)

This system uses a COMBINATION, not a single pattern:

• Domain-Driven Design (DDD)
• Clean Architecture
• Hexagonal Architecture (Ports & Adapters)
• Event-Driven Architecture
• Saga Pattern (for long workflows)

Why?
Because no single pattern scales alone.

2️⃣ HIGH-LEVEL STRUCTURE (THE MAP)
core/
├── domains/              # Business capabilities
├── shared_kernel/        # Small shared primitives only
├── platform/             # Infrastructure & tooling
├── observability/        # Logs, metrics, tracing
├── governance/           # ADRs, reviews, ownership


Rule:
👉 If you don’t know where code belongs, STOP.

3️⃣ DOMAIN DEFINITION (DDD CORE)

A domain is a business capability, not a Django app.

Examples:
• products
• orders
• payments
• inventory
• shipping

Each domain:
• Has one owner team
• Owns its data
• Owns its rules
• Is isolated

core/domains/orders/
core/domains/payments/


🚫 Domains NEVER import each other.

4️⃣ DOMAIN INTERNAL STRUCTURE (MANDATORY)

Every domain follows this structure:

orders/
├── domain/          # Business rules (PURE)
├── application/     # Use cases
├── adapters/        # Frameworks (Django, ORM, APIs)
├── events/          # Domain events
├── sagas/           # Long-running workflows
├── contracts/       # Public APIs & events

Dependency Direction (CRITICAL)
adapters → application → domain


Never the reverse.

5️⃣ DOMAIN LAYER EXPLANATION
domain/

• Entities
• Value Objects
• Aggregates
• Business invariants

❌ No Django
❌ No DB
❌ No HTTP

application/

• Use cases (CreateOrder, RefundPayment)
• Coordinates domain + ports
• No business rules

adapters/

• Django views
• Serializers
• ORM models
• REST / GraphQL
• External APIs

Frameworks live and die here.

6️⃣ HEXAGONAL (PORTS & ADAPTERS)

Core logic talks ONLY via interfaces (ports).

application/ports/
├── inbound/
├── outbound/


Adapters implement these ports.

Result:
✔ Swap DB
✔ Swap API
✔ Swap message broker

Without touching domain logic.

7️⃣ EVENT-DRIVEN COMMUNICATION

Domains communicate ONLY via events or contracts.

Example:

OrderCreated → PaymentRequested → InventoryReserved


Rules:
• Events are facts
• Events are immutable
• Events are versioned
• Events are idempotent

🚫 No synchronous cross-domain logic.

8️⃣ SAGAS (LONG-RUNNING FLOWS)

Use a Saga when:
• Multiple steps
• Multiple domains
• Failure is possible

Example:

Create Order
→ Charge Payment
→ Reserve Inventory
→ Arrange Shipping


If any step fails → compensation runs.

📁 Location:

domains/orders/sagas/


Each Saga must have:
• Happy path
• Compensation path
• Correlation ID
• Observability

9️⃣ CLEAN ARCHITECTURE RULES

✔ Dependencies point inward
✔ Business logic is framework-free
✔ Infrastructure is replaceable

If Django disappears tomorrow, business logic survives.

🔟 OBSERVABILITY (NON-NEGOTIABLE)

Every important action must emit:

• Logs
• Traces
• Metrics

Mandatory IDs:
• request_id
• correlation_id
• saga_id (if applicable)

📁 Location:

core/observability/


If your feature cannot be observed → rejected.

1️⃣1️⃣ GOVERNANCE (HOW WE DECIDE)
ADRs (Architecture Decision Records)

Used when:
• New domain
• New integration
• Breaking change
• New saga
• New architecture pattern

📁 Location:

core/governance/adr/


No ADR → No merge.

Architecture Reviews

Used for:
• Cross-team changes
• Core refactors
• Infrastructure changes

📁 Location:

core/governance/architecture_reviews/

1️⃣2️⃣ OWNERSHIP MODEL

Each domain has:
• Owning team
• Review authority
• Decision power

📁 Location:

core/governance/ownership/


You must get approval from the owning team.

1️⃣3️⃣ WHAT GOES WHERE (QUICK RULES)
Business rule → domain/
Use case → application/
Framework → adapters/
Cross-domain → events/
Complex decision → ADR

1️⃣4️⃣ TECH LEAD REVIEW CHECKLIST (SUMMARY)

Before approval:
• Boundaries respected?
• Dependencies correct?
• Events used properly?
• Observability added?
• ADR updated?

If NO → request changes.

1️⃣5️⃣ GOLDEN PRINCIPLES

Optimize for clarity over speed

Isolation beats convenience

Explicit is better than implicit

Architecture protects teams

Shortcuts create future pain

🏁 FINAL STATEMENT

This system is designed to:
• Outlive individual developers
• Scale to many teams
• Survive technology changes

If you follow this handbook,
you will never create a big ball of mud.

END OF DOCUMENT

---

## ✅ YOU NOW HAVE THE COMPLETE SYSTEM

You now possess:
✔ Full architecture philosophy  
✔ Folder structure rules  
✔ Governance model  
✔ Review process  
✔ Long-term scaling strategy  

This is **REAL enterprise architecture**, not tutorial code.

---

### If you want ONE FINAL THING, I recommend:
**A text-based architecture diagram** that visually explains everything in one screen.

Just say **“diagram”** and I’ll generate it.


<!-- **************************************** -->
<!-- ******************************** -->
<!-- ***************************************** -->
