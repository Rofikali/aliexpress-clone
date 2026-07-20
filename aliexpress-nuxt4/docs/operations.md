# Frontend Operations Guide

## Purpose

The Nuxt storefront is the presentation and client-orchestration boundary for the DRF API. It is deployed as a Node/Nitro server and reads its API location from Nuxt runtime configuration.

## Configuration

Copy `.env.example` to `.env` for local development.

```dotenv
NUXT_PUBLIC_BASE_API=http://localhost:8000/api/v1
```

`NUXT_PUBLIC_BASE_API` is intentionally public because browsers use it. Never put credentials, private keys, broker URLs, or Django secrets in a `NUXT_PUBLIC_*` variable. The configured API must allow the storefront origin through its production CORS configuration.

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

- The Axios plugin adds an `X-Request-ID` to every API request. Preserve this value in frontend error reports and use it to correlate the request with DRF structured logs.
- Checkout creates and sends a UUID `Idempotency-Key`. A retry of the same business action must reuse its key; a newly initiated checkout gets a new key.
- Services normalize API envelopes before stores or components consume them. New services must use `normalizeResponse` and `handleApiError` from `app/utils/api/base.ts` rather than parsing Axios errors ad hoc.
- Automatic retries are appropriate only for safe, idempotent reads. Do not retry checkout, payment, or state-changing writes without an explicit idempotency design.

## Security Boundary

Security headers are set for Nuxt routes in `nuxt.config.ts`. The browser must still enforce HTTPS, a restrictive API CORS allow-list, and a production Content Security Policy at the ingress or application layer.

The current authentication client calls the API directly. Before handling real customer sessions, introduce a Nuxt backend-for-frontend session boundary that stores refresh credentials in `Secure`, `HttpOnly`, `SameSite` cookies and proxies authenticated API requests. Do not persist long-lived bearer or refresh tokens in browser storage.

## Release Checklist

1. Set the production `NUXT_PUBLIC_BASE_API` to the versioned API origin.
2. Run `pnpm typecheck`, `pnpm test:run`, and `pnpm build` against the locked dependencies.
3. Validate sign-in, cart, checkout, and failed-request correlation using an `X-Request-ID`.
4. Confirm the API CORS allow-list, TLS termination, CSP, error reporting, and alert routing.
5. Roll back by redeploying the last known-good frontend artifact; API contract changes require a compatible rollout window.

## Current Gaps

- Browser end-to-end tests for sign-in, cart, and checkout are not implemented yet.
- OpenAPI-generated TypeScript clients and contract-drift checks are not implemented yet.
- Client error telemetry and real-user performance monitoring are not connected yet.
- The direct-browser authentication model must be replaced by the BFF/cookie model before a public production launch.
