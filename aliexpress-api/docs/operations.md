# Backend Operations

## Settings Selection

- Local Django commands default to `configs.settings.dev`.
- Deployments must set `DJANGO_SETTINGS_MODULE=configs.settings.prod` explicitly.
- ASGI and WSGI default to production settings and fail safely when required production values are missing.

Copy `.env.example` to `.env` for local development. Never commit the real `.env` file.

## Required Production Configuration

- `SECRET_KEY` and `JWT_SIGNING_KEY`
- `ALLOWED_HOSTS`
- `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, and `DB_PORT`
- `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS` when the frontend is hosted on a different origin

Production uses secure cookies, HSTS, HTTPS redirect, secure proxy headers, and PostgreSQL connection reuse. Deploy behind a proxy that sets `X-Forwarded-Proto: https`; otherwise configure `SECURE_SSL_REDIRECT=false` only as a temporary, reviewed exception.

## Runtime Endpoints

- `/healthz/` is a liveness endpoint. It confirms that the process can respond.
- `/readyz/` is a readiness endpoint. It verifies that the configured database accepts a query.
- `/api/schema/` exposes the OpenAPI schema.

Load balancers should use liveness for restarts and readiness for traffic routing. Do not expose admin, schema UIs, or debug tooling publicly without access controls.

## Local Verification

```powershell
cd aliexpress-api/aliexpressapi
uv sync --group dev
uv run ruff check .
uv run pytest
uv run manage.py check --settings=configs.settings.dev
```

## Verified Integration Boundaries

The current integration suite verifies these server-side behaviors:

- Unauthenticated requests cannot access cart, order, checkout, inventory, or seller routes.
- Public catalog endpoints remain available without authentication.
- A user must verify an account before receiving login tokens.
- An authenticated buyer can add a product variant to their own cart and increment its quantity.
- Cart commands use Pydantic models: UUIDs, strict positive quantities, and unknown fields are rejected with a structured client error rather than causing a server error.

The suite does not yet prove checkout pricing, inventory reservation, payment callbacks, or order ownership. Treat those flows as incomplete until their transactional and idempotency tests exist.

## Checkout Guarantees

The current checkout endpoint requires an `Idempotency-Key` UUID header. Within one database transaction it:

- Returns the original order for a repeated key from the same authenticated buyer.
- Locks the buyer's active cart and the involved product variants before mutation.
- Revalidates variant availability and stock, snapshots current variant prices, and decrements stock only when an order is created.
- Deactivates and locks the completed cart, while enforcing one active cart per authenticated buyer.
- Scopes idempotency keys to the buyer, so separate buyers may safely use the same key.

This is an order-creation and inventory-reservation boundary only. It does not charge a payment method, persist shipping details, publish an event, or implement compensation for cancelled/expired orders. Do not connect a payment provider until a transactional outbox and webhook verification flow are implemented.

Apply the included order and cart migrations before deployment:

```powershell
uv run manage.py migrate --settings=configs.settings.prod
```

## Next Hardening Work

1. Add shipping-address and payment-intent domains with Pydantic commands and contract tests.
2. Implement a transactional outbox, signed webhook verification, and compensation paths for payment failures, expiry, cancellation, and refunds.
3. Add structured request IDs, JSON logging, metrics, and alerting around checkout, inventory, and webhooks.
4. Add dependency/security scanning, concurrent checkout tests against PostgreSQL, and browser end-to-end checkout coverage to CI.
