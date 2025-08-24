apiexpress clone API Documentation To Handle 1 billion/trilion users

🎨 Accounts / Identity API – Enhanced ViewSets Overview
🛠️ API Highlights
| **ViewSet**                 | **List Endpoint**             | **Retrieve Endpoint**            | **Special Features**                                                  | **Caching**                      | **Filtering/Sorting**     | **Bulk Support** | **Notes**                                                                |
| --------------------------- | ----------------------------- | -------------------------------- | --------------------------------------------------------------------- | -------------------------------- | ------------------------- | ---------------- | ------------------------------------------------------------------------ |
| `UserViewSet`               | `GET /api/users/`             | `GET /api/users/{id}/`           | Role-based (buyer/seller/admin), KYC status tracking, last login info | ⚠️ Partial (profile cache)       | ✅ Yes (role, KYC, active) | 🚧 Planned       | Admin-only for list; normal users can only view/update their own profile |
| `AuthViewSet`               | `POST /api/auth/login/`       | ❌                                | JWT login, refresh tokens, device binding                             | ✅ Yes (short-lived JWT in Redis) | ❌                         | ❌                | SSR-ready (HttpOnly cookie refresh) for Nuxt3                            |
| `LogoutViewSet`             | `POST /api/auth/logout/`      | ❌                                | Token/session invalidation, multi-device support                      | ✅ Yes (Redis token blacklist)    | ❌                         | ❌                | Revokes all tokens for given device                                      |
| `PasswordResetViewSet`      | `POST /api/password/request/` | `POST /api/password/reset/`      | Issues one-time reset tokens, tracks expiry & usage                   | ❌ No                             | ❌                         | ❌                | Reset flow triggers async email/SMS event                                |
| `DeviceViewSet`             | `GET /api/devices/`           | `GET /api/devices/{id}/`         | Multi-device login mgmt, push token storage                           | ✅ Yes (last-active cache)        | ✅ Yes (device type, user) | ✅ Yes            | Lets users revoke lost/stolen devices                                    |
| `KYCViewSet`                | `POST /api/kyc/submit/`       | `GET /api/kyc/status/{user_id}/` | Document upload, approval workflow, async processing                  | ❌ No                             | ✅ Yes (status, date)      | ❌                | On approval → user role auto-upgraded to `seller`                        |
| `SessionViewSet` (optional) | `GET /api/sessions/`          | `GET /api/sessions/{id}/`        | Active session listing for user; force logout support                 | ✅ Yes (Redis-backed)             | ✅ Yes (ip, device, user)  | ❌                | Useful for security dashboards                                     
      |
🎨 Permissions & Roles API – Enhanced ViewSets Overview
🛠️ API Highlights
| **ViewSet**                      | **List Endpoint**                | **Retrieve Endpoint**                 | **Special Features**                                                                                    | **Caching**                       | **Filtering/Sorting**               | **Bulk Support** | **Notes**                                                    |
| -------------------------------- | -------------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------- | ----------------------------------- | ---------------- | ------------------------------------------------------------ |
| `RoleViewSet`                    | `GET /api/roles/`                | `GET /api/roles/{id}/`                | Manages roles (`admin`, `seller`, `buyer`); role assignment to users                                    | ❌ No                              | ✅ Yes (role name)                   | ✅ Yes            | Admin-only; assigns roles to users                           |
| `PermissionViewSet`              | `GET /api/permissions/`          | `GET /api/permissions/{id}/`          | Manages system-wide permissions (CRUD per resource)                                                     | ❌ No                              | ✅ Yes (resource, action)            | ✅ Yes            | Super-admin only                                             |
| `UserRoleViewSet`                | `GET /api/user-roles/`           | `GET /api/user-roles/{id}/`           | Mapping of users ↔ roles; supports multiple roles per user                                              | ✅ Yes (per-user cache)            | ✅ Yes (user, role)                  | ✅ Yes            | Useful for audit dashboards                                  |
| `OrderPermissionViewSet`         | `GET /api/order-permissions/`    | `GET /api/order-permissions/{id}/`    | Object-level permissions for Orders (buyer = own orders, seller = orders with their items, admin = all) | ✅ Yes (query result caching)      | ✅ Yes (order\_id, user\_id, role)   | ❌ No             | Enforced dynamically at request level                        |
| `ReturnPermissionViewSet`        | `GET /api/return-permissions/`   | `GET /api/return-permissions/{id}/`   | Controls who can view/approve refunds (buyer can request, seller can respond, admin can override)       | ⚠️ Partial (status checks cached) | ✅ Yes (return\_id, status, role)    | ❌ No             | Integrated into return/refund workflow                       |
| `ShipmentPermissionViewSet`      | `GET /api/shipment-permissions/` | `GET /api/shipment-permissions/{id}/` | Controls shipment visibility (buyer sees own shipments, seller sees shipments they fulfill)             | ✅ Yes (tracking cache)            | ✅ Yes (shipment\_id, carrier, role) | ❌ No             | Helps ensure sellers don’t see buyer info from other sellers |
| `AdminOverridePermissionViewSet` | `GET /api/admin-overrides/`      | `GET /api/admin-overrides/{id}/`      | Lets admins temporarily override role checks for critical flows                                         | ❌ No                              | ✅ Yes (resource, user\_id)          | ❌ No             | Logs every override via Kafka → AuditLog                     |



