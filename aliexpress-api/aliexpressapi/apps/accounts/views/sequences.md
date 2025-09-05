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
