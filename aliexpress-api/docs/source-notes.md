# Existing Backend Notes

This page places the existing backend Markdown files into the backend documentation system. They live under `docs/reference/`, grouped by their purpose.

## Authority Order

1. `docs/` at repository root: system-wide decisions and roadmap.
2. This `aliexpress-api/docs/` directory: backend implementation rules.
3. The source notes below: useful designs, API examples, and migration reference.

When documents conflict, follow the higher item. Update or replace the older note as part of the change; do not silently choose between two designs.

## Architecture and Governance

- [Migration checklist](reference/architecture/django_to_ddd_checklist.md): adopt its gradual, domain-by-domain migration approach.
- [DDD rules](reference/architecture/DDD_Rules.md): preserve the order, inventory, payment, and query/write boundary rules.
- [System overview](reference/architecture/core/ARCHITECTURE.md), [guardrails](reference/architecture/core/governance/guardrails/cli_policies.md), and [review checklist](reference/architecture/core/governance/architecture_reviews/review_checklist.md): use as review inputs; align future CI checks with them.
- [Monolith-to-microservices plan](reference/architecture/MONOLITH_TO_MICROSERVICES.md) and [repository split strategy](reference/architecture/REPO_SPLIT_STRATEGY.md): reference only after the extraction criteria in `docs/architecture-roadmap.md` are met.
- [Architecture handbook](reference/architecture/ARCHITECTURE_HANDBOOK.md), [cheat sheet](reference/architecture/ARCHITECTURE_CHEAT_SHEET.md), [clean/hexagonal structure](reference/architecture/DDD_Clean_Hexagonal_Struct.md), and [staff-level structure](reference/architecture/ALIEXPRESS-CLONE%20%E2%80%94%20STAFF-LEVEL%20FOLDER%20STRUCTURE%20%28V1%29.md): design reference material, not a mandate for a big-bang rewrite.

## Domain Design Notes

These LLD/HLD notes define useful domain candidates. Convert each selected workflow into a versioned application use case, invariants, and tests before implementing it.

- [Service map](reference/design-patterns/aliexpress_clone.md)
- [Accounts](reference/design-patterns/accounts_searvice_design.md)
- [Products](reference/design-patterns/products_service_design.md)
- [Cart and wishlist](reference/design-patterns/card%26wishtlist_service_design.md)
- [Orders](reference/design-patterns/order_service_design.md)
- [Payments](reference/design-patterns/payment_service_design.md)
- [Shipping and inventory](reference/design-patterns/shipping_%26_logistics_service_design.md)
- [Search](reference/design-patterns/search_service_design.md)
- [Reviews](reference/design-patterns/review_service_design.md)
- [Notifications](reference/design-patterns/Notifications_service_design.md)

## API and Product Notes

- [API wireframes](reference/api/api_wireframes.md) and [viewset documentation](reference/apps/views.md): endpoint and interaction reference. Reconcile every endpoint against the generated OpenAPI schema before treating it as public.
- [Auth notes](reference/api/auth_md.md), [webhooks](reference/webhooks.md), and [automatic router](reference/components/router/auto-route.md): adapter-level reference.
- [Product responses](reference/api/products/products_md.md), [variants](reference/api/products/product_variant_res.md), [attributes](reference/api/products/product_attributes_res.md), and [product frontend needs](reference/api/products/products_frontend.md): contract-design reference shared with Nuxt work.
- [Delivery steps](reference/schemas/Steps%20%28%20Start%20To%20Production%20%29.md), [cart architecture](reference/apps/carts/archetech.md), and [product architecture](reference/apps/products/archetech.md): implementation notes to refine as those modules are migrated.
