## 4. Order Service

### LLD – Database Schema

| Table       | Columns / Description                                                                 |
| ----------- | ------------------------------------------------------------------------------------ |
| orders_order | id PK, user_id FK, total_amount, status ENUM['pending','confirmed','shipped','delivered','returned'], created_at, updated_at |
| orders_order_item | id PK, order_id FK, product_id FK, seller_id FK, quantity, price, SKU, created_at, updated_at |
| orders_shipment | id PK, order_id FK, warehouse_id FK, carrier, tracking_number, status ENUM['pending','in_transit','delivered','returned'], estimated_delivery, created_at, updated_at |
| orders_return   | id PK, order_item_id FK, reason, status ENUM['requested','processed','rejected'], processed_at, created_at, updated_at |

### HLD – Service Design

- **Order Lifecycle:**  
  Cart → Checkout → Payment → Shipping → Delivery → Returns  

- **Multi-Seller Support:**  
  - Orders with products from multiple sellers are split internally per seller  
  - Each seller has independent shipment and inventory handling  

- **Integration:**  
  - Payment Service: verifies payment status  
  - Shipping Service: generates tracking & shipment updates  
  - Inventory Service: reserves stock on order creation  

- **Event-driven architecture:**  
  - `order.created` → triggers stock reservation & payment initiation  
  - `order.paid` → triggers shipping label creation  
  - `shipment.updated` → updates order status in real-time  
  - `order.returned` → triggers refund workflow  

- **Scaling & Performance:**  
  - Partition orders table by user_id or region  
  - Read replicas for order history queries  
  - Background workers handle bulk order processing, shipping updates, and return handling  

- **Caching:**  
  - Redis for frequently accessed order summaries (recent orders, tracking info)  
  - TTL: 10–30 minutes depending on update frequency  

### Optional: ERD

```mermaid
erDiagram
    accounts_user ||--o{ orders_order : places
    orders_order ||--o{ orders_order_item : contains
    orders_order_item }o--|| products_product : for
    orders_order ||--o{ orders_shipment : fulfills
    orders_order_item ||--o{ orders_return : may_have
    warehouse ||--o{ orders_shipment : fulfills
