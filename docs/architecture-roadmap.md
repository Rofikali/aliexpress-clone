# Modular Monolith Roadmap

## Goal

Deliver a reliable marketplace with a modular Django REST Framework backend and Nuxt frontend. Keep deployment simple while making module extraction possible later.

## Why Not Microservices Now?

Microservices add distributed transactions, network failures, tracing, deployment orchestration, versioning, and operational cost. A modular monolith gives the important benefit now: clear ownership and enforced boundaries. Extract a service only when a module needs independent scaling, deployment, team ownership, security isolation, or a different reliability profile.

## Bounded Contexts

| Module | Owns | May depend on |
| --- | --- | --- |
| accounts | identity, profiles, roles, addresses | shared kernel |
| catalog | products, categories, variants, media | inventory (availability contract) |
| inventory | stock, reservations, warehouses | shared kernel |
| cart | carts and cart items | catalog query contract |
| checkout | pricing snapshot and checkout orchestration | cart, inventory, orders, payments |
| orders | order lifecycle and immutable purchase snapshots | payments, shipping contracts |
| payments | payment intents, provider attempts, refunds | orders contract |
| shipping | fulfilment, shipment tracking | orders contract |
| promotions | coupons and pricing rules | catalog, checkout contracts |
| notifications | delivery preferences and notification delivery | domain events |
| search | query projections and indexing | catalog events |

## Rules for Module Boundaries

1. A module owns its tables and Django models. Other modules do not query or mutate them directly.
2. Cross-module reads use a query port, explicit application service, or read projection.
3. Cross-module writes use a command/application port. Long-running workflows use events and a saga/process manager.
4. Database transactions remain inside one module. Use compensating actions for cross-module failure.
5. Every public HTTP and event contract is versioned and backward compatible while consumers migrate.

## Delivery Stages

### Stage 1: Establish the foundation

- Keep current Django apps operational.
- Create module packages and move new business rules into application use cases.
- Add architecture tests/import checks and a common error envelope.
- Document API contracts through OpenAPI and generate or validate frontend types.

### Stage 2: Harden transactional workflows

- Introduce an outbox table and background publisher.
- Make payment and checkout commands idempotent with idempotency keys.
- Add inventory reservation, order snapshots, audit records, and retry policies.
- Add correlation IDs, structured logs, metrics, and health/readiness endpoints.

### Stage 3: Extract only with evidence

Before extraction, define the service API/event contract, migrate data ownership, run a strangler route, add dashboards and runbooks, then cut over. Do not split a module merely because it has a folder.

## Definition of Done for Cross-Module Work

- Ownership and dependencies documented.
- Command/query/event contract versioned and tested.
- Authorization, validation, idempotency, and failure behavior defined.
- Logs, metrics, and alerts added for the new critical path.
- Rollback and data-migration plan reviewed.
