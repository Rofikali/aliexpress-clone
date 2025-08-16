## 3. Search & Recommendation Service

### LLD – Database Schema

| Table                 | Columns / Description                                                |
| --------------------- | ------------------------------------------------------------------- |
| search_index          | product_id FK, title, description, category_id FK, brand_id FK, price, stock, created_at, updated_at |
| recommendation_rules  | id, rule_type ENUM['also_bought','trending','personalized'], parameters JSON, created_at, updated_at |
| recommendation_log    | user_id FK, product_id FK, recommended_product_id FK, rule_id FK, timestamp |

### HLD – Service Design

- **Search Engine:** Elasticsearch / OpenSearch
- **Capabilities:**
  - Full-text search on product title & description
  - Faceted filtering by category, brand, price, attributes
  - Sorting by popularity, rating, price, relevance
- **Recommendations:**
  - Personalized ML-based ranking
  - “You may also like” (user-product collaborative filtering)
  - “Frequently bought together” (association rules / basket analysis)
- **Caching Layer:** Redis / Memcached for hot queries & recommendation results
- **Event-driven architecture:**
  - Kafka / RabbitMQ messages when products are added/updated → triggers search index updates
  - User interactions (clicks, purchases) → recommendation service logs for ML model retraining
- **Scaling:**
  - Search nodes horizontally scalable
  - Separate clusters for search and recommendation
  - Read replicas for high-volume queries
- **API Endpoints:**
  - `/search` → full-text + faceted filters
  - `/recommendations/user/{id}` → personalized suggestions
  - `/recommendations/product/{id}` → “also bought together”

### Optional: Caching & Precomputation

- Cache top N trending products per category
- Precompute recommendation lists nightly or incrementally for low-latency responses
