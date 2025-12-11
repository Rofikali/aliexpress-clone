//// Auto-converted DBML from Django graph_models output
//// Clean short names, A → Z (tables + refs)

Table log_entries {
  id bigint [pk, increment]
  content_type_id int
  user_id uuid
  action_flag smallint
  action_time datetime
  change_message text
  object_id text
  object_repr varchar
}

Table permissions {
  id bigint [pk, increment]
  content_type_id int
  codename varchar
  name varchar
}

Table groups {
  id bigint [pk, increment]
  name varchar
}

Table content_types {
  id bigint [pk, increment]
  app_label varchar
  model varchar
}

Table sessions {
  session_key varchar [pk]
  expire_date datetime
  session_data text
}

Table outstanding_tokens {
  id bigint [pk, increment]
  user_id uuid
  created_at datetime
  expires_at datetime
  jti varchar
  token text
}

Table blacklisted_tokens {
  id bigint [pk, increment]
  token_id bigint
  blacklisted_at datetime
}

Table homepage_sections {
  id uuid [pk]
  created_at datetime
  is_active boolean
  metadata json
  position int
  slug varchar
  title varchar
  type varchar
  updated_at datetime
}

Table homepage_banners {
  id uuid [pk]
  section_id uuid
  alt_text varchar
  created_at datetime
  image varchar
  is_active boolean
  link_url varchar
  sort_order int
  title varchar
  updated_at datetime
}

Table homepage_products {
  id uuid [pk]
  product_id uuid
  section_id uuid
  featured_rank int
  sort_order int
}

Table homepage_categories {
  id uuid [pk]
  category_id bigint
  section_id uuid
  sort_order int
}

Table users {
  id uuid [pk]
  created_at datetime
  email varchar
  is_active boolean
  is_email_verified boolean
  is_staff boolean
  is_superuser boolean
  kyc_status varchar
  last_login datetime
  password varchar
  phone_number varchar
  role varchar
  updated_at datetime
  username varchar
}

Table user_devices {
  id uuid [pk]
  user_id uuid
  created_at datetime
  device_token varchar
  device_type varchar
  ip_address varchar
  last_active datetime
  updated_at datetime
  user_agent text
}

Table password_reset_tokens {
  id uuid [pk]
  user_id uuid
  created_at datetime
  expires_at datetime
  token varchar
  used boolean
}

Table kyc_applications {
  id uuid [pk]
  reviewed_by uuid
  user_id uuid
  notes text
  reviewed_at datetime
  status varchar
  submitted_at datetime
}

Table kyc_documents {
  id uuid [pk]
  application_id uuid
  document_type varchar
  file varchar
  uploaded_at datetime
}

Table email_verifications {
  id uuid [pk]
  user_id uuid
  code varchar
  created_at datetime
  expires_at datetime
  is_used boolean
  used_at datetime
}

Table categories {
  id bigint [pk, increment]
  parent_id bigint
  created_at datetime
  description text
  name varchar
  slug varchar
  updated_at datetime
}

Table brands {
  id bigint [pk, increment]
  created_at datetime
  description text
  logo varchar
  name varchar
  slug varchar
  updated_at datetime
}

Table products {
  id uuid [pk]
  brand_id bigint
  category_id bigint
  seller_id uuid
  created_at datetime
  currency varchar
  description text
  discount_price decimal
  image varchar
  is_active boolean
  price decimal
  rating float
  review_count int
  sku varchar
  slug varchar
  stock int
  title varchar
  updated_at datetime
}

Table inventories {
  id bigint [pk, increment]
  product_id uuid
  change int
  created_at datetime
  location varchar
  quantity int
  reason varchar
  reference_id uuid
  sku varchar
  stock int
}

Table product_images {
  id bigint [pk, increment]
  product_id uuid
  alt_text varchar
  created_at datetime
  image varchar
  position int
}

Table product_attributes {
  id uuid [pk]
  created_at datetime
  name varchar
  sort_order int
  updated_at datetime
}

Table product_attribute_values {
  id uuid [pk]
  attribute_id uuid
  created_at datetime
  updated_at datetime
  value varchar
}

Table product_variants {
  id uuid [pk]
  image_id bigint
  product_id uuid
  created_at datetime
  currency varchar
  discount_price decimal
  is_active boolean
  price decimal
  sku varchar
  stock int
  updated_at datetime
}

Table product_variant_values {
  id uuid [pk]
  attribute_id uuid
  value_id uuid
  variant_id uuid
  created_at datetime
  updated_at datetime
}