# Products API – ViewSets Documentation

This document describes all the API **ViewSets** available in `products/api/viewsets.py`.  


## 🎨 Products Table API – Enhanced ViewSets Overview

| **ViewSet**                | **List Endpoint**                | **Retrieve Endpoint**              | **Special Features**         | **Caching**         | **Filtering/Sorting** | **Bulk Support** | **Notes**                       |
|----------------------------|----------------------------------|------------------------------------|------------------------------|---------------------|-----------------------|------------------|----------------------------------|
| `ProductsViewSet`          | `GET /api/products/`             | `GET /api/products/{id}/`          | Cache + Cursor Pagination    | ✅ Yes (list/single) | ✅ Yes                | 🚧 Planned       | Most traffic, optimize prefetch  |
| `CategoryViewSet`          | `GET /api/categories/`           | `GET /api/categories/{id}/`        | Hierarchical categories      | ❌ No                | ✅ Yes                | ✅ Yes           | Good for faceted search          |
| `BrandViewSet`             | `GET /api/brands/`               | `GET /api/brands/{id}/`            | Simple retrieval             | ❌ No                | ✅ Yes                | ✅ Yes           | Frequently cached                |
| `ProductImageViewSet`      | `GET /api/product-images/`       | `GET /api/product-images/{id}/`    | CDN recommended              | ❌ No                | ⚠️ Limited            | ✅ Yes           | Consider CDN for images          |
| `ProductVariantViewSet`    | `GET /api/variants/`             | `GET /api/variants/{id}/`          | Variant options              | ❌ No                | ✅ Yes                | ✅ Yes           | Heavy prefetching                |
| `ProductAttributeViewSet`  | `GET /api/attributes/`           | `GET /api/attributes/{id}/`        | Lightweight attributes       | ❌ No                | ✅ Yes                | ✅ Yes           | Lightweight                      |
| `InventoryViewSet`         | `GET /api/inventory/`            | `GET /api/inventory/{id}/`         | Stock tracking, real-time    | ❌ No                | ✅ Yes                | ✅ Yes           | Should be real-time              |

---

## 🎨 Cart & Wishlist Table API – Enhanced ViewSets Overview
### 🛠️ API Highlights

| **ViewSet**           | **List Endpoint**          | **Retrieve Endpoint**           | **Special Features**            | **Caching**        | **Filtering/Sorting** | **Bulk Support** | **Notes**                                     |
| --------------------- | -------------------------- | ------------------------------- | ------------------------------- | ------------------ | --------------------- | ---------------- | --------------------------------------------- |
| `CartViewSet`         | `GET /api/cart/`           | `GET /api/cart/{id}/`           | Auto-create, per-user isolation | ✅ Yes (per-user)   | ⚠️ Limited            | 🚧 Planned       | One active cart per user; merge on login      |
| `CartItemViewSet`     | `GET /api/cart-items/`     | `GET /api/cart-items/{id}/`     | Add/Update/Delete products      | ✅ Yes (items list) | ✅ Yes                 | ✅ Yes            | Idempotent add-to-cart, optimistic locking    |
| `WishlistViewSet`     | `GET /api/wishlists/`      | `GET /api/wishlists/{id}/`      | Simple, user-specific           | ❌ No               | ✅ Yes                 | 🚧 Planned       | Typically 1 wishlist per user                 |
| `WishlistItemViewSet` | `GET /api/wishlist-items/` | `GET /api/wishlist-items/{id}/` | Add/Remove wishlist items       | ❌ No               | ✅ Yes                 | ✅ Yes            | Consider async events → recommendation engine |


