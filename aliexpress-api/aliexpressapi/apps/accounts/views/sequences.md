First time user → Register → receive tokens → start using app

Returning user → Login → receive tokens

Using API → send access token on each request

Access token expires → call Refresh with refresh token → get new access token

User logs out → call Logout with refresh token → blacklisted

 [ Client / Postman / Frontend ]
                │
                │   1. Register (username, email, phone, pass, role)
                ▼
       ┌──────────────────────────────┐
       │   /api/v1/register/          │
       │   - Creates user & profile   │
       │   - Issues JWT tokens        │
       └──────────────────────────────┘
                │
                │   Response:
                │   {
                │     profile: {...},
                │     tokens: {
                │        access, refresh,
                │        access_expires_at,
                │        sub = user_id (UUID)
                │     }
                │   }
                ▼
        ┌──────────────────────┐
        │  Client Stores Tokens│
        └──────────────────────┘
                │
                │  2. Use Access Token
                │     → Authorization: Bearer <access>
                ▼
       ┌──────────────────────────────┐
       │  Any Protected API Endpoint  │
       └──────────────────────────────┘
                │
                │  3. Access Token Expired?
                │
         ┌─────────────Yes──────────────┐
         ▼                              │
┌─────────────────────────┐             │
│  /api/v1/token/refresh/ │             │
│   - Send refresh token  │             │
│   - Get new access (+   │             │
│     rotated refresh if  │             │
│     enabled)            │             │
└─────────────────────────┘             │
         │                              │
         ▼                              │
  New Access Token 🔑                   │
         │                              │
         └──────────→ Continue Using API│

# Accounts Auth — Visual Summary

A compact visual overview of what we implemented together for **Accounts / Auth** in your AliExpress-clone DRF project. This is intentionally small, actionable, and ready to share with teammates.

---

## Key components

* **User (Custom)** — `apps.accounts.models.user.User` (UUID PK, `is_email_verified`, `kyc_status`)
* **Devices** — per-device records for session management (`apps.accounts.models.device.UserDevice`)
* **Tokens** — access + refresh JWT helpers in `core/authentication/jwt_utils.py` and persistent `RefreshToken` model
* **Email verification** — `EmailVerification` model + endpoints to request/confirm OTP
* **Password reset** — `PasswordResetToken` model + request/confirm endpoints
* **KYC (stubbed)** — `KYCApplication` + `KYCDocument` models and endpoints placeholder for submit/status/webhook

---

## Flow (compact)

```mermaid
flowchart LR
  A[Register (POST /api/v1/register/)] --> B[Create User (is_email_verified=false)]
  B --> C[Create EmailVerification OTP]
  C --> D[Send OTP via email]
  D --> E[User confirms OTP (POST /api/v1/email-verification-confirm/)]
  E --> F[Mark user.is_email_verified = true]

  subgraph Auth
    G[Login (POST /api/v1/login/)] -->|requires verified| H[create_token_pair_for_user]
    H --> I[Return access + refresh tokens]
    I --> J[Refresh (POST /api/v1/refresh/)]
    I --> K[Logout (POST /api/v1/logout/) -> blacklist refresh]
  end

  subgraph Account Recovery
    L[Password Reset Request] --> M[Create PasswordResetToken]
    M --> N[Send reset link]
    N --> O[Password Reset Confirm]
  end

  subgraph KYC
    P[KYC Submit (POST /api/v1/kyc/submit/)] --> Q[Create KYCApplication + KYCDocument]
    Q --> R[Provider webhook updates status]
  end
```

---

## Endpoints (short list)

* `POST /api/v1/register/` — register user (returns profile + tokens; sends OTP)
* `POST /api/v1/login/` — login (blocked until `is_email_verified`)
* `POST /api/v1/refresh/` — rotate/refresh tokens
* `POST /api/v1/logout/` — blacklist refresh token
* `POST /api/v1/email-verification-request/` — resend OTP (auth required)
* `POST /api/v1/email-verification-confirm/` — confirm OTP (auth required)
* `POST /api/v1/password-reset/request/` — request password reset
* `POST /api/v1/password-reset/confirm/` — confirm and set new password
* `POST /api/v1/kyc/submit/` — submit KYC documents
* `GET  /api/v1/kyc/status/` — check KYC status

---

## Notes / dev conveniences

* **Console email backend** used during dev: set `EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"` — OTPs print to terminal.
* OTPs are 6-digit, expire in \~10 minutes by default.
* Login is strict: users must verify email before logging in (configurable).
* Refresh tokens are prepared for rotation/blacklist; device-aware rotation can be added via `UserDevice` + Redis keys.

---

## Next small suggestions

1. Add `is_email_verified` to `ProfileSerializer` (done).
2. Add a `/resend` endpoint with throttle scope.
3. Add a small admin KYC review UI (Django admin customization).

---

If you want a PNG/SVG export, or a prettier diagram (graphical), tell me and I’ll produce a downloadable image or a compact SVG you can embed in docs.
