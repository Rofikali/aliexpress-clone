ALIEXPRESS-LEVEL DATABASE DESIGN

Save as:

docs/architecture/database-tables-full.md

1️⃣ PRODUCTS DATABASE (products_db)

Purpose: Product catalog, variants, images, pricing, attributes

Table	Key Columns	Notes
products	id, sku, title, description, category_id, status, created_at, updated_at	Aggregate root
product_variants	id, product_id, attributes_json, price, stock_unit_id	Snapshot per variant
product_images	id, product_id, url, type, position	Multiple images per product
product_pricing	id, product_id, variant_id, base_price, discount, currency, effective_from, effective_to	Time-versioned pricing
product_attributes	id, product_id, name, value, searchable	Denormalized for search
product_publications	id, product_id, status, published_at, unlisted_at	Track marketplace publishing
products_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven propagation

Principle: Products are event-sourced for downstream domains; read-heavy domain.

2️⃣ INVENTORY DATABASE (inventory_db)

Purpose: Track stock, reservations, movements

Table	Key Columns	Notes
stock_items	id, product_id, variant_id, total_quantity, available_quantity, updated_at	Aggregate root
stock_reservations	id, stock_item_id, order_id, quantity, status, expires_at, created_at	Reservation model
stock_movements	id, stock_item_id, change, reason, reference_id, created_at	Append-only
inventory_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event propagation

Principle: Reservation-based, eventual consistency, safe for flash sales.

3️⃣ ORDERS DATABASE (orders_db)

Purpose: Legal and financial record

Table	Key Columns	Notes
orders	id, buyer_id, seller_id, order_number, status, order_type, currency, total_amount, created_at, updated_at	Aggregate root
order_items	id, order_id, product_snapshot_json, price_snapshot, quantity, created_at	Immutable snapshot
order_status_history	id, order_id, from_status, to_status, reason, changed_by, changed_at	Audit trail
order_payments	id, order_id, payment_id, amount, status, created_at	Reference to payments
order_shipments	id, order_id, shipment_id, carrier, tracking_number, status, created_at	Shipment references
order_refunds	id, order_id, refund_id, amount, reason, status, created_at	Refund references
orders_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven integration

Principle: Orders are append-only facts, coordinate via events, never execute external actions.

4️⃣ CART DATABASE (cart_db)

Purpose: Temporary user selections

Table	Key Columns	Notes
carts	id, user_id, status, created_at, updated_at	Aggregate root
cart_items	id, cart_id, product_id, variant_id, quantity, added_at	Snapshot
cart_coupons	id, cart_id, coupon_id, applied_at	Temporary discount application
carts_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Cart events for checkout

Principle: Disposable domain, orchestrates checkout flow, snapshot of intent.

5️⃣ PAYMENTS DATABASE (payments_db)

Purpose: Money safety and financial transactions

Table	Key Columns	Notes
payment_intents	id, order_id, amount, currency, gateway, idempotency_key, status, created_at	Retry-safe
payment_transactions	id, payment_intent_id, gateway_transaction_id, type, amount, status, created_at	Append-only
refunds	id, payment_intent_id, refund_reference, amount, status, created_at	Append-only
ledgers	id, account, debit, credit, currency, reference_id, created_at	Source of truth
payments_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven

Principle: Idempotent, append-only, independent from orders.

6️⃣ CHECKOUT DATABASE (checkout_db)

Purpose: Orchestration layer

Table	Key Columns	Notes
checkout_sessions	id, user_id, cart_id, status, started_at, completed_at	Aggregate root
checkout_steps	id, session_id, step_type, status, attempted_at	Track flow progress
checkout_failures	id, session_id, reason, failed_at	Audit for retries
checkout_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven notifications

Principle: Stateless orchestration, coordinates orders, payments, inventory, coupons.

7️⃣ SHIPPING DATABASE (shipping_db)
Table	Key Columns	Notes
shipments	id, order_id, carrier, tracking_number, status, shipped_at, delivered_at	Aggregate root
shipment_events	id, shipment_id, event_type, payload, created_at	Event sourcing for shipment updates
carrier_integrations	id, carrier_name, api_endpoint, credentials	External service metadata
shipping_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven updates

Principle: Async, eventual consistency, reacts to order events.

8️⃣ COUPONS DATABASE (coupons_db)
Table	Key Columns	Notes
coupons	id, code, type, discount, max_uses, status, valid_from, valid_to	Aggregate root
coupon_rules	id, coupon_id, rule_type, rule_json	Business rules
coupon_redemptions	id, coupon_id, user_id, order_id, redeemed_at	Audit trail
coupons_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven
9️⃣ ACCOUNTS DATABASE (accounts_db)
Table	Key Columns	Notes
users	id, email, password_hash, status, created_at, updated_at	Aggregate root
user_profiles	id, user_id, first_name, last_name, phone, address_json	Snapshot
user_roles	id, user_id, role, assigned_at	Role management
accounts_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven
🔟 NOTIFICATIONS DATABASE (notifications_db)
Table	Key Columns	Notes
notifications	id, user_id, type, payload_json, status, created_at, sent_at	Aggregate root
notification_channels	id, type, provider_info	Email, SMS, Push
notifications_outbox_events	id, aggregate_id, event_type, payload, created_at, published_at	Event-driven
1️⃣1️⃣ SEARCH / READ MODELS (search_db)
Table	Key Columns	Notes
product_search_view	product_id, title, category_id, variant_attributes_json	Denormalized
order_list_view	order_id, buyer_id, status, total_amount, created_at	Customer view
seller_dashboard_view	seller_id, orders_json, revenue	Analytics

Principle: Disposable, rebuildable, eventual consistency.

🧬 OUTBOX / EVENT TABLE RULES

All domains have outbox_events table:

outbox_events
-------------
id (PK)
aggregate_id
event_type
payload (JSONB)
created_at
published_at


Principle: Guarantees async, durable, replayable events for cross-domain coordination.

🧠 PRINCIPAL-LEVEL DATABASE LAWS

1️⃣ Aggregate = transactional boundary
2️⃣ Append-only events wherever possible
3️⃣ Snapshots for mutable external data (products, pricing)
4️⃣ No cross-domain FKs; use IDs only
5️⃣ Idempotency keys for payments, reservations, and checkout
6️⃣ Read models are disposable & replaceable
7️⃣ All domains event-driven via outbox pattern