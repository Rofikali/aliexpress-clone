🧩 TEAM-WISE REPO SPLIT STRATEGY

(Monorepo → Multi-Repo at Scale)

🧠 CORE PRINCIPLE

Teams own domains.
Domains own repos.
Repos own releases.

No shared ownership = no chaos.

🏗️ PHASE 0 — STARTING POINT (MONOREPO)
aliexpress-platform/
├── core/
│   ├── domains/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── products/
│   │   ├── inventory/
│   │   ├── checkout/
│   │   ├── shipping/
│   │   ├── coupons/
│   │   ├── search/
│   │   └── notifications/
│
├── apps/
├── manage.py
└── docs/


✔ Single CI
✔ Single deployment
✔ Fast iteration

❌ Team contention
❌ Scaling pain

🚀 PHASE 1 — DOMAIN OWNERSHIP (NO REPO SPLIT YET)
Assign Teams
Team	Owns
Orders Team	Orders + Checkout
Payments Team	Payments
Catalog Team	Products
Supply Team	Inventory + Shipping
Growth Team	Coupons
Platform Team	Search + Notifications
RULE

❌ No team touches another domain’s core folder
✔ Changes via events/contracts only

✂️ PHASE 2 — LOGICAL SPLIT (IN SAME REPO)
core/domains/orders/        # Owned by Orders Team
core/domains/payments/      # Owned by Payments Team

Introduce:

Domain-level CI checks

Independent test suites

ADR ownership per domain

✔ Cultural separation
✔ Still one repo

🔥 PHASE 3 — PHYSICAL REPO SPLIT (REAL TRANSITION)
1️⃣ Create Domain Repos
orders-service/
payments-service/
products-service/
inventory-service/
checkout-orchestrator/
shipping-service/
coupons-service/
search-readmodels/
notifications-service/


Each repo contains:

├── domain/
├── application/
├── adapters/
├── events/
├── contracts/
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md

🔗 PLATFORM REPO (THE GLUE)
platform-infra/
├── api-gateway/
├── event-bus/
├── auth/
├── shared-observability/
├── terraform/
└── deployment/


Owned by Platform Team only.

🧬 SHARED CODE STRATEGY (CRITICAL)
❌ WHAT NOT TO SHARE

Models

Business logic

ORM entities

✅ WHAT CAN BE SHARED
shared-contracts/
├── events/
├── protobuf/
├── openapi/
└── schemas/


Versioned. Read-only.

🔐 RELEASE INDEPENDENCE

Each domain repo:

Owns its deployment

Owns its rollback

Owns its SLA

Example:

orders-service v3.2.1
payments-service v1.9.4

🔁 COMMUNICATION RULES
Type	Allowed
REST sync	Gateway → Domain
Events	Domain → Domain
DB access	❌ NEVER
Shared cache	❌ NEVER
🧠 MIGRATION PLAYBOOK (SAFE)
Step 1

Extract domain folder into new repo
Keep DB shared initially

Step 2

Introduce event publishing

Step 3

Cut DB joins

Step 4

Deploy independently

🚨 FAILURE ISOLATION MATRIX
Failure	Impact
Payments down	Orders wait
Inventory down	Checkout blocked
Notifications down	No user impact
Search down	Degraded UX
🧪 CI/CD MODEL
PR → Domain Tests → Contract Tests → Deploy


Contract tests prevent breaking other teams.

🧠 ORG STRUCTURE (REALISTIC)
Principal Architect
│
├── Domain Architects (per 3–4 domains)
│
├── Staff Engineers (per team)
│
└── Platform Architects

🔥 PRINCIPAL-LEVEL RULES (NON-NEGOTIABLE)

1️⃣ No cross-domain DB joins
2️⃣ No shared business logic
3️⃣ Events are contracts
4️⃣ Teams deploy independently
5️⃣ Refactors never stop the business

🏁 FINAL TRUTH

Microservices are not technical.
They are organizational.