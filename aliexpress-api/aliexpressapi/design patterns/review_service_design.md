# 📝 Review & Ratings Service – LLD + HLD

---

## 🧩 LLD – Database Schema

### 1. Review Table

| Column      | Type          | Constraints / Notes                        |
| ----------- | ------------- | ----------------------------------------- |
| id          | BIGINT / UUID | PK                                         |
| user_id     | FK → accounts_user | Indexed                               |
| product_id  | FK → products_product | Indexed                           |
| seller_id   | FK → accounts_user | Indexed, optional (for seller review) |
| rating      | INT           | 1–5, NOT NULL                              |
| comment     | TEXT          | Optional                                    |
| is_verified | BOOLEAN       | Verified purchase flag                      |
| status      | ENUM          | ['pending','approved','rejected','flagged'] |
| created_at  | TIMESTAMP     | Indexed                                    |
| updated_at  | TIMESTAMP     |                                           |

### 2. Review Metadata / Aggregates Table

| Column       | Type           | Constraints / Notes                        |
| ------------ | -------------- | ----------------------------------------- |
| id           | BIGINT / UUID  | PK                                         |
| product_id   | FK → products_product | Indexed                           |
| avg_rating   | FLOAT          | Updated via triggers / batch jobs          |
| review_count | INT            | Total approved reviews                      |
| last_updated | TIMESTAMP      |                                           |

### 3. Moderation / Spam Table

| Column      | Type           | Constraints / Notes                        |
| ----------- | -------------- | ----------------------------------------- |
| id          | BIGINT / UUID  | PK                                         |
| review_id   | FK → review    | Indexed                                    |
| flagged_by  | ENUM / VARCHAR | ['user','system']                           |
| reason      | TEXT           | Spam, offensive content, fake review       |
| status      | ENUM           | ['pending','actioned','ignored']           |
| created_at  | TIMESTAMP      |                                           |

---

## 🏗 HLD – Service Design

### Microservices

- **Review Service** – CRUD for product & seller reviews  
- **Moderation Service** – ML-based spam/fake review detection  
- **Aggregator Service** – updates `avg_rating` and `review_count` in Products DB  

### Cache Layer

- Redis for frequently viewed product ratings & top reviews  
- TTL: 1–6 hours depending on review volume  

### Event-Driven Updates

- New review → triggers Moderation Service  
- Approved review → update aggregates via Aggregator Service  
- Review flagged → notifications to moderation team  

### API Endpoints

| Method | Endpoint                        | Description                           |
| ------ | ------------------------------- | ------------------------------------- |
| POST   | /review/create                  | Submit a new review                    |
| PATCH  | /review/update/{id}             | Edit review (if allowed)               |
| GET    | /review/product/{product_id}    | Fetch reviews for a product            |
| GET    | /review/seller/{seller_id}      | Fetch reviews for a seller             |
| POST   | /review/flag/{review_id}        | Flag review for moderation             |
| GET    | /review/aggregates/{product_id} | Fetch aggregate rating & review count  |

### Scalability

- Partition reviews by `product_id` or `seller_id`  
- Background workers for moderation & aggregate updates  
- Read replicas for fetching reviews and aggregates  

### Security

- Only verified buyers can submit product reviews  
- Authenticated users for seller reviews & moderation actions  
- Audit logs for moderation & edits  

---

## 📊 ERD – Review & Ratings Service

```mermaid
erDiagram
    accounts_user ||--o{ review : writes
    products_product ||--o{ review : receives
    review ||--o{ review_moderation : flagged_by
    products_product ||--o{ review_aggregates : aggregates

Architecture – HLD 

graph TB
    APIGW[API Gateway]
    Web[Web SPA]
    App[Mobile Apps]

    ReviewService[Review Service]
    ModerationService[Moderation / ML Service]
    AggregatorService[Aggregate & Stats Service]
    Redis[Redis Cache]
    Postgres[Postgres DB]
    Kafka[Event Bus / Kafka]

    Web --> APIGW
    App --> APIGW

    APIGW --> ReviewService
    ReviewService --> ModerationService
    ReviewService --> AggregatorService

    ReviewService --> Redis
    AggregatorService --> Redis

    ReviewService --> Postgres
    AggregatorService --> Postgres

    ReviewService --> Kafka
