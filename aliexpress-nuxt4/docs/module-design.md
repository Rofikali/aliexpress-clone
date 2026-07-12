# Frontend Module Design

## Target Structure

```text
app/
  features/
    catalog/       # components, composables, API client, types, tests
    cart/
    checkout/
    orders/
    account/
  shared/
    api/           # transport, auth, error mapping, generated contract types
    ui/            # reusable accessible design-system components
    lib/           # framework-independent helpers
  pages/           # route composition only
  layouts/
  middleware/
```

Migrate feature-by-feature from the existing `components`, `services`, `stores`, and `composables` folders. Do not move files solely to satisfy the diagram.

## Dependency Rules

- Pages compose features; they do not perform raw HTTP calls.
- Feature components render state and emit intent. Feature composables coordinate UI behavior.
- API clients are typed adapters over the shared transport. They do not import Vue components or stores.
- Pinia is for durable cross-page client state (session, cart summary, UI preferences), not every server response.
- Server state has explicit loading, empty, error, and retry states. Avoid duplicate caches without invalidation rules.

## SOLID in Vue/Nuxt

- Keep a component focused on rendering one concern; move multi-step flows into composables.
- Inject transport/configuration at the shared API boundary so it is replaceable in tests.
- Prefer small composables (`useCart`, `useCheckout`) over global god-stores.
- Define API response types at the contract boundary; do not spread untyped `any` through features.

## Accessibility and Performance

- Every interactive component supports keyboard input, focus handling, and accessible labels.
- Use SSR-safe data fetching and avoid browser-only APIs during server rendering.
- Define image sizes, lazy-load noncritical media, and track Core Web Vitals for product/listing pages.
