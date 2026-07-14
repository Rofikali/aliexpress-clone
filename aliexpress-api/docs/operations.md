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

## Next Hardening Work

1. Audit object-level authorization for every authenticated route, especially cart, order, checkout, payment, and inventory ownership.
2. Add structured request IDs, JSON logging, metrics, and alerting around checkout, payments, inventory, and webhooks.
3. Add database migration checks, dependency/security scanning, and authenticated endpoint tests to CI.
4. Implement durable idempotency and transactional outbox processing before enabling real payment providers.
