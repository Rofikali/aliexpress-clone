### orders

id (UUID, PK)
order_number (VARCHAR, UNIQUE)        -- public reference
buyer_id (UUID)                       -- reference only, no FK
buyer_snapshot (JSONB)                -- name, email, phone
status (VARCHAR)                      -- CREATED, PAID, SHIPPED, COMPLETED, etc
currency (CHAR(3))
subtotal_amount (DECIMAL)
discount_amount (DECIMAL)
tax_amount (DECIMAL)
shipping_amount (DECIMAL)
total_amount (DECIMAL)
payment_status (VARCHAR)
created_at (TIMESTAMP)
confirmed_at (TIMESTAMP, NULL)
cancelled_at (TIMESTAMP, NULL)
completed_at (TIMESTAMP, NULL)

✅ Why this exists

Single source of truth

Auditable

Legal-grade snapshot

Never recalculated

🚫 Never update prices here after creation.

### order_items

id (UUID, PK)
order_id (UUID)
product_id (UUID)
variant_id (UUID)
product_snapshot (JSONB)      -- title, attributes
price_snapshot (JSONB)        -- unit price, discounts
quantity (INT)
total_price (DECIMAL)
created_at (TIMESTAMP)

✅ Why snapshot?

Product price may change tomorrow

Product may be deleted

Order must remain legally valid

🚫 Never join to products table.

### order_addresses
---------------
id (UUID, PK)
order_id (UUID)
type (VARCHAR)                -- SHIPPING / BILLING
address_snapshot (JSONB)      -- full address
created_at (TIMESTAMP)

✅ Why snapshot?

Addresses change. Orders must not.

### order_shipments
---------------
id (UUID, PK)
order_id (UUID)
carrier (VARCHAR)
tracking_number (VARCHAR)
status (VARCHAR)              -- PENDING, SHIPPED, DELIVERED
shipped_at (TIMESTAMP, NULL)
delivered_at (TIMESTAMP, NULL)

✅ Why separate?

Shipment lifecycle ≠ Order lifecycle

Multiple shipments per order possible

### order_refunds
-------------
id (UUID, PK)
order_id (UUID)
payment_id (UUID)
amount (DECIMAL)
reason (VARCHAR)
status (VARCHAR)              -- REQUESTED, APPROVED, PAID
created_at (TIMESTAMP)

✅ Why separate?

Refunds are financial transactions, not order state.

### order_state_history
-------------------
id (UUID, PK)
order_id (UUID)
from_status (VARCHAR)
to_status (VARCHAR)
changed_by (VARCHAR)          -- SYSTEM / USER / ADMIN
created_at (TIMESTAMP)

✅ Why?

Legal disputes

Customer support

Debugging incidents

🚫 Never delete history.

### order_outbox_events
-------------------
id (UUID, PK)
aggregate_id (UUID)
event_type (VARCHAR)
payload (JSONB)
created_at (TIMESTAMP)
published_at (TIMESTAMP, NULL)

✅ Why?

Guaranteed event delivery

Enables saga orchestration

Replayable

Every order state change emits an event.

### order_saga_state
----------------
id (UUID, PK)
saga_type (VARCHAR)           -- CHECKOUT, REFUND
order_id (UUID)
current_step (VARCHAR)
status (VARCHAR)
context (JSONB)
created_at (TIMESTAMP)
updated_at (TIMESTAMP)

✅ Why?

Orders are NOT atomic

Handles partial failures

Enables compensation

### order_list_view
---------------
order_id
order_number
buyer_name
status
total_amount
created_at

### order_detail_view
-----------------
order_id
full_order_payload (JSONB)

### END HERE
✅ Built from events
✅ Rebuildable
🚫 Never source of truth

🔐 CRITICAL DESIGN LAWS (MEMORIZE)
❌ Forbidden

Cross-domain foreign keys

Updating historical prices

Deleting orders

Payment writing to Orders DB

Orders querying Payment DB

✅ Mandatory

Snapshot everything

Append-only philosophy

Outbox for events

Saga for long flows

Read/write separation

🧠 ORDER STATE MACHINE (SUMMARY)
CREATED
  ↓
CONFIRMED
  ↓
PAID
  ↓
SHIPPED
  ↓
COMPLETED

FAILURE PATHS:
CREATED → CANCELLED
PAID → REFUNDED

🏁 FINAL PRINCIPAL-LEVEL TRUTH

Orders DB is a legal ledger, not a CRUD table.
Treat it like a bank statement.