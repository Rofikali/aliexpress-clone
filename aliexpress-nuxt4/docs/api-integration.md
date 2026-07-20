# Frontend API Integration

## Transport Contract

- Read `baseApi` from Nuxt runtime configuration and provide environment-specific values through deployment configuration.
- Centralize auth headers, token refresh, timeout, and request IDs in `app/plugins/axios.js`; normalize responses and errors in `app/utils/api/base.ts`.
- Map backend error `code` values to user-safe messages at the feature boundary.
- Retry only safe idempotent reads automatically. Checkout/payment actions need a client-generated idempotency key and clear recovery UI.

## API Type Safety

Use the DRF OpenAPI schema as the source for generated or validated TypeScript types. CI should fail when a frontend client depends on a removed/changed contract without an approved version migration.

## Authentication

- Do not persist sensitive tokens in unsafe browser storage when an HttpOnly-cookie flow is available.
- Treat the backend as the authorization source of truth; route middleware improves UX but is not security.
- On a refresh failure, clear client session state consistently and redirect to sign-in with a safe return URL.
- The current direct-browser flow is transitional. Move refresh credentials to a Nuxt BFF using `Secure`, `HttpOnly`, `SameSite` cookies before public production use.

## Frontend Release Safety

- Support old and new API response shapes during backend rollout when needed.
- Gate unfinished flows with feature flags rather than dead routes.
- Add component/unit tests per feature and browser tests for sign-in, cart, checkout, and order history.
