# Architecture Documentation

This directory is the architectural source of truth for the AliExpress clone. The target is a **modular monolith**: one deployable Django API and one Nuxt application, with business modules that can be extracted later only when there is a demonstrated operational need.

## Start Here

1. Read [the target architecture](architecture-roadmap.md).
2. Read the backend rules in `../aliexpress-api/docs/`.
3. Read the frontend rules in `../aliexpress-nuxt4/docs/`.
4. Record material decisions as ADRs before changing cross-module boundaries.

## Non-Negotiable Decisions

- One repository and one database are acceptable now; services are not a maturity goal.
- Each business capability owns its models, use cases, API routes, events, and tests.
- Modules communicate through application ports and versioned contracts, not imports into another module's persistence layer.
- External effects are asynchronous and reliable through an outbox; never publish an event before its database transaction commits.
- The Nuxt app consumes published HTTP contracts only. It does not mirror Django internals.

## Documentation Rule

New architecture documents belong here or in the relevant application `docs/` directory. Existing notes in `core/`, `md_files/`, and `Dir Rules & Structers/` are reference material, not automatically binding when they conflict with this documentation.

## Existing Documentation Maps

- [Backend source notes](../aliexpress-api/docs/source-notes.md)
- [Frontend source notes](../aliexpress-nuxt4/docs/source-notes.md)
