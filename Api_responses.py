# Auth Layer 
{
  "success": true,
  "code": 201,
  "message": "User registered successfully. Verification OTP sent to email.",
  "request": {
    "id": "ac583f28-7324-49bc-a6db-c641f0e7f728",
    "timestamp": "2025-09-08T15:59:54.430092Z",
    "latency_ms": 0.04,
    "region": "Nepal-01",
    "cache": "MISS"
  },
  "meta": {},
  "errors": null,
  "data": {
    "profile": {
      "id": "1397343a-0c84-4703-83a8-a4a3599f1eff",
      "username": "1test43433",
      "email": "1tst34433@exaeremple.com",
      "phone_number": "9874563241",
      "role": "buyer",
      "kyc_status": "pending",
      "is_active": true,
      "is_email_verified": false,
      "last_login": null,
      "created_at": "2025-09-08T15:59:54.385088Z",
      "updated_at": "2025-09-08T15:59:54.385124Z"
    },
    "tokens": {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc1ODY0MzE5NCwiaWF0IjoxNzU3MzQ3MTk0LCJqdGkiOiI0Y2E4Y2RlOGFiMjc0NmE2YTZiZDQwMGNiNTZlOGMwMiIsInVzZXJfaWQiOiIxMzk3MzQzYS0wYzg0LTQ3MDMtODNhOC1hNGEzNTk5ZjFlZmYifQ.end6NdjD7049uC3-O2IMA9Udcf3_1RUXhakxJASREFY",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU3MzQ3Nzk0LCJpYXQiOjE3NTczNDcxOTQsImp0aSI6IjU4MjAyMjVlYzUyMjRiMmJiMTBhYmQ1ZjQyNDI4YjFmIiwidXNlcl9pZCI6IjEzOTczNDNhLTBjODQtNDcwMy04M2E4LWE0YTM1OTlmMWVmZiJ9.Vl2E7qp-1tmK7DVa3pnLfymTE4S7fco3qocPBIYR1O0",
      "access_expires_at": 1757347794,
      "sub": "1397343a-0c84-4703-83a8-a4a3599f1eff"
    },
    "email_verification": {
      "sent": true,
      "expires_at": "2025-09-08T16:09:54.414696Z"
    }
  }
} here is the registration response, and this is my baseresponseFectory response now refector my 


# Products Layers
{
  "success": true,
  "code": 200,
  "message": "Products fetched successfully (cache)",
  "request": {
    "id": "2d5e292b-0c39-411f-a60d-ce50e6fa8f57",
    "timestamp": "2025-09-09T08:14:06.011532Z",
    "latency_ms": 0.13,
    "region": "Nepal-01",
    "cache": "HIT"
  },
  "meta": {
    "next_cursor": "cD0yMDI1LTA5LTA3KzA5JTNBMTElM0EyMS4yNTI0NTclMkIwMCUzQTAw",
    "has_next": true
  },
  "errors": null,
  "data": [
    {
      "id": "574ac81c-3eb2-4173-b048-68472c501952",
      "title": "Street range",
      "description": "Total now large learn these marriage rich its. Stand thank type state. Performance class fact speech.",
      "price": "479.33",
      "image": "http://localhost:8000/media/products/images/picture-participant.jpg",
      "images": [
        {
          "id": 2246,
          "product": "574ac81c-3eb2-4173-b048-68472c501952",
          "image": "http://localhost:8000/media/products/images/picture-participant-1.jpg"
        },
      ],
      "category": {
        "id": 1,
        "name": "Default Category",
        "description": "Auto-created default category"
      },
      "brand": {
        "id": 1,
        "name": "Default Brand",
        "description": "Auto-created default brand"
      },
      "created_at": "2025-09-07T09:11:21.497504Z",
      "updated_at": "2025-09-07T11:24:36.017785Z"
    },
   
  ]
}

# error layers
{
  "success": false,
  "code": 400,
  "message": "Validation failed",
  "request": {
    "id": "d70b2330-c7c3-4e21-a2d7-1bfde448c735",
    "timestamp": "2025-09-09T08:18:40.915393Z",
    "latency_ms": 0.13,
    "region": "Nepal-01",
    "cache": "MISS"
  },
  "meta": {},
  "errors": [
    {
      "code": "USERNAME",
      "message": "user with this username already exists."
    },
    {
      "code": "EMAIL",
      "message": "Enter a valid email address."
    },
    {
      "code": "PHONE_NUMBER",
      "message": "Enter a valid phone number (digits only, 7-15)."
    },
    {
      "code": "PASSWORD",
      "message": "Ensure this field has at least 8 characters."
    },
    {
      "code": "ROLE",
      "message": "\"b\" is not a valid choice."
    }
  ],
  "data": null
}