# Frontend Architecture Guide

The Nuxt application is a domain-oriented client of the DRF API. It owns presentation, local interaction state, and client-side orchestration; it does not duplicate backend authorization or business invariants.

## Read Next

- [Frontend module and data rules](module-design.md)
- [API contract and reliability rules](api-integration.md)
- [Frontend runtime, release, and security operations](operations.md)
- [Existing frontend notes and their status](source-notes.md)

## Current Integration

`NUXT_PUBLIC_BASE_API` configures the API base through Nuxt runtime configuration. See `.env.example` for the local value and `operations.md` for deployment rules.
