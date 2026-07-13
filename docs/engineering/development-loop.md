# Engineering Delivery Loop

## Purpose

This is the default loop for a feature, bug fix, refactor, or operational change. Its job is to reduce rework and make risks visible before users find them.

```text
Understand -> Design -> Slice -> Implement -> Verify -> Review -> Release -> Observe -> Learn
```

## 1. Understand

Write the user or operational outcome, affected bounded context, non-goals, acceptance criteria, and failure cases. Identify whether the change touches money, inventory, identity, personal data, or a public API; these require elevated review.

## 2. Design

Document the smallest design that meets the outcome:

- module ownership and allowed dependencies
- API/event/data-contract changes
- authorization and validation rules
- transaction boundary, idempotency behavior, and failure recovery
- telemetry, rollout, rollback, and migration plan

Use an ADR for a durable cross-module, security, data, or infrastructure decision. Do not write an ADR for an ordinary local implementation detail.

## 3. Slice

Deliver vertical slices. A slice has a usable path from Nuxt UI through the DRF contract to persistence, with tests and observability. Avoid merging a large folder restructure before behavior is protected by tests.

## 4. Implement

Keep the dependency direction from the architecture guide. Make HTTP adapters thin, keep framework-independent business rules where complexity warrants it, and avoid direct access to another module's models.

## 5. Verify

Run the smallest relevant checks first, then the required quality gates. Test unhappy paths, authorization, duplicate requests, concurrent updates, and provider failure for critical flows—not only the successful demo path.

## 6. Review

Reviewers check behavior, contracts, data safety, security, tests, observability, and rollback. Review is not a spelling check or a rubber stamp.

## 7. Release

Use backward-compatible changes, feature flags, and expand/contract database migrations. Define a measurable success signal and a rollback trigger before enabling a risky change.

## 8. Observe

After release, inspect errors, latency, business outcomes, and logs using a correlation ID. Compare real behavior against the acceptance criteria and SLOs.

## 9. Learn

For incidents, near-misses, or significant surprises, record what happened, why detection or recovery was slow, and one or more owned follow-up actions. Blameless learning improves the system; blame hides risk.

## Definition of Ready

- Outcome and acceptance criteria are clear.
- Owner module and API/event contract impact are known.
- Security/data classification and failure modes are considered.
- The slice is small enough to verify and review.

## Definition of Done

- Behavior, automated tests, and documentation are updated.
- Required quality gates pass.
- Observability and rollback are present for customer-impacting changes.
- No known security or data-integrity risk is silently deferred.
