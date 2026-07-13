# Security Baseline

## Scope

Security is a product requirement. Apply this baseline to backend, frontend, CI, infrastructure, dependencies, and operational access.

## Secrets and Configuration

- Keep secrets out of source control, logs, API responses, screenshots, and test fixtures.
- Commit sanitized `.env.example` files, never real `.env` files.
- Validate environment configuration on startup; fail closed for missing production secrets.
- Rotate credentials after exposure and document ownership/rotation frequency.
- Use separate development, staging, and production credentials and databases.

## Identity and Access

- Enforce authorization in backend use cases or DRF permissions; Nuxt route middleware is not security.
- Apply least privilege to users, staff roles, Django admin, database accounts, CI tokens, and cloud identities.
- Use secure password hashing, rate limits, lockout/abuse controls, and MFA for privileged accounts.
- Revoke/rotate refresh tokens on logout, credential reset, and suspected compromise.
- Log security-relevant events without logging tokens, passwords, payment data, or unnecessary personal data.

## Web and API Safety

- Use HTTPS in non-local environments; set secure cookie flags only when HTTPS is enabled.
- Configure CORS and CSRF origins explicitly per environment; never use permissive origins with credentials.
- Validate and normalize input at the API boundary. Enforce object-level authorization on every resource lookup.
- Set request-size, upload-type, pagination, rate-limit, and timeout limits.
- Return stable public error codes; do not disclose stack traces, secrets, or internal topology.
- Verify webhook signatures, timestamps, replay protection, and idempotency before changing state.

## Data and Payments

- Store the minimum personal data needed, classify it, and define retention/deletion behavior.
- Encrypt data in transit and use managed encryption at rest where available.
- Never store raw payment card data. Use provider tokens and follow the payment provider's PCI guidance.
- Protect export, admin, search, and analytics endpoints from bulk data exfiltration.

## Supply Chain and CI

- Pin dependencies with lockfiles and review updates.
- Run dependency, secret, static-analysis, and container/image scans in CI once the tooling is installed.
- Restrict CI secrets to protected branches/environments and use short-lived credentials where possible.
- Require review for authentication, permissions, payments, database migrations, and deployment changes.

## Release Security Checklist

- No development secrets, debug mode, permissive hosts, or unsafe CORS configuration in production.
- Production database backup/restore and access controls verified.
- Known critical vulnerabilities have a remediation or approved, time-bound exception.
- Security contact, incident path, and credential-rotation procedure documented.
