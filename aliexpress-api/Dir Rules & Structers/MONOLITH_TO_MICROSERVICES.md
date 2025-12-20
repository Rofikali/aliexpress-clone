                ┌───────────────────────────────┐
                │       CLIENTS (Web/Mobile)    │
                └─────────────┬─────────────────┘
                              │ HTTP / GraphQL
                              ▼
          ┌─────────────────────────────────────────────┐
          │             MODULAR MONOLITH                │
          │ (Single deployable Django app)             │
          │                                             │
          │ core/domains/                               │
          │ ├─ orders/                                 │
          │ ├─ payments/                               │
          │ ├─ products/                               │
          │ ├─ inventory/                              │
          │ ├─ carts/                                  │
          │ └─ checkout/                               │
          │                                             │
          │ application/use_cases/                      │
          │ adapters/                                  │
          │ events/                                    │
          │ sagas/                                     │
          │ contracts/                                 │
          └─────────────┬─────────────────────────────┘
                        │ gradual extraction
                        ▼
  ┌────────────────────────────────────────────────────────────┐
  │ PHASE 1: FIRST MICROSERVICE                                 │
  │ orders-service                                              │
  │ ┌─────────────────────────────┐                             
  │ │ domain/                     │                             
  │ │ application/                │                             
  │ │ adapters/                   │                             
  │ │ events/                     │                             
  │ │ sagas/                      │                             
  │ │ contracts/                  │                             
  │ └─────────────────────────────┘                             
  │ communicates via contracts/events with monolith             │
  └────────────────────────────────────────────────────────────┘
                        │ extract next
                        ▼
  ┌────────────────────────────────────────────────────────────┐
  │ PHASE 2: PAYMENTS SERVICE                                    │
  │ payments-service                                             │
  │ same folder structure as orders-service                     │
  │ communicates via events/contracts                             │
  └────────────────────────────────────────────────────────────┘
                        │ extract next
                        ▼
  ┌────────────────────────────────────────────────────────────┐
  │ PHASE 3: PRODUCTS & INVENTORY SERVICES                      │
  │ products-service / inventory-service                        │
  │ same folder structure, events, adapters, contracts         │
  └────────────────────────────────────────────────────────────┘
                        │ extract next
                        ▼
  ┌────────────────────────────────────────────────────────────┐
  │ PHASE 4: CARTS, CHECKOUT, COUPONS, REFUNDS                 │
  │ each as independent microservice                             │
  └────────────────────────────────────────────────────────────┘
                        │ extract final
                        ▼
  ┌────────────────────────────────────────────────────────────┐
  │ PHASE 5: PLATFORM CORE / SHARED SERVICES                   │
  │ - messaging / event bus (Kafka/RabbitMQ)                   │
  │ - auth / identity                                           │
  │ - logging / tracing / metrics                               │
  │ - shared libraries                                          │
  └────────────────────────────────────────────────────────────┘

══════════════════════════════════════════════════════════════
LEGEND
══════════════════════════════════════════════════════════════
• Each domain folder in monolith = candidate microservice
• Events/contracts = communication layer
• Sagas = orchestrate distributed workflows
• Strangler pattern = gradually replace monolith piece by piece
• Each extracted service = independent repo & deployable unit
