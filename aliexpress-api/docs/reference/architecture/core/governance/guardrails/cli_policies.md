# Architecture Guardrails (CI)

## Dependency Rules
- Domains MUST NOT import other domains
- Domain layer MUST NOT import application, adapters, or infrastructure
- Shared kernel MUST NOT contain business logic

## Folder Boundaries
- Each domain folder has exactly one owning team
- No global "utils" folder allowed
- No shared models across domains

## Event Rules
- Events are append-only
- No breaking changes without versioning
- Consumers must tolerate unknown fields

## Enforcement
Violations cause:
- CI failure
- Architecture review required
- ADR justification mandatory

## Exceptions
Exceptions require:
- Architecture Council approval
- Time-bound ADR
- Explicit rollback plan
