# Frontend Operations Guide

## Purpose

The Nuxt storefront is the presentation and client-orchestration boundary for the DRF API. It is deployed as a Node/Nitro server and reads its API location from Nuxt runtime configuration.

## Configuration

Copy `.env.example` to `.env` for local development.

```dotenv
NUXT_API_INTERNAL_BASE=http://localhost:8000/api/v1
NUXT_SESSION_COOKIE_SECURE=false
```

`NUXT_API_INTERNAL_BASE` is server-only. Nuxt proxies browser API requests through `/api/backend`, so the DRF origin, bearer tokens, and refresh token are never exposed to browser JavaScript. Set `NUXT_SESSION_COOKIE_SECURE=true` in production HTTPS deployments. Never put credentials, private keys, broker URLs, or Django secrets in a `NUXT_PUBLIC_*` variable.

## Run and Verify

Run these commands from `aliexpress-nuxt4`.

```powershell
pnpm install --frozen-lockfile
pnpm dev
pnpm typecheck
pnpm test:run
pnpm build
node .output/server/index.mjs
```

The production build emits a Node server in `.output`. Deploy that output with the same supported operating-system architecture as the build when using native dependencies such as `sharp`.

## API Reliability Contract

- The Axios plugin adds an `X-Request-ID` to every API request. The Nuxt proxy forwards it to DRF; preserve it in frontend error reports to correlate with DRF structured logs.
- Checkout creates and sends a UUID `Idempotency-Key`. A retry of the same business action must reuse its key; a newly initiated checkout gets a new key.
- Services normalize API envelopes before stores or components consume them. New services must use `normalizeResponse` and `handleApiError` from `app/utils/api/base.ts` rather than parsing Axios errors ad hoc.
- Automatic retries are appropriate only for safe, idempotent reads. Do not retry checkout, payment, or state-changing writes without an explicit idempotency design.

## Security Boundary

Security headers are set for Nuxt routes in `nuxt.config.ts`. The browser must still enforce HTTPS and a production Content Security Policy at the ingress or application layer.

The Nuxt backend-for-frontend stores access and refresh credentials in `HttpOnly`, `SameSite=Lax` cookies and injects the access token only on server-to-DRF requests. It refreshes an expired access token once, clears an invalid session, and never returns token fields from login, registration, or session responses. Do not persist long-lived bearer or refresh tokens in browser storage.

The BFF endpoints are `/api/auth/login`, `/api/auth/register`, `/api/auth/session`, `/api/auth/logout`, and `/api/backend/**`. Keep Nuxt and the browser on the same public origin. The private DRF origin should not accept arbitrary public browser traffic in production.

## Release Checklist

1. Set `NUXT_API_INTERNAL_BASE` to the private versioned DRF API origin and `NUXT_SESSION_COOKIE_SECURE=true`.
2. Run `pnpm typecheck`, `pnpm test:run`, and `pnpm build` against the locked dependencies.
3. Validate sign-in, cart, checkout, and failed-request correlation using an `X-Request-ID`.
4. Confirm the API CORS allow-list, TLS termination, CSP, error reporting, and alert routing.
5. Roll back by redeploying the last known-good frontend artifact; API contract changes require a compatible rollout window.

## Current Gaps

- The sign-in BFF journey is covered by Playwright; cart, checkout, and refresh browser journeys still need coverage.
- OpenAPI-generated TypeScript clients and contract-drift checks are not implemented yet.
- Client error telemetry and real-user performance monitoring are not connected yet.
- CSRF controls and origin enforcement should be added before accepting cross-site browser integrations.
