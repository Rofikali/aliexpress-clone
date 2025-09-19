uv init

uv add django
adee new

uv venv

uv pip install -r pyproject.toml

## migrations

python manage.py makemigrations accounts products orders carts  
python manage.py migrate
python manage.py createsuperuser

### automate above code

python setup.py

## Gerenate products with images

python manage.py generate_fake_products 50
python manage.py generate_product_images 5

# 📁 Scalable Microservices Django Project Structure

This structure is designed for extreme scale — up to **1 trillion users**, assuming distributed infrastructure, Kubernetes, PostgreSQL clusters, and high-performance caching and queuing systems.

## 🗂️ Folder Structure aliexressclone drf api

project_root/
│
├── core/                               # Shared, reusable, framework-level logic
│   ├── authentication/
│   │   ├── **init**.py
│   │   ├── jwt_utils.py                # JWT issue/verify/rotate w/ device-aware refresh
│   │   ├── backends.py                 # Custom DRF auth backends
│   │   └── device_manager.py           # Device session + refresh jti Redis helpers
│   │
│   ├── router/
│   │   └── routers.py
│   │
│   ├── pagination/
│   │   ├── **init**.py
│   │   ├── base_cursor.py
│   │   ├── offset_pagination.py
│   │   └── infinite_scroll.py
│   │
│   ├── permissions/
│   │   └── permissions.py
│   │
│   ├── responses/
│   │   ├── **init**.py
│   │   └── response_factory.py
│   │
│   ├── mixins/
│   │   ├── **init**.py
│   │   └── soft_delete_mixin.py
│   │
│   ├── caching/
│   │   ├── **init**.py
│   │   ├── base_cache.py
│   │   ├── cache_factory.py
│   │   └── invalidation.py
            kyc_middleware              # can't order, widrow, send money without kyc approved
│   │
│   ├── middleware/
│   │   ├── request_timer.py
│   │   └── request_id.py               # Inject X-Request-ID for tracing
│   │
│   ├── throttling/
│   │   ├── **init**.py
│   │   ├── base_throttle.py
│   │   ├── backend.py
│   │   ├── middleware.py
│   │   ├── utils.py
│   │   └── exceptions.py
│   │
│   ├── utils/
│   │   ├── encoders.py
│   │   ├── money.py
│   │   └── tokens.py                   # generate_one_time_token, hmac verify, etc.
│   │
│   └── **init**.py
│
├── apps/                               # Domain-driven apps
```│   ├── accounts/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models/
│   │   │   ├── **init**.py
│   │   │   ├── user.py                 # Custom User
│   │   │   ├── email_verification.py   # EmailVerification model
│   │   │   ├── device.py               # Device model
│   │   │   └── kyc.py                  # KYCApplication + KYCDocument
│   │   ├── serializers/
│   │   │   ├── **init**.py
│   │   │   ├── auth_serializer.py
│   │   │   ├── profile_serializer.py
│   │   │   ├── password_serializer.py
│   │   │   ├── device_serializer.py
│   │   │   ├── email_verification_serializer.py
│   │   │   └── kyc_serializer.py
│   │   ├── views/
│   │   │   ├── **init**.py             
│   │   │   ├── auth_views.py                       # login, register, logout, refresh
│   │   │   ├── profile_views.py                    # profile + KYC
│   │   │   ├── password_views.py                   # password reset + confirm
│   │   │   ├── device_views.py                     # user devices 
│   │   │   ├── email_verification_views.py         # (to add: email OTP / link verification)
            ├── kyc_views.py                        # User submit, check status
     │      └── kyc_admin_views.py                  # Admin approve/reject
│   │   ├── webhooks/
│   │   │   └── kyc_webhook.py          # KYC provider webhook handler # If using 3rd party KYC provider
│   │   ├── urls.py
│   │   └── tests/
│   │       ├── test_auth.py
│   │       ├── test_email_verification.py 
│   │       ├── test_kyc.py
│   │       └── test_device.py
```│   │


```
│   ├── products/
```

```
```
│   ├── posts/
│   ├── orders/
│   ├── payments/
│   ├── notifications/
│   └── **init**.py
│
├── services/
│   ├── celery_worker/                      # still not working on it for later use
│   │   ├── **init**.py
│   │   └── tasks/
│   │       ├── **init**.py
│   │       └── notifications.py        # send_verification_email, KYC notifications
│   ├── elasticsearch/
│   ├── redis/
│   └── email_service/
│
├── configs/
│   ├── settings/
│   │   ├── **init**.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── test.py
│   ├── **init**.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── static/
├── media/
│
├── requirements/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── README.md



This yields the exact endpoints you specified:

GET /api/v1/products/

GET /api/v1/products/{id}/

GET /api/v1/products/{product_pk}/variants/

GET /api/v1/products/{product_pk}/variants/{id}/

GET /api/v1/products/{product_pk}/variants/{variant_pk}/attributes/

POST /api/v1/products/{product_pk}/variants/{variant_pk}/attributes/

GET/PUT/DELETE /api/v1/products/{product_pk}/variants/{variant_pk}/attributes/{id}/