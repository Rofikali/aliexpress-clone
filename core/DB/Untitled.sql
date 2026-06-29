CREATE TABLE "products" (
  "id" uuid PRIMARY KEY,
  "seller_id" uuid,
  "title" varchar,
  "description" text,
  "category_id" uuid,
  "status" varchar,
  "created_at" timestamp,
  "updated_at" timestamp
);

CREATE TABLE "product_variants" (
  "id" uuid PRIMARY KEY,
  "product_id" uuid,
  "sku" varchar UNIQUE,
  "attributes" json,
  "created_at" timestamp
);

CREATE TABLE "product_prices" (
  "id" uuid PRIMARY KEY,
  "variant_id" uuid,
  "currency" varchar,
  "amount" decimal,
  "valid_from" timestamp,
  "valid_to" timestamp
);

CREATE TABLE "product_images" (
  "id" uuid PRIMARY KEY,
  "product_id" uuid,
  "url" varchar,
  "sort_order" int
);

CREATE TABLE "carts" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "status" varchar,
  "expires_at" timestamp,
  "created_at" timestamp
);

CREATE TABLE "cart_items" (
  "id" uuid PRIMARY KEY,
  "cart_id" uuid,
  "product_id" uuid,
  "variant_id" uuid,
  "quantity" int,
  "price_snapshot" json
);

CREATE TABLE "orders" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "order_number" varchar UNIQUE,
  "status" varchar,
  "total_amount" decimal,
  "currency" varchar,
  "created_at" timestamp
);

CREATE TABLE "order_items" (
  "id" uuid PRIMARY KEY,
  "order_id" uuid,
  "product_id" uuid,
  "variant_id" uuid,
  "quantity" int,
  "unit_price" decimal,
  "total_price" decimal
);

CREATE TABLE "order_addresses" (
  "id" uuid PRIMARY KEY,
  "order_id" uuid,
  "type" varchar,
  "address" json
);

CREATE TABLE "order_state_transitions" (
  "id" uuid PRIMARY KEY,
  "order_id" uuid,
  "from_state" varchar,
  "to_state" varchar,
  "changed_at" timestamp
);

CREATE TABLE "payments" (
  "id" uuid PRIMARY KEY,
  "order_id" uuid,
  "status" varchar,
  "amount" decimal,
  "currency" varchar,
  "provider" varchar,
  "created_at" timestamp
);

CREATE TABLE "payment_transactions" (
  "id" uuid PRIMARY KEY,
  "payment_id" uuid,
  "provider_txn_id" varchar,
  "type" varchar,
  "amount" decimal,
  "status" varchar,
  "created_at" timestamp
);

CREATE TABLE "payment_idempotency_keys" (
  "id" uuid PRIMARY KEY,
  "key" varchar UNIQUE,
  "request_hash" varchar,
  "created_at" timestamp
);

CREATE TABLE "inventory_items" (
  "id" uuid PRIMARY KEY,
  "product_id" uuid,
  "variant_id" uuid,
  "total_stock" int
);

CREATE TABLE "inventory_reservations" (
  "id" uuid PRIMARY KEY,
  "order_id" uuid,
  "variant_id" uuid,
  "quantity" int,
  "status" varchar,
  "expires_at" timestamp
);

CREATE TABLE "checkout_sessions" (
  "id" uuid PRIMARY KEY,
  "cart_id" uuid,
  "user_id" uuid,
  "status" varchar,
  "created_at" timestamp
);

CREATE TABLE "checkout_steps" (
  "id" uuid PRIMARY KEY,
  "session_id" uuid,
  "step_name" varchar,
  "status" varchar,
  "updated_at" timestamp
);

CREATE TABLE "shipments" (
  "id" uuid PRIMARY KEY,
  "order_id" uuid,
  "carrier" varchar,
  "tracking_number" varchar,
  "status" varchar,
  "shipped_at" timestamp
);

CREATE TABLE "shipment_events" (
  "id" uuid PRIMARY KEY,
  "shipment_id" uuid,
  "status" varchar,
  "occurred_at" timestamp
);

CREATE TABLE "coupons" (
  "id" uuid PRIMARY KEY,
  "code" varchar UNIQUE,
  "discount_type" varchar,
  "discount_value" decimal,
  "valid_from" timestamp,
  "valid_to" timestamp
);

CREATE TABLE "coupon_redemptions" (
  "id" uuid PRIMARY KEY,
  "coupon_id" uuid,
  "user_id" uuid,
  "order_id" uuid,
  "redeemed_at" timestamp
);

CREATE TABLE "users" (
  "id" uuid PRIMARY KEY,
  "email" varchar UNIQUE,
  "phone" varchar,
  "status" varchar,
  "created_at" timestamp
);

CREATE TABLE "user_addresses" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "address" json
);

CREATE TABLE "notifications" (
  "id" uuid PRIMARY KEY,
  "user_id" uuid,
  "type" varchar,
  "payload" json,
  "status" varchar,
  "created_at" timestamp
);

CREATE TABLE "product_search_view" (
  "product_id" uuid PRIMARY KEY,
  "title" varchar,
  "category_id" uuid,
  "price_min" decimal,
  "price_max" decimal,
  "searchable_text" text
);

CREATE TABLE "domain_outbox_events" (
  "id" uuid PRIMARY KEY,
  "aggregate_type" varchar,
  "aggregate_id" uuid,
  "event_type" varchar,
  "payload" json,
  "created_at" timestamp,
  "processed" boolean
);

CREATE TABLE "audit_logs" (
  "id" uuid PRIMARY KEY,
  "actor_id" uuid,
  "action" varchar,
  "entity" varchar,
  "entity_id" uuid,
  "payload" json,
  "created_at" timestamp
);
