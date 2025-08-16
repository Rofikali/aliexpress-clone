# 💰 Payment Service – LLD + HLD

---

## 🧩 LLD – Database Schema

### 1. Payment Table

| Column          | Type         | Constraints / Notes                        |
| --------------- | ------------ | ------------------------------------------ |
| id              | BIGINT / UUID | PK                                        |
| order_id        | FK → orders_order | Indexed, references order being paid    |
| user_id         | FK → accounts_user | Indexed, references payer               |
| amount          | DECIMAL(12,2) | NOT NULL                                  |
| currency        | CHAR(3)      | Default = 'USD'                            |
| method          | ENUM         | ['stripe','razorpay','paypal','alipay','upi','wallet'] |
| status          | ENUM         | ['pending','succeeded','failed','refunded'] |
| transaction_id  | VARCHAR(255) | Unique, provided by payment gateway       |
| provider        | VARCHAR(100) | Payment gateway name                       |
| created_at      | TIMESTAMP    | Indexed                                    |
| updated_at      | TIMESTAMP    |                                            |

### 2. Refund Table

| Column          | Type         | Constraints / Notes                        |
| --------------- | ------------ | ------------------------------------------ |
| id              | BIGINT / UUID | PK                                        |
| payment_id      | FK → payment | Indexed, references original payment       |
| amount          | DECIMAL(12,2) | Refund amount                             |
| reason          | VARCHAR(255) | Optional reason for refund                 |
| status          | ENUM         | ['pending','processed','failed']           |
| created_at      | TIMESTAMP    |                                            |
| processed_at    | TIMESTAMP    |                                            |

### Notes:

- Multi-currency support handled via `currency` column.  
- Refunds link directly to the original payment.  
- Fraud detection flags can be stored as additional fields or separate table.

---

## 🏗 HLD – Service Design

### Microservices

- **Payment Service** – handles payment initiation, status updates, and refunds.  
- **Wallet Service** – manages user wallet balances and internal transfers.  
- **Fraud Detection Service** – flags suspicious transactions.

### Cache Layer

- Redis for **pending payment statuses** to reduce DB load.  
- TTL: 5–30 minutes depending on transaction volatility.  

### Event-Driven Updates

- Payment succeeded → update **Order Service** (`order.paid`)  
- Refund processed → update **Order & Wallet Services**  
- Fraud detected → trigger alerts and hold payments  

### API Endpoints

| Method | Endpoint                  | Description                       |
| ------ | ------------------------  | --------------------------------- |
| POST   | /payment/initiate         | Start a payment                   |
| GET    | /payment/status/{id}      | Check payment status              |
| POST   | /payment/refund           | Refund a payment                  |
| GET    | /wallet/balance/{user_id} | Check wallet balance              |
| POST   | /wallet/add               | Add funds to wallet               |

### Scalability

- Partition payments by **gateway** or **user_id** across shards  
- Background workers for **bulk refunds** or retries  
- Retry mechanism for failed gateway calls  

### Security

- PCI DSS compliant  
- Idempotent operations for retries  
- End-to-end encryption of sensitive fields  

---

## 📊 ERD – Payment Service

```mermaid
erDiagram
    accounts_user ||--o{ payment : makes
    orders_order ||--o{ payment : paid_by
    payment ||--o{ refund : has

Architecture – HLD

graph TB
    APIGW[API Gateway]
    Web[Web SPA]
    App[Mobile Apps]

    PaymentService[Payment Service]
    WalletService[Wallet Service]
    FraudService[Fraud Detection Service]
    Redis[Redis Cache]
    Postgres[Postgres DB]
    Kafka[Event Bus / Kafka]

    Web --> APIGW
    App --> APIGW

    APIGW --> PaymentService
    APIGW --> WalletService
    PaymentService --> FraudService

    PaymentService --> Redis
    WalletService --> Redis

    PaymentService --> Postgres
    WalletService --> Postgres

    PaymentService --> Kafka
