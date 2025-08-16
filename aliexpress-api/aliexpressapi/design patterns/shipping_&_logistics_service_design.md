# 🚚 Shipping & Logistics Service – LLD + HLD

---

## 🧩 LLD – Database Schema

### 1. Warehouse Table

| Column      | Type         | Constraints / Notes                  |
| ----------- | ------------ | ----------------------------------- |
| id          | BIGINT / UUID | PK                                  |
| name        | VARCHAR(255) | NOT NULL                             |
| location    | VARCHAR(500) | Geo-coordinates / address            |
| capacity    | INT          | Optional, max inventory capacity     |
| created_at  | TIMESTAMP    | Indexed                              |
| updated_at  | TIMESTAMP    |                                     |

### 2. Inventory Table

| Column       | Type           | Constraints / Notes                  |
| ------------ | -------------- | ----------------------------------- |
| id           | BIGINT / UUID  | PK                                  |
| product_id   | FK → products_product | Indexed                         |
| warehouse_id | FK → warehouse | Indexed                             |
| stock        | INT            | Current available stock             |
| reserved     | INT            | Stock reserved for pending orders   |
| created_at   | TIMESTAMP      |                                     |
| updated_at   | TIMESTAMP      |                                     |

### 3. Shipment Table

| Column            | Type           | Constraints / Notes                    |
| ----------------- | -------------- | ------------------------------------- |
| id                | BIGINT / UUID  | PK                                    |
| order_id          | FK → orders_order | Indexed                            |
| carrier           | ENUM / VARCHAR | ['DHL','FedEx','UPS','Local']         |
| tracking_number   | VARCHAR(255)   | Unique                                |
| status            | ENUM           | ['pending','in_transit','delivered','failed','returned'] |
| estimated_delivery| TIMESTAMP      | Optional                               |
| shipped_at        | TIMESTAMP      | When shipped                           |
| delivered_at      | TIMESTAMP      | When delivered                         |
| created_at        | TIMESTAMP      | Indexed                                |
| updated_at        | TIMESTAMP      |                                       |

### 4. Shipping Address Table

| Column         | Type         | Constraints / Notes                  |
| -------------- | ------------ | ----------------------------------- |
| id             | BIGINT / UUID | PK                                  |
| user_id        | FK → accounts_user | Indexed                          |
| order_id       | FK → orders_order | Indexed (optional, if assigned) |
| address_line1  | VARCHAR(255) | NOT NULL                             |
| address_line2  | VARCHAR(255) | Optional                             |
| city           | VARCHAR(100) | NOT NULL                             |
| state          | VARCHAR(100) | NOT NULL                             |
| country        | VARCHAR(100) | NOT NULL                             |
| postal_code    | VARCHAR(20)  | NOT NULL                             |
| latitude       | DECIMAL(9,6) | Optional for geolocation             |
| longitude      | DECIMAL(9,6) | Optional for geolocation             |
| created_at     | TIMESTAMP    | Indexed                              |
| updated_at     | TIMESTAMP    |                                     |

---

## 🏗 HLD – Service Design

### Microservices

- **Shipping Service** – manages shipments, tracking, and delivery events  
- **Logistics Integration Service** – connects with DHL, FedEx, UPS, and local couriers  
- **Warehouse & Inventory Service** – keeps stock updated per warehouse

### Cache Layer

- Redis for frequently queried **shipment statuses** and **tracking info**  
- TTL: 5–30 minutes depending on volatility  

### Event-Driven Updates

- Order confirmed → reserve stock → create shipment  
- Shipment status updated → push notifications to user  
- Stock changes → notify Cart & Order Services  

### API Endpoints

| Method | Endpoint                        | Description                          |
| ------ | -------------------------------- | ------------------------------------ |
| POST   | /shipment/create                | Create a shipment                    |
| GET    | /shipment/status/{tracking_no}  | Check shipment status                |
| POST   | /shipment/update-status         | Update shipment status               |
| GET    | /warehouse/inventory/{product_id} | Check stock per warehouse          |
| GET    | /shipping/cost-estimate         | Calculate shipping cost by address   |

### Scalability

- Partition warehouses by region  
- Background jobs for bulk shipment creation and tracking updates  
- CDN or edge cache for tracking pages  
- Multi-region setup for global shipping support

### Security

- Authenticated APIs for shipment creation and updates  
- Logging and audit of all shipment events  

---

## 📊 ERD – Shipping Service

```mermaid
erDiagram
    accounts_user ||--o{ shipping_address : has
    orders_order ||--o{ shipment : fulfilled_by
    warehouse ||--o{ inventory : stores
    products_product ||--o{ inventory : stocked_as
    shipment ||--o{ shipping_address : ships_to


Architecture – HLD

graph TB
    APIGW[API Gateway]
    Web[Web SPA]
    App[Mobile Apps]

    ShippingService[Shipping Service]
    LogisticsService[3rd-Party Logistics Integration]
    WarehouseService[Warehouse & Inventory Service]
    Redis[Redis Cache]
    Postgres[Postgres DB]
    Kafka[Event Bus / Kafka]

    Web --> APIGW
    App --> APIGW

    APIGW --> ShippingService
    APIGW --> WarehouseService
    ShippingService --> LogisticsService

    ShippingService --> Redis
    WarehouseService --> Redis

    ShippingService --> Postgres
    WarehouseService --> Postgres

    ShippingService --> Kafka
