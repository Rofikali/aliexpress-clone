from django.db import IntegrityError, transaction

from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
from apps.checkout.errors import CheckoutConflictError
from apps.order.models.order import Order
from apps.order.models.order_item import OrderItem
from apps.products.models.product_variant import ProductVariant


class CheckoutRepository:
    def get_order_by_idempotency_key(self, *, user, idempotency_key):
        return Order.objects.filter(
            user=user,
            idempotency_key=idempotency_key,
        ).first()

    def get_active_cart_for_user(self, *, user):
        return (
            Cart.objects.select_for_update()
            .filter(user=user, is_active=True, is_locked=False)
            .order_by("created_at")
            .first()
        )

    def get_locked_cart_items(self, *, cart):
        return list(
            CartItem.objects.select_for_update()
            .filter(cart=cart)
            .order_by("id")
        )

    def get_locked_variants(self, *, cart_items):
        variant_ids = [item.product_variant_id for item in cart_items]
        variants = ProductVariant.objects.select_for_update().filter(id__in=variant_ids)
        return {variant.id: variant for variant in variants}

    def assert_variants_are_checkoutable(self, *, cart_items, variants):
        for item in cart_items:
            variant = variants.get(item.product_variant_id)
            if variant is None or not variant.is_active:
                raise CheckoutConflictError("A cart item is no longer available")
            if variant.stock < item.quantity:
                raise CheckoutConflictError("Insufficient inventory for a cart item")

    def reserve_inventory(self, *, cart_items, variants):
        for item in cart_items:
            variant = variants[item.product_variant_id]
            variant.stock -= item.quantity
            variant.save(update_fields=["stock"])

    def create_order(self, *, user, idempotency_key, cart_items, variants):
        existing = self.get_order_by_idempotency_key(
            user=user,
            idempotency_key=idempotency_key,
        )

        if existing:
            return existing, False

        order_items = []
        total_price = 0
        for item in cart_items:
            variant = variants[item.product_variant_id]
            unit_price = variant.discount_price or variant.price
            subtotal = unit_price * item.quantity
            total_price += subtotal
            order_items.append(
                OrderItem(
                    order_id=None,
                    product_variant=variant,
                    quantity=item.quantity,
                    unit_price=unit_price,
                    subtotal=subtotal,
                )
            )

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    total_price=total_price,
                    idempotency_key=idempotency_key,
                )
                for item in order_items:
                    item.order = order
                OrderItem.objects.bulk_create(order_items)
        except IntegrityError:
            return (
                Order.objects.get(user=user, idempotency_key=idempotency_key),
                False,
            )

        return order, True

    def deactivate_cart(self, cart):
        cart.is_active = False
        cart.is_locked = True
        cart.save(update_fields=["is_active", "is_locked"])
