# Frontend Architecture Guide

The Nuxt application is a domain-oriented client of the DRF API. It owns presentation, local interaction state, and client-side orchestration; it does not duplicate backend authorization or business invariants.

## Read Next

- [Frontend module and data rules](module-design.md)
- [API contract and reliability rules](api-integration.md)
- [Existing frontend notes and their status](source-notes.md)

## Current Integration

The configured API base is `/api/v1` via Nuxt runtime configuration. Replace the hard-coded development value with environment-driven runtime configuration before production deployment.
