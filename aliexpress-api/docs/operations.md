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

## Local RabbitMQ and Metrics

Start the local broker and Prometheus stack from the repository root:

```powershell
docker compose -f docker-compose.observability.yml up -d
```

RabbitMQ exposes AMQP on `localhost:5672` and its management UI on `http://localhost:15672`. Prometheus is available at `http://localhost:9090` and scrapes the local API's `/metrics/` endpoint. The local compose file creates the durable `marketplace.events` topic exchange and a development queue bound to `#`.

Run the API separately, then dispatch one outbox batch or run the worker continuously:

```powershell
uv run manage.py dispatch_outbox --once
uv run manage.py dispatch_outbox --batch-size 100 --poll-seconds 5
```

The worker requires `RABBITMQ_URL`, `RABBITMQ_EXCHANGE`, `OUTBOX_MAX_ATTEMPTS`, `OUTBOX_RETRY_BASE_SECONDS`, and `OUTBOX_LEASE_SECONDS`. Keep it as a separate process from the web API so broker failures do not exhaust HTTP workers.

## Logging and Metrics

HTTP logs are JSON on standard output and contain `request_id`, `trace_id`, event name, method, path, status, and duration. The API echoes `X-Request-ID` on each response; clients should include it in support reports.

`/metrics/` exports Prometheus request latency/count and outbox-status metrics. Production requires `Authorization: Bearer <METRICS_BEARER_TOKEN>` and network-level restrictions to the monitoring collector. Do not expose this endpoint publicly.

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

This is an order-creation and inventory-reservation boundary only. It does not charge a payment method, persist shipping details, publish an event externally, or implement compensation for cancelled/expired orders. Do not connect a payment provider until an outbox dispatcher and webhook verification flow are implemented.

## Transactional Outbox

Successful checkout now persists an `order.created` event in the same database transaction as the order, inventory reservation, and cart deactivation. The event payload is typed, is unique per order/event type, and begins in the `PENDING` state. A rejected checkout or an idempotent replay does not create another event.

The outbox dispatcher now claims due events with a processing lease, increments attempts, applies bounded exponential backoff, reclaims expired leases, and records terminal failures. It invokes a publisher only after the claim transaction commits and marks an event `PUBLISHED` only after that publisher returns successfully. The RabbitMQ publisher uses a durable topic exchange, persistent messages, mandatory routing, and publisher confirms.

Deploy `dispatch_outbox` as a dedicated worker with a RabbitMQ URL configured through environment variables. Delivery is at-least-once: downstream consumers must deduplicate by event ID and be safe when receiving the same event again. Alert on pending-event age, processing-lease age, retry count, failed-event count, queue depth, and consumer lag; reconcile orders that do not have their expected published event.

Apply the included order and cart migrations before deployment:

```powershell
uv run manage.py migrate --settings=configs.settings.prod
```

## Next Hardening Work

1. Add RabbitMQ consumer modules, dead-letter queues, replay tooling, and a reconciliation dashboard.
2. Add shipping-address and payment-intent domains with Pydantic commands and contract tests.
3. Implement signed webhook verification and compensation paths for payment failures, expiry, cancellation, and refunds.
4. Add alert rules, PostgreSQL concurrency tests, distributed tracing exports, and browser end-to-end checkout coverage to CI.
