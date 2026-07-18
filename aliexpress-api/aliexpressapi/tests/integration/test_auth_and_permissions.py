from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from decimal import Decimal
from uuid import uuid4

import pytest
from rest_framework.test import APIClient

from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
from apps.products.models.brand import Brand
from apps.products.models.category import Category
from apps.products.models.product import Product
from apps.products.models.product_variant import ProductVariant
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.outbox.models import OutboxEvent


User = get_user_model()


def create_checkout_cart(user, *, label, quantity=2, stock=10, variant_price="100.00"):
    seller = User.objects.create_user(
        email=f"seller-{label}@example.com",
        username=f"seller-{label}",
        password="StrongPassword123!",
        role="seller",
    )
    category = Category.objects.create(name=f"Phones {label}", slug=f"phones-{label}")
    brand = Brand.objects.create(name=f"Example {label}", slug=f"example-{label}")
    product = Product.objects.create(
        title=f"Example Phone {label}",
        slug=f"example-phone-{label}",
        description="A test product",
        sku=f"EXAMPLE-PHONE-{label}",
        price=variant_price,
        stock=stock,
        seller=seller,
        category=category,
        brand=brand,
    )
    variant = ProductVariant.objects.create(
        product=product,
        sku=f"EXAMPLE-PHONE-{label}-BLACK",
        price=variant_price,
        stock=stock,
    )
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(
        cart=cart,
        product_variant=variant,
        quantity=quantity,
        price=variant_price,
    )
    return cart, variant


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


@pytest.mark.django_db
def test_authenticated_user_can_add_and_increment_own_cart_item():
    buyer = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    seller = User.objects.create_user(
        email="seller@example.com",
        username="seller",
        password="StrongPassword123!",
        role="seller",
    )
    category = Category.objects.create(name="Phones", slug="phones")
    brand = Brand.objects.create(name="Example", slug="example")
    product = Product.objects.create(
        title="Example Phone",
        slug="example-phone",
        description="A test product",
        sku="EXAMPLE-PHONE",
        price="100.00",
        stock=10,
        seller=seller,
        category=category,
        brand=brand,
    )
    variant = ProductVariant.objects.create(
        product=product,
        sku="EXAMPLE-PHONE-BLACK",
        price="100.00",
        stock=10,
    )
    api_client = APIClient()
    api_client.force_authenticate(user=buyer)

    first_add = api_client.post(
        reverse("cart-add-item"),
        {"product_variant_id": str(variant.id), "quantity": 2},
        format="json",
    )
    second_add = api_client.post(
        reverse("cart-add-item"),
        {"product_variant_id": str(variant.id), "quantity": 3},
        format="json",
    )

    assert first_add.status_code == 201
    assert second_add.status_code == 201
    cart = Cart.objects.get(user=buyer, is_active=True)
    item = CartItem.objects.get(cart=cart, product_variant=variant)
    assert item.quantity == 5
    assert Cart.objects.filter(user=seller, is_active=True).count() == 0


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("payload", "expected_field"),
    [
        (
            {"product_variant_id": "not-a-uuid", "quantity": 0},
            "product_variant_id",
        ),
        (
            {"product_variant_id": "not-a-uuid", "quantity": "2"},
            "quantity",
        ),
        (
            {"product_variant_id": "not-a-uuid", "unexpected": True},
            "unexpected",
        ),
    ],
)
def test_cart_rejects_invalid_pydantic_commands(payload, expected_field):
    user = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    api_client = APIClient()
    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse("cart-add-item"),
        payload,
        format="json",
    )

    assert response.status_code == 400
    response_body = response.json()
    assert response_body["message"] == "Request validation failed"
    assert response_body["errors"]
    assert all(error["code"] == "VALIDATION_ERROR" for error in response_body["errors"])
    assert any(
        error["message"].startswith(f"{expected_field}:")
        for error in response_body["errors"]
    )


