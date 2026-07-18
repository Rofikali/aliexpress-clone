# Backend Architecture Guide

The DRF backend is a modular monolith. Django is the delivery and persistence framework; it is not the location for all business logic.

## Current Entry Points

- API routes are mounted under `/api/v1/` in `configs/urls.py`.
- OpenAPI schema is served at `/api/schema/`.
- Existing Django apps under `apps/` are the starting point for bounded contexts, not a requirement to rewrite everything at once.

## Read Next

- [Module design and dependency rules](module-design.md)
- [API, events, and extraction strategy](contracts-and-evolution.md)
- [Production configuration and runtime operations](operations.md)
- [System observability standards](../../docs/engineering/observability.md)
- [Existing backend notes and their status](source-notes.md)

## Working Rule

For a change inside an existing app, first add the use case and tests using the structure below. Migrate legacy view/model logic gradually; do not perform a repository-wide rewrite.
