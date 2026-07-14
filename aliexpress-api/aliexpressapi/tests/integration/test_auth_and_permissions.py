from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

import pytest


User = get_user_model()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("url_name", "method"),
    [
        ("cart-list", "get"),
        ("order-list", "get"),
        ("checkout-list", "post"),
    ],
)
def test_sensitive_marketplace_routes_require_authentication(client, url_name, method):
    response = getattr(client, method)(reverse(url_name), data={}, content_type="application/json")

    assert response.status_code == 401


@pytest.mark.django_db
def test_catalog_is_public_but_inventory_is_protected(client):
    assert client.get(reverse("products-list")).status_code == 200
    assert client.get(reverse("inventory-list")).status_code == 401


@pytest.mark.django_db
@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
def test_registration_then_login_requires_verified_email(client):
    registration = client.post(
        reverse("register-list"),
        data={
            "username": "buyer-one",
            "email": "buyer@example.com",
            "password": "StrongPassword123!",
            "role": "buyer",
        },
        content_type="application/json",
    )

    assert registration.status_code == 201
    assert registration.json()["data"]["tokens"]["access"]

    rejected_login = client.post(
        reverse("login-list"),
        data={"email": "buyer@example.com", "password": "StrongPassword123!"},
        content_type="application/json",
    )
    assert rejected_login.status_code == 403

    user = User.objects.get(email="buyer@example.com")
    user.is_email_verified = True
    user.save(update_fields=["is_email_verified"])

    accepted_login = client.post(
        reverse("login-list"),
        data={"email": "buyer@example.com", "password": "StrongPassword123!"},
        content_type="application/json",
    )

    assert accepted_login.status_code == 200
    assert accepted_login.json()["data"]["access"]
