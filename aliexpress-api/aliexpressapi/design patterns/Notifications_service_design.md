# 🔔 Notifications Service – LLD + HLD

---

## 🧩 LLD – Database Schema

### 1. Notification Table

| Column       | Type           | Constraints / Notes                             |
| ------------ | -------------- | ----------------------------------------------- |
| id           | BIGINT / UUID  | PK                                              |
| user_id      | FK → accounts_user | Indexed                                     |
| type         | ENUM           | ['email','sms','push','in_app']               |
| title        | VARCHAR(255)   | Short description / message title              |
| body         | TEXT           | Message content                                |
| template_id  | FK → templates | Optional, template used for message            |
| status       | ENUM           | ['pending','sent','failed','read']             |
| scheduled_at | TIMESTAMP      | Optional, for delayed / scheduled notifications|
| sent_at      | TIMESTAMP      | When the notification was actually sent        |
| created_at   | TIMESTAMP      | Indexed                                        |
| updated_at   | TIMESTAMP      |                                               |

### 2. Notification Templates Table

| Column      | Type          | Constraints / Notes                        |
| ----------- | ------------- | ----------------------------------------- |
| id          | BIGINT / UUID | PK                                         |
| name        | VARCHAR(100)  | Template name, unique                       |
| type        | ENUM          | ['email','sms','push','in_app']           |
| subject     | VARCHAR(255)  | For email / push notifications             |
| body        | TEXT          | Template content, supports placeholders    |
| created_at  | TIMESTAMP     |                                           |
| updated_at  | TIMESTAMP     |                                           |

### Notes:

- `Notification.status` allows retry logic for failed sends.
- Templates support personalization with placeholders like `{{user_name}}` or `{{order_id}}`.

---

## 🏗 HLD – Service Design

### Microservices

- **Notification Service** – orchestrates sending messages across multiple channels.
- **Template Service** – manages notification templates.
- **Queue / Event Bus** – Kafka / RabbitMQ for async delivery and retries.

### Event-Driven Architecture

- Example: `order.placed` → triggers notification to buyer and seller.
- Async processing ensures minimal impact on core services.
- Retry logic for failed deliveries, backed by DLQ (Dead Letter Queue).

### Cache Layer

- Redis for throttling & rate-limiting per user/channel.
- Cache common templates for fast retrieval.

### API Endpoints

| Method | Endpoint                       | Description                           |
| ------ | ------------------------------ | ------------------------------------- |
| POST   | /notification/send             | Send notification immediately         |
| POST   | /notification/schedule         | Schedule notification for later       |
| GET    | /notification/user/{user_id}   | Fetch user notifications              |
| POST   | /template/create               | Create a new template                 |
| PATCH  | /template/update/{template_id} | Update template                        |
| GET    | /template/list                 | List all templates                     |

### Scalability

- Partition notifications by `user_id` for horizontal scaling.
- Kafka partitions for concurrent delivery.
- Use multiple worker instances to handle high throughput.

### Security

- Only authenticated services can publish/send notifications.
- Validate template placeholders to prevent injection attacks.

---

## 📊 ERD – Notifications Module

```mermaid
erDiagram
    accounts_user ||--o{ notification : receives
    notification ||--|| templates : uses

Architecture – HLD

graph TB
    APIGW[API Gateway]
    Web[Web SPA]
    App[Mobile Apps]

    NotificationService[Notification Service]
    TemplateService[Template Service]
    Kafka[Event Bus / Kafka]
    Redis[Redis Cache]
    Postgres[Postgres DB]

    Web --> APIGW
    App --> APIGW

    APIGW --> NotificationService
    NotificationService --> TemplateService
    NotificationService --> Redis
    NotificationService --> Postgres
    NotificationService --> Kafka
