# Existing Frontend Notes

This page makes the existing frontend Markdown files discoverable from the canonical frontend documentation. They live under `docs/reference/`.

## Authority Order

1. `docs/` at repository root: cross-application architecture decisions.
2. This `aliexpress-nuxt4/docs/` directory: frontend engineering and integration rules.
3. The source notes below: existing feature, wireframe, and folder references.

## Existing Architecture Notes

- [Current frontend README](../README.md): broad project and legacy Nuxt structure reference.
- [Folder flow rules](reference/Folled_rules.md): preserve its intended UI -> service -> store flow, but use the feature-oriented dependency rules in `module-design.md` for new code.
- [Checkout and address structure](reference/nuxt_directory_structer.md): use as the starting feature map for checkout and account-address work.

## Product and Wireframe Notes

- [Frontend wireframes](reference/wireframes/frontend_wireframes.md): page composition and UI inventory reference.
- [Product interaction/API flows](reference/wireframes/products_related.md): catalog, variant, pagination, cart, and checkout interaction reference.

## How to Use These Notes

Before implementing a UI flow, identify its matching backend contract in `aliexpress-api/docs/source-notes.md`, then document the final request/response contract in the OpenAPI schema. The frontend must not invent response shapes or replicate backend checkout, stock, pricing, or authorization rules.