## 🎨 SearchViewSet Table API – Enhanced ViewSets Overview
### 🛠️ API Highlights

| **ViewSet**                 | **List Endpoint**                     | **Retrieve Endpoint**                    | **Special Features**                 | **Caching**         | **Filtering/Sorting** | **Bulk Support** | **Notes**                                    |
| --------------------------- | ------------------------------------- | ---------------------------------------- | ------------------------------------ | ------------------- | --------------------- | ---------------- | -------------------------------------------- |
| `SearchViewSet`             | `GET /api/search/`                    | –                                        | Full-text, Faceted, Sorting          | ✅ Yes (query cache) | ✅ Yes                 | 🚧 Planned       | Backed by ElasticSearch                      |
| `RecommendationViewSet`     | `GET /api/recommendations/user/{id}/` | `GET /api/recommendations/product/{id}/` | Personalized, Trending, Also Bought  | ✅ Yes (per-user)    | ⚠️ Limited            | ❌ No             | Realtime from cache or ML service            |
| `RecommendationRuleViewSet` | `GET /api/rules/`                     | `GET /api/rules/{id}/`                   | Manage rule-based recommendations    | ❌ No                | ✅ Yes                 | ✅ Yes            | Admin-only                                   |
| `RecommendationLogViewSet`  | `GET /api/logs/`                      | `GET /api/logs/{id}/`                    | User-product recommendation tracking | ❌ No                | ✅ Yes                 | ✅ Yes            | Heavy writes → use Kafka → async persistence |


## 🎨 Order Table API – Enhanced ViewSets Overview
### 🛠️ API Highlights

| **ViewSet**        | **List Endpoint**       | **Retrieve Endpoint**        | **Special Features**                                     | **Caching**                  | **Filtering/Sorting**        | **Bulk Support** | **Notes**                                                                 |
| ------------------ | ----------------------- | ---------------------------- | -------------------------------------------------------- | ---------------------------- | ---------------------------- | ---------------- | ------------------------------------------------------------------------- |
| `OrderViewSet`     | `GET /api/orders/`      | `GET /api/orders/{id}/`      | Lifecycle mgmt (pending → delivered), multi-seller split | ✅ Yes (recent orders cache)  | ✅ Yes (status, date, user)   | 🚧 Planned       | Event-driven (`order.created`, `order.paid`) integrated with Kafka/Rabbit |
| `OrderItemViewSet` | `GET /api/order-items/` | `GET /api/order-items/{id}/` | Per-seller item breakdown, SKU & pricing details         | ⚠️ Partial (per-order cache) | ✅ Yes (seller, product, SKU) | ✅ Yes            | Supports seller dashboards for granular item visibility                   |
| `ShipmentViewSet`  | `GET /api/shipments/`   | `GET /api/shipments/{id}/`   | Tracks carrier, tracking no., delivery status            | ✅ Yes (tracking info 15 min) | ✅ Yes (carrier, status)      | ❌ No             | Integrated w/ external carriers (FedEx, DHL, etc.)                        |
| `ReturnViewSet`    | `GET /api/returns/`     | `GET /api/returns/{id}/`     | Handles returns/refunds, return reasons                  | ❌ No                         | ✅ Yes (status, date)         | ✅ Yes            | Event `order.returned` → triggers refund workflows                        |






