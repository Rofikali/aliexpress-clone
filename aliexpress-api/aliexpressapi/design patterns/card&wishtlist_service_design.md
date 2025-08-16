# 🛒 Cart & Wishlist Service – LLD + HLD

---

## 🧩 LLD – Database Schema

### 1. Cart Table

| Column      | Type         | Constraints / Notes                                         |
| ----------- | ------------ | ------------------------------------------------------------ |
| id          | BIGINT / UUID | PK                                                          |
| user_id     | FK → accounts_user | Indexed, references the owner of the cart               |
| total_price | DECIMAL(12,2) | Stores current total (snapshot)                            |
| status      | ENUM         | ['active','ordered','abandoned']                             |
| created_at  | TIMESTAMP    | Indexed                                                      |
| updated_at  | TIMESTAMP    |                                                              |

### 2. Cart Items Table

| Column     | Type         | Constraints / Notes                                       |
| ---------- | ------------ | ---------------------------------------------------------- |
| id         | BIGINT / UUID | PK                                                        |
| cart_id    | FK → cart    | Indexed, ON DELETE CASCADE                                  |
| product_id | FK → products_product | Indexed, references included product              |
| quantity   | INT          | ≥ 1                                                         |
| price      | DECIMAL(12,2)| Cached snapshot price to prevent inconsistencies           |
| created_at | TIMESTAMP    |                                                            |
| updated_at | TIMESTAMP    |                                                            |

### 3. Wishlist Table

| Column      | Type         | Constraints / Notes                                       |
| ----------- | ------------ | ---------------------------------------------------------- |
| id          | BIGINT / UUID | PK                                                        |
| user_id     | FK → accounts_user | Indexed, references the owner                          |
| product_id  | FK → products_product | Indexed                                               |
| created_at  | TIMESTAMP    |                                                            |
| UNIQUE(user_id, product_id) | Ensures no duplicate wishlist entries |                |

**Notes:**

- Cart items store a **snapshot of price** to maintain consistency during checkout.  
- Wishlist is a simple **key-value mapping** for fast lookups.  
- Cart **status allows cleanup** of abandoned carts automatically.

---

## 🏗 HLD – Service Design

### Microservices

- **Cart Service** – handles add/remove/update items, calculates totals  
- **Wishlist Service** – handles favorites/wishlist operations  

### Cache Layer

- **Redis** for active carts and frequently accessed wishlists  
- TTL: 1–6 hours, write-through cache strategy  

### Event-Driven Updates

- Product price or stock changes → update cart totals/availability  
- Cart checkout → triggers **Order Service**  

### API Endpoints

| Method | Endpoint                 | Description                       |
| ------ | ------------------------ | --------------------------------- |
| POST   | /cart/add-item           | Add product to cart               |
| PATCH  | /cart/update-item        | Change quantity                   |
| DELETE | /cart/remove-item        | Remove product                    |
| GET    | /cart                     | Fetch cart contents               |
| POST   | /wishlist/add            | Add product to wishlist           |
| DELETE | /wishlist/remove         | Remove from wishlist              |
| GET    | /wishlist                 | Fetch wishlist items              |

### Scalability

- Partition **carts by user_id** across database shards  
- **Redis clusters** for high concurrency  
- Background jobs to clean **abandoned carts**  

### Security

- Only authenticated users can modify their cart/wishlist  

---

## 📊 ERD – Cart & Wishlist

```mermaid
erDiagram
    accounts_user ||--o{ cart : owns
    cart ||--o{ cart_item : contains
    products_product ||--o{ cart_item : included_in
    accounts_user ||--o{ wishlist : keeps
    products_product ||--o{ wishlist : listed_in
