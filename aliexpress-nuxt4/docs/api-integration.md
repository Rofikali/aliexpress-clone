# Frontend API Integration

## Transport Contract

- Browser code calls the same-origin `/api/backend` Nuxt BFF. Configure the private DRF origin with `NUXT_API_INTERNAL_BASE` at deployment time.
- Centralize timeouts and request IDs in `app/plugins/axios.js`; the BFF owns authorization headers and one-time token refresh. Normalize responses and errors in `app/utils/api/base.ts`.
- Map backend error `code` values to user-safe messages at the feature boundary.
- Retry only safe idempotent reads automatically. Checkout/payment actions need a client-generated idempotency key and clear recovery UI.

## API Type Safety

Use the DRF OpenAPI schema as the source for generated or validated TypeScript types. CI should fail when a frontend client depends on a removed/changed contract without an approved version migration.

## Authentication

- Tokens are stored in `HttpOnly`, `SameSite` BFF cookies and must never enter Pinia state, browser storage, or frontend API response bodies.
- Treat the backend as the authorization source of truth; route middleware improves UX but is not security.
- On a refresh failure, clear client session state consistently and redirect to sign-in with a safe return URL.
- The BFF proxy must remain same-origin, use `Secure` cookies under HTTPS, and pass only allow-listed request headers to DRF.

## Frontend Release Safety

- Support old and new API response shapes during backend rollout when needed.
- Gate unfinished flows with feature flags rather than dead routes.
- Add component/unit tests per feature and browser tests for sign-in, cart, checkout, and order history.