@pytest.mark.django_db
def test_checkout_reserves_inventory_and_snapshots_current_variant_price():
    buyer = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    cart, variant = create_checkout_cart(buyer, label="checkout", quantity=2)
    variant.price = Decimal("125.00")
    variant.save(update_fields=["price"])
    api_client = APIClient()
    api_client.force_authenticate(user=buyer)

    response = api_client.post(
        reverse("checkout-list"),
        {},
        format="json",
        HTTP_IDEMPOTENCY_KEY=str(uuid4()),
    )

    assert response.status_code == 201
    order = Order.objects.get(id=response.json()["data"]["order_id"])
    order_item = OrderItem.objects.get(order=order)
    variant.refresh_from_db()
    cart.refresh_from_db()
    assert order.total_price == Decimal("250.00")
    assert order_item.unit_price == Decimal("125.00")
    assert variant.stock == 8
    assert not cart.is_active
    assert cart.is_locked
    event = OutboxEvent.objects.get(
        aggregate_type="order",
        aggregate_id=order.id,
        event_type="order.created",
    )
    assert event.status == OutboxEvent.Status.PENDING
    assert event.payload == {
        "order_id": str(order.id),
        "user_id": str(buyer.id),
        "total_price": "250.00",
    }


@pytest.mark.django_db
def test_checkout_replay_returns_original_order_without_second_stock_reservation():
    buyer = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    _, variant = create_checkout_cart(buyer, label="replay", quantity=2)
    key = uuid4()
    api_client = APIClient()
    api_client.force_authenticate(user=buyer)

    first_response = api_client.post(
        reverse("checkout-list"),
        {},
        format="json",
        HTTP_IDEMPOTENCY_KEY=str(key),
    )
    replay_response = api_client.post(
        reverse("checkout-list"),
        {},
        format="json",
        HTTP_IDEMPOTENCY_KEY=str(key),
    )

    assert first_response.status_code == 201
    assert replay_response.status_code == 200
    assert replay_response.json()["data"] == first_response.json()["data"]
    assert Order.objects.filter(user=buyer, idempotency_key=key).count() == 1
    assert OutboxEvent.objects.filter(event_type="order.created").count() == 1
    variant.refresh_from_db()
    assert variant.stock == 8


@pytest.mark.django_db
def test_checkout_rejects_insufficient_inventory_without_mutating_cart_or_stock():
    buyer = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    cart, variant = create_checkout_cart(
        buyer,
        label="stock-conflict",
        quantity=2,
        stock=1,
    )
    api_client = APIClient()
    api_client.force_authenticate(user=buyer)

    response = api_client.post(
        reverse("checkout-list"),
        {},
        format="json",
        HTTP_IDEMPOTENCY_KEY=str(uuid4()),
    )

    assert response.status_code == 409
    assert response.json()["errors"][0]["code"] == "CHECKOUT_CONFLICT"
    assert Order.objects.count() == 0
    assert OutboxEvent.objects.count() == 0
    variant.refresh_from_db()
    cart.refresh_from_db()
    assert variant.stock == 1
    assert cart.is_active
    assert not cart.is_locked


@pytest.mark.django_db
def test_checkout_requires_a_valid_idempotency_key():
    buyer = User.objects.create_user(
        email="buyer@example.com",
        username="buyer",
        password="StrongPassword123!",
    )
    api_client = APIClient()
    api_client.force_authenticate(user=buyer)

    response = api_client.post(reverse("checkout-list"), {}, format="json")

    assert response.status_code == 400
    assert response.json()["message"] == "Request validation failed"
    assert response.json()["errors"][0]["code"] == "VALIDATION_ERROR"


@pytest.mark.django_db
def test_checkout_idempotency_key_is_scoped_to_the_authenticated_buyer():
    first_buyer = User.objects.create_user(
        email="first-buyer@example.com",
        username="first-buyer",
        password="StrongPassword123!",
    )
    second_buyer = User.objects.create_user(
        email="second-buyer@example.com",
        username="second-buyer",
        password="StrongPassword123!",
    )
    create_checkout_cart(first_buyer, label="first-buyer")
    create_checkout_cart(second_buyer, label="second-buyer")
    key = uuid4()
    first_client = APIClient()
    first_client.force_authenticate(user=first_buyer)
    second_client = APIClient()
    second_client.force_authenticate(user=second_buyer)

    first_response = first_client.post(
        reverse("checkout-list"),
        {},
        format="json",
        HTTP_IDEMPOTENCY_KEY=str(key),
    )
    second_response = second_client.post(
        reverse("checkout-list"),
        {},
        format="json",
        HTTP_IDEMPOTENCY_KEY=str(key),
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert Order.objects.filter(idempotency_key=key).count() == 2