Table orders {
  id bigint [pk, increment]
  user_id uuid
  created_at datetime
  status varchar
  total_amount decimal
  updated_at datetime
}

Table order_items {
  id bigint [pk, increment]
  order_id bigint
  product_id uuid
  seller_id uuid
  sku varchar
  created_at datetime
  price decimal
  quantity int
  updated_at datetime
}

Table shipments {
  id bigint [pk, increment]
  order_id bigint
  warehouse_inventory_id bigint
  carrier varchar
  created_at datetime
  estimated_delivery datetime
  shipped_at datetime
  status varchar
  tracking_number varchar
  updated_at datetime
}

Table returns {
  id bigint [pk, increment]
  order_item_id bigint
  created_at datetime
  processed_at datetime
  reason text
  status varchar
  updated_at datetime
}

Table carts {
  id bigint [pk, increment]
  user_id uuid
  created_at datetime
  status varchar
  updated_at datetime
}

Table cart_items {
  id bigint [pk, increment]
  cart_id bigint
  product_id uuid
  added_at datetime
  quantity int
  unit_price decimal
}

Table wishlists {
  id bigint [pk, increment]
  user_id uuid
  created_at datetime
  name varchar
}

Table wishlist_items {
  id bigint [pk, increment]
  product_id uuid
  wishlist_id bigint
  added_at datetime
}

Table search_index {
  id bigint [pk, increment]
  brand_id bigint
  category_id bigint
  product_id uuid
  created_at datetime
  description text
  price decimal
  stock int
  title varchar
  updated_at datetime
}

Table recommendation_rules {
  id bigint [pk, increment]
  created_at datetime
  parameters json
  rule_type varchar
  updated_at datetime
}

Table recommendation_logs {
  id bigint [pk, increment]
  product_id uuid
  recommended_product_id uuid
  rule_id bigint
  user_id uuid
  timestamp datetime
}

//// ---------- REFERENCES (foreign keys) ----------

Ref: log_entries.user_id > users.id
Ref: log_entries.content_type_id > content_types.id

Ref: permissions.content_type_id > content_types.id
Ref: groups.id > permissions.id // group-permission many-to-many expressed elsewhere by DB layer

Ref: outstanding_tokens.user_id > users.id
Ref: blacklisted_tokens.token_id > outstanding_tokens.id

Ref: homepage_banners.section_id > homepage_sections.id
Ref: homepage_products.section_id > homepage_sections.id
Ref: homepage_products.product_id > products.id
Ref: homepage_categories.section_id > homepage_sections.id
Ref: homepage_categories.category_id > categories.id

Ref: users.id > groups.id // users.groups (M:N) - note: actual M:N table not shown, DB layer will create
Ref: users.id > permissions.id // users.user_permissions (M:N) - actual M:N join table not shown

Ref: user_devices.user_id > users.id
Ref: password_reset_tokens.user_id > users.id
Ref: kyc_applications.user_id > users.id
Ref: kyc_applications.reviewed_by > users.id
Ref: kyc_documents.application_id > kyc_applications.id
Ref: email_verifications.user_id > users.id

Ref: categories.parent_id > categories.id

Ref: products.seller_id > users.id
Ref: products.category_id > categories.id
Ref: products.brand_id > brands.id

Ref: inventories.product_id > products.id
Ref: product_images.product_id > products.id

Ref: product_attribute_values.attribute_id > product_attributes.id
Ref: product_variant_values.variant_id > product_variants.id
Ref: product_variant_values.attribute_id > product_attributes.id
Ref: product_variant_values.value_id > product_attribute_values.id

Ref: product_variants.product_id > products.id
Ref: product_variants.image_id > product_images.id

Ref: orders.user_id > users.id
Ref: order_items.order_id > orders.id
Ref: order_items.product_id > products.id
Ref: order_items.seller_id > users.id
Ref: shipments.order_id > orders.id
Ref: shipments.warehouse_inventory_id > inventories.id
Ref: returns.order_item_id > order_items.id

Ref: carts.user_id > users.id
Ref: cart_items.cart_id > carts.id
Ref: cart_items.product_id > products.id
Ref: wishlists.user_id > users.id
Ref: wishlist_items.wishlist_id > wishlists.id
Ref: wishlist_items.product_id > products.id

Ref: search_index.product_id > products.id
Ref: search_index.category_id > categories.id
Ref: search_index.brand_id > brands.id

Ref: recommendation_logs.user_id > users.id
Ref: recommendation_logs.product_id > products.id
Ref: recommendation_logs.recommended_product_id > products.id
Ref: recommendation_logs.rule_id > recommendation_rules.id