📖 Full Backend API Overview (Accounts + Orders + Permissions)
🛠️ API Mega-Table
| **Module**      | **ViewSet / Service**       | **List Endpoint**                | **Retrieve Endpoint**                 | **Special Features**                                                      | **Caching**                    | **Filtering/Sorting**         | **Bulk Support** | **Notes**                                       |
| --------------- | --------------------------- | -------------------------------- | ------------------------------------- | ------------------------------------------------------------------------- | ------------------------------ | ----------------------------- | ---------------- | ----------------------------------------------- |
| **Accounts**    | `UserViewSet`               | `GET /api/users/`                | `GET /api/users/{id}/`                | Core user management (admin only)                                         | ❌ No                           | ✅ Yes (email, role, active)   | 🚧 Planned       | Passwords handled via auth service              |
|                 | `AuthViewSet`               | `POST /api/login/`               | ❌                                     | JWT/OAuth2 login, refresh token                                           | ⚡ Token-level cache in Redis   | ❌ No                          | ❌ No             | Social logins optional                          |
|                 | `RegisterViewSet`           | `POST /api/register/`            | ❌                                     | User signup (buyer/seller)                                                | ❌ No                           | ❌ No                          | ❌ No             | Triggers welcome email event                    |
|                 | `ProfileViewSet`            | `GET /api/profile/`              | `PATCH /api/profile/{id}/`            | Profile read/update; buyer/seller KYC status                              | ✅ Yes (per-user profile cache) | ❌ No                          | ❌ No             | Object-level perms enforced                     |
|                 | `KYCViewSet`                | `POST /api/kyc/submit/`          | `GET /api/kyc/status/{user_id}/`      | Seller verification docs upload + approval flow                           | ⚠️ Partial (status cached)     | ✅ Yes (status, date)          | ❌ No             | Event-driven updates via Kafka                  |
|                 | `PasswordResetViewSet`      | `POST /api/password/reset/`      | `GET /api/password/reset/{token}/`    | Password reset with expiring token                                        | ❌ No                           | ❌ No                          | ❌ No             | Token one-time use                              |
| **Orders**      | `OrderViewSet`              | `GET /api/orders/`               | `GET /api/orders/{id}/`               | Lifecycle (pending → delivered), multi-seller split                       | ✅ Yes (recent orders cache)    | ✅ Yes (status, date, user)    | 🚧 Planned       | Emits events `order.created`, `order.paid`      |
|                 | `OrderItemViewSet`          | `GET /api/order-items/`          | `GET /api/order-items/{id}/`          | Seller-level breakdown of SKUs, pricing                                   | ⚠️ Partial (per-order cache)   | ✅ Yes (seller, SKU, product)  | ✅ Yes            | Supports seller dashboards                      |
|                 | `ShipmentViewSet`           | `GET /api/shipments/`            | `GET /api/shipments/{id}/`            | Tracks carrier, tracking no., delivery status                             | ✅ Yes (tracking cache, 15 min) | ✅ Yes (carrier, status)       | ❌ No             | Linked with external carriers (DHL/FedEx APIs)  |
|                 | `ReturnViewSet`             | `GET /api/returns/`              | `GET /api/returns/{id}/`              | Handles return/refund lifecycle                                           | ❌ No                           | ✅ Yes (status, date, reason)  | ✅ Yes            | Event `order.returned` triggers refund pipeline |
| **Permissions** | `RoleViewSet`               | `GET /api/roles/`                | `GET /api/roles/{id}/`                | Role CRUD (`admin`, `seller`, `buyer`)                                    | ❌ No                           | ✅ Yes (role)                  | ✅ Yes            | Admin-only                                      |
|                 | `PermissionViewSet`         | `GET /api/permissions/`          | `GET /api/permissions/{id}/`          | CRUD on resource/action permissions                                       | ❌ No                           | ✅ Yes (resource, action)      | ✅ Yes            | Super-admin only                                |
|                 | `UserRoleViewSet`           | `GET /api/user-roles/`           | `GET /api/user-roles/{id}/`           | Maps users ↔ roles (multiple possible)                                    | ✅ Yes (per-user cache)         | ✅ Yes (user, role)            | ✅ Yes            | Core for audit dashboards                       |
|                 | `OrderPermissionViewSet`    | `GET /api/order-permissions/`    | `GET /api/order-permissions/{id}/`    | Object-level perms: buyer=own orders, seller=their orders, admin=all      | ✅ Yes (query cache)            | ✅ Yes (order\_id, user, role) | ❌ No             | Enforced in DRF `has_object_permission`         |
|                 | `ReturnPermissionViewSet`   | `GET /api/return-permissions/`   | `GET /api/return-permissions/{id}/`   | Buyer requests, seller approves, admin override                           | ⚠️ Partial (status cached)     | ✅ Yes (status, role)          | ❌ No             | Hooks into refund workflow                      |
|                 | `ShipmentPermissionViewSet` | `GET /api/shipment-permissions/` | `GET /api/shipment-permissions/{id}/` | Buyer sees own shipments, seller sees fulfilled shipments, admin sees all | ✅ Yes (tracking cache)         | ✅ Yes (shipment\_id, carrier) | ❌ No             | Privacy boundary for cross-seller visibility    |
|                 | `AdminOverrideViewSet`      | `GET /api/admin-overrides/`      | `GET /api/admin-overrides/{id}/`      | Emergency admin override on permissions                                   | ❌ No                           | ✅ Yes (resource, user\_id)    | ❌ No             | Logged to Kafka → AuditLog                      |
