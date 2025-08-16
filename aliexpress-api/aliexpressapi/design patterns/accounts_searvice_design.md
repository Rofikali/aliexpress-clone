# 🛡️ Accounts / Identity Service – LLD + HLD

---

## 🧩 LLD – Database Schema

### 1. Users Table

| Column         | Type         | Constraints / Notes                       |
| -------------- | ------------ | ----------------------------------------- |
| id             | UUID / BIGINT | PK, Sharding key                           |
| username       | VARCHAR(100) | Unique, Indexed                            |
| email          | VARCHAR(255) | Unique, Indexed                            |
| phone_number   | VARCHAR(20)  | Optional, Indexed                           |
| password_hash  | VARCHAR(255) | NOT NULL                                   |
| role           | ENUM         | ['buyer','seller','admin']                 |
| kyc_status     | ENUM         | ['pending','approved','rejected']          |
| is_active      | BOOLEAN      | Default TRUE                               |
| last_login     | TIMESTAMP    | Indexed                                    |
| created_at     | TIMESTAMP    | Indexed                                    |
| updated_at     | TIMESTAMP    |                                            |

### 2. User Devices Table

| Column       | Type          | Constraints / Notes                    |
| ------------ | ------------- | ------------------------------------ |
| id           | BIGINT / UUID | PK                                     |
| user_id      | FK → users    | Indexed                                |
| device_type  | ENUM          | ['mobile','desktop','tablet']         |
| device_token | VARCHAR(255)  | Optional, for push notifications      |
| last_active  | TIMESTAMP     | Indexed                                |
| created_at   | TIMESTAMP     |                                        |
| updated_at   | TIMESTAMP     |                                        |

### 3. Password Resets Table

| Column     | Type          | Constraints / Notes                |
| ---------- | ------------- | --------------------------------- |
| id         | BIGINT / UUID | PK                                |
| user_id    | FK → users    | Indexed                            |
| token      | VARCHAR(255)  | Unique, for verification            |
| expires_at | TIMESTAMP     | Expiration timestamp               |
| used       | BOOLEAN       | Default FALSE                      |
| created_at | TIMESTAMP     |                                     |

### Notes:

- `kyc_status` tracks seller verification.
- Devices table helps with multi-device 2FA and push notifications.
- Password reset tokens are time-limited and one-time use.

---

## 🏗 HLD – Service Design

### Microservices

- **Identity Service** – handles user registration, login, authentication, and role management.
- **KYC Service** – verifies sellers via document upload, approval workflow.
- **2FA & Device Management** – supports multi-device login, OTP/Authenticator apps.
- **Password Reset Service** – issues, validates, and tracks reset tokens.

### Authentication & Security

- JWT / OAuth2 / SSO support
- Optional Social logins: Google, Facebook, Apple
- 2FA via SMS, Email, or Authenticator apps
- Password hashing: bcrypt / Argon2
- Rate limiting and brute-force detection

### Caching Layer

- Redis cache for sessions / active tokens
- Throttle login attempts per IP/user

### Event-Driven Architecture

- User registration → send welcome email / SMS
- KYC approved → notify seller & update role
- Password reset → notification triggered asynchronously
- User deactivated → propagate to other services

### API Endpoints

| Method | Endpoint                  | Description                          |
| ------ | ------------------------- | ------------------------------------ |
| POST   | /register                 | Create a new user                     |
| POST   | /login                    | Authenticate user                     |
| POST   | /logout                   | Invalidate token / session            |
| POST   | /password/reset-request   | Request password reset token          |
| POST   | /password/reset           | Reset password using token            |
| GET    | /profile/{user_id}        | Fetch user profile                    |
| PATCH  | /profile/{user_id}        | Update user profile                   |
| POST   | /kyc/submit               | Upload KYC documents                  |
| GET    | /kyc/status/{user_id}     | Fetch KYC verification status         |

### Scalability

- Partition users by `user_id` for horizontal scaling
- Read replicas for profile and authentication queries
- Redis clusters for token/session storage
- Background workers for KYC processing and email/SMS sending

### Security Considerations

- Only authenticated services can call sensitive APIs
- All sensitive data encrypted at rest
- Audit logging for login attempts, KYC approvals, and password resets

---

## 📊 ERD – Accounts / Identity Module

```mermaid
erDiagram
    accounts_user ||--o{ user_device : owns
    accounts_user ||--o{ password_reset : requests

Architecture – HLD

graph TB
    APIGW[API Gateway]
    Web[Web SPA]
    App[Mobile Apps]

    IdentityService[Identity / User Service]
    KYCService[KYC Verification Service]
    PasswordResetService[Password Reset Service]
    Redis[Redis Cache]
    Postgres[Postgres DB]
    Kafka[Event Bus / Kafka]

    Web --> APIGW
    App --> APIGW

    APIGW --> IdentityService
    IdentityService --> Redis
    IdentityService --> Postgres
    IdentityService --> Kafka
    IdentityService --> KYCService
    IdentityService --> PasswordResetService
