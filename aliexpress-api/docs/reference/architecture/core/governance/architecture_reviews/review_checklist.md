# Architecture Review Checklist

## General
- [ ] Does this change introduce a new domain or bounded context?
- [ ] Does it affect more than one team?
- [ ] Is backward compatibility preserved?

## DDD
- [ ] Are aggregates clearly defined?
- [ ] Are invariants enforced inside the domain?
- [ ] No anemic domain models introduced?

## Clean Architecture
- [ ] Dependencies point inward?
- [ ] Application layer has no framework dependency?
- [ ] Domain layer is pure?

## Hexagonal
- [ ] External systems accessed only via ports?
- [ ] Adapters isolated from core logic?

## Event-Driven / Saga
- [ ] Events are immutable?
- [ ] Compensation paths defined?
- [ ] Idempotency considered?

## Data
- [ ] No cross-domain DB access?
- [ ] No shared tables?

## Observability
- [ ] Correlation IDs propagated?
- [ ] Saga steps observable?
- [ ] Metrics defined?

## Governance
- [ ] ADR created or updated?
- [ ] Owning team identified?
