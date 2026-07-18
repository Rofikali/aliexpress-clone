# AliExpress Clone

A full-stack marketplace project built as a **modular monolith**: a Django REST Framework API and a Nuxt 4 storefront. The project is designed to keep deployment simple today while preserving clear boundaries for future service extraction when there is a real scaling or ownership need.

> **Current status:** active development. The API and frontend structure are in place, but this repository is not production-ready yet. See [Architecture](#architecture) and [Current limitations](#current-limitations) before deploying it.

## Why This Project Exists

This project is a practical e-commerce architecture exercise. It models the core marketplace flows—identity, catalog, cart, checkout, orders, payments, search, and product discovery—while applying maintainable backend and frontend boundaries.

The goal is not to prematurely create microservices. The goal is to build a reliable modular monolith where each business capability has explicit ownership, contracts, tests, and a safe extraction path.

## Capabilities

- Account, authentication, and profile foundations
- Product catalog, categories, variants, attributes, and media
- Cart and wishlist flows
- Checkout and order workflows
- Payment, search, and home API modules
- OpenAPI schema via DRF Spectacular
- Nuxt 4 storefront with Pinia, Nuxt UI, and image support

## Architecture

```text
Browser
  |
  v
Nuxt 4 application (port 3000)
  |
  | HTTP /api/v1
  v
Django REST Framework (port 8000)
  |
  v
SQLite for local development / PostgreSQL for production
```

The target architecture is a modular monolith:

- Each business module owns its models, use cases, adapters, routes, and tests.
- Django/DRF remains at the HTTP and persistence boundary; business rules move toward application and domain layers.
- Cross-module communication uses explicit ports, contracts, and transactional outbox events—not direct model access.
- A module becomes a microservice only after it has a proven boundary and an operational reason to be independently deployed.

Read the architecture guides:

- [System architecture roadmap](docs/architecture-roadmap.md)
- [Backend architecture guide](aliexpress-api/docs/README.md)
- [Backend operations guide](aliexpress-api/docs/operations.md)
- [Frontend architecture guide](aliexpress-nuxt4/docs/README.md)

## Repository Layout

```text
.
├── aliexpress-api/          # Django REST Framework backend
│   ├── aliexpressapi/apps/  # Business modules and Django integration
│   └── docs/                # Backend architecture and reference notes
├── aliexpress-nuxt4/        # Nuxt 4 frontend
│   ├── app/                 # Pages, components, stores, services, composables
│   └── docs/                # Frontend architecture and reference notes
├── core/                    # Earlier domain and architecture exploration
└── docs/                    # Canonical system-level architecture decisions
```

## Prerequisites

- Python version supported by `aliexpress-api/aliexpressapi/pyproject.toml`
- [uv](https://docs.astral.sh/uv/)
- Node.js LTS and pnpm
- PostgreSQL only when using production settings
- Docker Desktop for the local RabbitMQ and Prometheus stack

## Local Development

### 1. Start the API

The development configuration uses SQLite. Set the settings module explicitly so startup does not depend on the current `DEBUG` environment value.

```powershell
cd aliexpress-api/aliexpressapi
uv sync
$env:DJANGO_SETTINGS_MODULE = "configs.settings.dev"
uv run manage.py migrate
uv run manage.py runserver 127.0.0.1:8000
```

Optional local broker and metrics stack:

```powershell
docker compose -f docker-compose.observability.yml up -d
uv run manage.py dispatch_outbox --once
```

Useful endpoints:

- API root: `http://127.0.0.1:8000/api/v1/`
- Liveness: `http://127.0.0.1:8000/healthz/`
- Readiness: `http://127.0.0.1:8000/readyz/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`
- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- Django admin: `http://127.0.0.1:8000/admin/`

### 2. Start the frontend

Open a second terminal:

```powershell
cd aliexpress-nuxt4
pnpm install
pnpm dev
```

Open `http://localhost:3000`.

The Nuxt runtime configuration currently targets `http://localhost:8000/api/v1`.

## Environment Configuration

Copy `aliexpress-api/aliexpressapi/.env.example` to `aliexpress-api/aliexpressapi/.env` and replace its placeholder values. Keep secrets out of source control. Production additionally requires PostgreSQL and explicitly configured hosts/origins.

```dotenv
DEBUG=true
SECRET_KEY=replace-with-a-long-random-development-secret
JWT_SIGNING_KEY=replace-with-a-long-random-jwt-signing-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

For production, set `DEBUG=false` and configure `DB_NAME`, `DB_USER`, `DB_PASS`, `DB_HOST`, and `DB_PORT` with your managed PostgreSQL provider values.

## API Contracts

The backend publishes an OpenAPI schema. Treat that schema as the contract between DRF and Nuxt. New frontend code should use typed API boundary models and should not depend on Django model internals.

## Quality Direction

Staff-level quality is demonstrated by operational discipline, not folder count:

- Thin DRF views that call explicit application use cases
- Domain rules independent of Django/DRF where complexity justifies it
- Database constraints and transaction-safe checkout/payment flows
- Idempotency for payment, checkout, and webhook commands
- Contract, integration, and end-to-end tests for critical journeys
- Structured logging, correlation IDs, health checks, and deployment runbooks
- ADRs for material architecture changes

The complete working agreements are in the [engineering system](docs/engineering/README.md).

## Current Limitations

- The Django bootstrap selects development or production settings from `DEBUG`; use `DJANGO_SETTINGS_MODULE=configs.settings.dev` explicitly during local development until that bootstrap is simplified.
- The current backend `.env` reports a dotenv parse warning and should be normalized to plain `KEY=value` lines.
- Production PostgreSQL must be running and correctly configured before starting with production settings.
- The dev launcher scripts need process ownership, durable background execution, and actionable failure reporting before they should be relied on by a team.
- Automated test, lint, type-check, and CI workflows still need to be established and enforced.

## Contributing

1. Read the relevant backend or frontend architecture guide.
2. Keep changes within one bounded context where possible.
3. Add or update tests and API/event contracts with behavior changes.
4. Record a short ADR for cross-module or infrastructure decisions.
5. Do not introduce a service split without measurable extraction criteria.

## License

No license has been declared yet. Add one before accepting external contributions or distributing the project.
