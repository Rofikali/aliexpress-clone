# Backend Module Design

## Standard Module Shape

```text
apps/<module>/
  domain/          # Python business rules, entities, value objects, domain events
  application/     # Use cases, DTOs, ports, transaction boundaries
  adapters/
    inbound/rest/  # DRF serializers, views, URLs
    outbound/      # Django ORM repositories, provider clients, cache, messaging
  models/          # Django persistence models owned by this module
  tasks/           # Background handlers
  tests/
    unit/
    integration/
    contract/
```

Existing files may remain while being migrated. New logic follows this shape.

## Dependency Direction

```text
REST/Admin/Task -> application -> domain
                    |              ^
                    v              |
             adapters/ports --------
```

- `domain` imports only Python standard library and small shared value objects; no Django, DRF, ORM, HTTP, or provider SDKs.
- `application` coordinates a single use case and depends on port interfaces, not concrete repositories or providers.
- `adapters` implement ports and are the only layer allowed to import Django, DRF, storage, queues, or third-party APIs.
- Views are thin: authenticate, deserialize, call one use case, serialize the result.

## SOLID Applied Practically

- **Single responsibility:** a `PlaceOrder` use case is separate from payment capture and email delivery.
- **Open/closed:** introduce a payment-provider port; add providers as adapters instead of branching throughout checkout.
- **Liskov substitution:** every adapter obeys its port's return values, exceptions, idempotency, and transaction contract.
- **Interface segregation:** use small ports such as `InventoryReservationPort`, not a global `MarketplaceService`.
- **Dependency inversion:** inject ports into use cases from a composition root; never import another module's model directly.

## Patterns to Use Deliberately

| Problem | Pattern |
| --- | --- |
| One user action | command/use-case handler |
| Provider or ORM dependency | port and adapter |
| Complex validity/state rules | aggregate plus value objects |
| Committed side effect | transactional outbox |
| Multi-module workflow | saga/process manager with compensations |
| Optimized listing/search | read projection/CQRS-lite |
| Provider selection | strategy |

Avoid factories, repositories, CQRS, or events when a simple function is clearer. Patterns serve failure modes, not résumé keywords.

## Transaction and Error Rules

- A use case owns `transaction.atomic()` and writes its outbox records in that transaction.
- Use `select_for_update()` or optimistic version checks for stock and state transitions.
- Return domain/application errors; map them to stable DRF error codes at the HTTP adapter.
- Require an idempotency key for payment, checkout, and webhook commands.
- Never call payment, email, or queue providers while a database transaction is open.
