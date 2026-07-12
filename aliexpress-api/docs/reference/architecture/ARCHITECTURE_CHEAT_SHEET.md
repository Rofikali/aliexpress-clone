📄 1️⃣ ONE-PAGE ARCHITECTURE CHEAT SHEET

For daily use (developers, reviewers, leads)

📁 File: ARCHITECTURE_CHEAT_SHEET.md

# Architecture Cheat Sheet (READ DAILY)

This project uses:
DDD + Clean Architecture + Hexagonal Architecture
with Saga + Event-Driven where needed.

----------------------------------
CORE RULES (NON-NEGOTIABLE)
----------------------------------

1. Domains are isolated
2. Dependencies point inward
3. No shared databases
4. No cross-domain imports
5. Observability is mandatory
6. Big changes require ADR + review

----------------------------------
FOLDER MEANINGS (MEMORIZE)
----------------------------------

domain/
→ Business rules ONLY
→ No Django, no DB, no APIs

application/
→ Use cases (what the system does)
→ Coordinates domain + ports

adapters/
→ Django, ORM, REST, Kafka, external APIs
→ Framework-specific code only

events/
→ Facts that already happened
→ Immutable, versioned

sagas/
→ Long-running workflows
→ Must include compensations

contracts/
→ Public APIs & events
→ Team boundaries live here

----------------------------------
WHERE DOES MY CODE GO?
----------------------------------

Business rule?
→ domain/

Use case (CreateOrder, RefundPayment)?
→ application/use_cases/

Django view, serializer, ORM?
→ adapters/inbound or adapters/outbound

Talking to another domain?
→ Emit or consume events

----------------------------------
HOW DOMAINS COMMUNICATE
----------------------------------

✔ Events (preferred)
✔ Public APIs (contracts)
✘ Direct imports
✘ Shared models
✘ Shared tables

----------------------------------
SAGA RULES
----------------------------------

• Used when multiple steps can fail
• Must have compensation steps
• Must be observable
• Must have correlation_id + saga_id

----------------------------------
OBSERVABILITY RULES
----------------------------------

Every important action must have:
• Logs
• Traces
• Metrics

If it can’t be observed, it’s broken.

----------------------------------
WHEN YOU MUST STOP & ASK
----------------------------------

• New domain
• New saga
• Breaking event/API
• Cross-team dependency
• New infrastructure

----------------------------------
GOLDEN SENTENCE
----------------------------------

"If it breaks boundaries, it’s rejected."

📄 2️⃣ TECH LEAD / ARCHITECT CHECKLIST

For PR reviews, design reviews, and long-term health

📁 File: TECH_LEAD_CHECKLIST.md

# Tech Lead Architecture Checklist

Use this checklist before approving:
- Large PRs
- Cross-team changes
- Architectural refactors

----------------------------------
DOMAIN & DDD
----------------------------------

[ ] Is the business concept placed in the correct domain?
[ ] Are aggregates clearly defined?
[ ] Are invariants enforced inside the domain?
[ ] No anemic domain models?

----------------------------------
CLEAN ARCHITECTURE
----------------------------------

[ ] Dependencies point inward?
[ ] Domain has no framework imports?
[ ] Application layer contains no infrastructure logic?

----------------------------------
HEXAGONAL ARCHITECTURE
----------------------------------

[ ] All external systems accessed via ports?
[ ] Adapters isolated from core logic?
[ ] Easy to swap DB or messaging without rewriting logic?

----------------------------------
DOMAIN ISOLATION
----------------------------------

[ ] No cross-domain imports?
[ ] No shared database tables?
[ ] Communication via events or contracts only?

----------------------------------
SAGA & EVENT-DRIVEN
----------------------------------

[ ] Saga used only when needed?
[ ] All failure paths compensated?
[ ] Events immutable and versioned?
[ ] Idempotency considered?

----------------------------------
OBSERVABILITY
----------------------------------

[ ] correlation_id propagated?
[ ] saga_id present for workflows?
[ ] Logs are structured?
[ ] Metrics defined for failures & latency?

----------------------------------
GOVERNANCE
----------------------------------

[ ] ADR created or updated?
[ ] Architecture review done (if required)?
[ ] Owning team approved changes?

----------------------------------
LONG-TERM HEALTH
----------------------------------

[ ] Does this reduce coupling?
[ ] Can this scale to more teams?
[ ] Will this still make sense in 5–10 years?

----------------------------------
FINAL QUESTION (MOST IMPORTANT)
----------------------------------

"If another team owned this tomorrow,
would they understand it without asking?"

If NO → reject or request changes.

🏁 FINAL NOTE (IMPORTANT)

With these two documents:

✅ Juniors know where to put code
✅ Seniors know what to protect
✅ Reviews stay objective
✅ Architecture survives people changes

This is how serious systems stay healthy.