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

## 🗂️ Folder Structure aliexressclone
project_root/
│
├── core/                               # Shared, reusable, framework-level logic
│   ├── authentication/                 # JWT utils & custom DRF auth backends
│   │   ├── __init__.py
│   │   ├── jwt_utils.py
│   │   └── backends.py
│   │
│   ├── router/                         # Custom routers (auto-generate plural/kebab-case)
│   │   └── routers.py
│   │
│   ├── pagination/                     # DRF pagination utilities
│   │   ├── __init__.py
│   │   ├── base_cursor.py
│   │   ├── offset_pagination.py
│   │   └── infinite_scroll.py
│   │
│   ├── permissions/                    # Centralized DRF permissions
│   │   └── permissions.py
│   │
│   ├── responses/                      # Standardized API responses
│   │   ├── __init__.py
│   │   └── response_factory.py         # success() / error() factory
│   │
│   ├── mixins/                         # DRF view/serializer mixins
│   │   ├── __init__.py
│   │   └── soft_delete_mixin.py
│   │
│   ├── caching/                        # Caching logic
│   │   ├── __init__.py
│   │   ├── base_cache.py
│   │   ├── cache_factory.py
│   │   └── invalidation.py
│   │
│   ├── middleware/                     # Custom middlewares
│   │   └── request_timer.py
│   │
│   ├── throttling/                     # API throttling utilities
│   │   ├── __init__.py
│   │   ├── base_throttle.py
│   │   ├── backend.py
│   │   ├── middleware.py
│   │   ├── utils.py
│   │   └── exceptions.py
│   │
│   ├── utils/                          # General-purpose helpers
│   │   ├── encoders.py
│   │   └── money.py
│   │
│   └── __init__.py
│
├── apps/                               # Domain-driven Django apps
│   ├── accounts/                       # Users & authentication
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models/
│   │   ├── serializers/
│   │   │   ├── __init__.py
│   │   │   ├── auth_serializer.py       # register, login, refresh, logout
│   │   │   ├── profile_serializer.py    # profile, KYC
│   │   │   ├── password_serializer.py   # reset request, confirm
│   │   │   └── device_serializer.py     # device management
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── auth_views.py           # register, login, refresh, logout
│   │   │   ├── profile_views.py        # profile, KYC
│   │   │   ├── password_views.py       # reset request, confirm
│   │   │   └── device_views.py         # device management
│   │   ├── urls.py
│   │   └── tests/
│   │
│   ├── products/                       # Product catalog, inventory, variants, images
│   ├── posts/                          # Reviews & social posts
│   ├── orders/                         # Orders & checkout workflow
│   ├── payments/                       # Payment gateway integrations
│   ├── notifications/                  # Push, email, real-time notifications
│   └── __init__.py
│
├── services/                           # External service integrations
│   ├── celery_worker/                  # Celery async workers
│   ├── elasticsearch/                  # Elasticsearch clients/config
│   ├── redis/                          # Redis cache / pub-sub
│   └── email_service/                  # Email sending logic
│
├── configs/                            # Project configuration & entrypoints
│   ├── settings/                       # Environment-based Django settings
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── prod.py
│   │   └── test.py
│   │
│   ├── __init__.py
│   ├── urls.py                         # Root URL router
│   ├── wsgi.py                         # WSGI entrypoint
│   └── asgi.py                         # ASGI entrypoint (WebSocket, async)
│
├── static/                             # Static assets (served via CDN in prod)
├── media/                              # User-uploaded files (S3 in prod)
│
├── requirements/                       # Dependencies per environment
│   ├── base.txt
│   ├── dev.txt
│   ├── prod.txt
│   └── test.txt
│
├── tests/                              # Global tests across apps
│   ├── unit/
│   ├── integration/
│   └── performance/
│
├── .env                                # Local environment variables
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── README.md
