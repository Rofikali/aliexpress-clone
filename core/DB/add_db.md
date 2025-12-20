This is the most STAFF / PRINCIPAL-LEVEL decision you could make.

Below is OPTION 1: DOMAIN-WISE DATABASE SPLIT, written so you can copy-paste into dbdiagram.io as separate diagrams (one per database).

No code.
Only schemas + why they exist.
This is AliExpress-grade and safe for 100+ devs, 50 years.

🧠 WHY SPLIT DATABASES BY DOMAIN (NON-NEGOTIABLE)

Each domain:

Owns its data

Owns its schema

Communicates only via events

Can scale, migrate, or be rewritten independently

❌ No shared tables
❌ No cross-DB foreign keys
✅ Eventual consistency
✅ Legal & financial isolation


### Project products_db {
  database_type: "PostgreSQL"
}

Table products {
  id uuid [pk]
  seller_id uuid
  title varchar
  description text
  category_id uuid
  status varchar
  created_at timestamp
  updated_at timestamp
}

Table product_variants {
  id uuid [pk]
  product_id uuid
  sku varchar [unique]
  attributes json
}

Table product_prices {
  id uuid [pk]
  variant_id uuid
  currency varchar
  amount decimal
  valid_from timestamp
  valid_to timestamp
}

Table product_images {
  id uuid [pk]
  product_id uuid
  url varchar
  sort_order int
}
 
### Project cart_db {
  database_type: "PostgreSQL"
}

Table carts {
  id uuid [pk]
  user_id uuid
  status varchar
  expires_at timestamp
  created_at timestamp
}

Table cart_items {
  id uuid [pk]
  cart_id uuid
  product_id uuid
  variant_id uuid
  quantity int
  price_snapshot json
}

### Project orders_db {
  database_type: "PostgreSQL"
}

Table orders {
  id uuid [pk]
  user_id uuid
  order_number varchar [unique]
  status varchar
  total_amount decimal
  currency varchar
  created_at timestamp
}

Table order_items {
  id uuid [pk]
  order_id uuid
  product_id uuid
  variant_id uuid
  quantity int
  unit_price decimal
  total_price decimal
}

Table order_addresses {
  id uuid [pk]
  order_id uuid
  type varchar
  address json
}

Table order_state_transitions {
  id uuid [pk]
  order_id uuid
  from_state varchar
  to_state varchar
  changed_at timestamp
}

### Project payments_db {
  database_type: "PostgreSQL"
}

Table payments {
  id uuid [pk]
  order_id uuid
  status varchar
  amount decimal
  currency varchar
  provider varchar
  created_at timestamp
}

Table payment_transactions {
  id uuid [pk]
  payment_id uuid
  provider_txn_id varchar
  type varchar
  amount decimal
  status varchar
  created_at timestamp
}

Table payment_idempotency_keys {
  id uuid [pk]
  key varchar [unique]
  request_hash varchar
  created_at timestamp
}

### Project inventory_db {
  database_type: "PostgreSQL"
}

Table inventory_items {
  id uuid [pk]
  product_id uuid
  variant_id uuid
  total_stock int
}

Table inventory_reservations {
  id uuid [pk]
  order_id uuid
  variant_id uuid
  quantity int
  status varchar
  expires_at timestamp
}

### Project checkout_db {
  database_type: "PostgreSQL"
}

Table checkout_sessions {
  id uuid [pk]
  cart_id uuid
  user_id uuid
  status varchar
  created_at timestamp
}

Table checkout_steps {
  id uuid [pk]
  session_id uuid
  step_name varchar
  status varchar
  updated_at timestamp
}

### Project shipping_db {
  database_type: "PostgreSQL"
}

Table shipments {
  id uuid [pk]
  order_id uuid
  carrier varchar
  tracking_number varchar
  status varchar
  shipped_at timestamp
}

Table shipment_events {
  id uuid [pk]
  shipment_id uuid
  status varchar
  occurred_at timestamp
}

### Project coupons_db {
  database_type: "PostgreSQL"
}

Table coupons {
  id uuid [pk]
  code varchar [unique]
  discount_type varchar
  discount_value decimal
  valid_from timestamp
  valid_to timestamp
}

Table coupon_redemptions {
  id uuid [pk]
  coupon_id uuid
  user_id uuid
  order_id uuid
  redeemed_at timestamp
}

### Project accounts_db {
  database_type: "PostgreSQL"
}

Table users {
  id uuid [pk]
  email varchar [unique]
  phone varchar
  status varchar
  created_at timestamp
}

Table user_addresses {
  id uuid [pk]
  user_id uuid
  address json
}

### Project notifications_db {
  database_type: "PostgreSQL"
}

Table notifications {
  id uuid [pk]
  user_id uuid
  type varchar
  payload json
  status varchar
  created_at timestamp
}

### EVENT INFRASTRUCTURE (EACH DB HAS ITS OWN)
Table domain_outbox_events {
  id uuid [pk]
  aggregate_type varchar
  aggregate_id uuid
  event_type varchar
  payload json
  created_at timestamp
  processed boolean
}
