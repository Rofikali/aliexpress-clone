# # from carts/repository/cart_repository.py

# from django.db import transaction
# from django.shortcuts import get_object_or_404

# from apps.carts.models.cart import Cart
# from apps.carts.models.cartItem import CartItem
# from apps.products.models.product_variant import ProductVariant


# class CartRepository:
#     """
#     Cart domain repository
#     ----------------------
#     - Single source of truth for cart mutations
#     - Concurrency-safe
#     - Checkout-ready
#     """

#     # -------------------------
#     # Cart retrieval / creation
#     # -------------------------
#     @transaction.atomic
#     def get_or_create_cart(self, *, user=None, session_id=None) -> Cart:
#         """
#         Returns an active cart.
#         Guarantees:
#         - One active cart per user OR session
#         - Safe under concurrent requests
#         """

#         if user and user.is_authenticated:
#             cart, _ = Cart.objects.select_for_update().get_or_create(
#                 user=user,
#                 is_active=True,
#                 defaults={"session_id": None},
#             )
#             return cart

#         if session_id:
#             cart, _ = Cart.objects.select_for_update().get_or_create(
#                 session_id=session_id,
#                 is_active=True,
#                 defaults={"user": None},
#             )
#             return cart

#         raise ValueError("Cart requires authenticated user or session_id")

#     # -------------------------
#     # Variant retrieval
#     # -------------------------
#     def get_variant(self, variant_id: str) -> ProductVariant:
#         return get_object_or_404(
#             ProductVariant.objects.select_related("product"),
#             id=variant_id,
#             is_active=True,
#         )

#     # -------------------------
#     # Cart item operations
#     # -------------------------
#     @transaction.atomic
#     def add_item(
#         self, *, cart: Cart, variant: ProductVariant, quantity: int
#     ) -> CartItem:
#         """
#         Add or increment item in cart.
#         - Locks cart row
#         - Prevents negative / zero quantity
#         """

#         if quantity <= 0:
#             raise ValueError("Quantity must be greater than zero")

#         if cart.is_locked:
#             raise PermissionError("Cart is locked for checkout")

#         # Lock existing item row (if exists)
#         item, created = CartItem.objects.select_for_update().get_or_create(
#             cart=cart,
#             product_variant=variant,
#             defaults={
#                 "price": variant.price,
#                 "discount_price": variant.discount_price,
#                 "quantity": quantity,
#             },
#         )

#         if not created:
#             item.quantity += quantity
#             item.save(update_fields=["quantity"])

#         return item

#     @transaction.atomic
#     def update_item(self, *, cart: Cart, item_id: str, quantity: int) -> CartItem:
#         """
#         Update item quantity explicitly.
#         """

#         if quantity <= 0:
#             raise ValueError("Quantity must be greater than zero")

#         if cart.is_locked:
#             raise PermissionError("Cart is locked for checkout")

#         item = CartItem.objects.select_for_update().get(id=item_id, cart=cart)

#         item.quantity = quantity
#         item.save(update_fields=["quantity"])

#         return item

#     @transaction.atomic
#     def remove_item(self, *, cart: Cart, item_id: str) -> None:
#         """
#         Remove item from cart.
#         """

#         if cart.is_locked:
#             raise PermissionError("Cart is locked for checkout")

#         item = CartItem.objects.select_for_update().get(id=item_id, cart=cart)
#         item.delete()


# carts/repository/cart_repository.py

from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404

from apps.carts.models.cart import Cart
from apps.carts.models.cartItem import CartItem
from apps.carts.errors import CartConflictError
from apps.products.models.product_variant import ProductVariant


class CartRepository:
    """
    Cart domain repository
    ----------------------
    - Single source of truth for cart mutations
    - Concurrency-safe
    - Checkout-ready
    """

    @transaction.atomic
    def get_or_create_cart(self, *, user=None, session_id=None) -> Cart:
        """
        Guarantees:
        - Only ONE active cart per user OR session
        - Safe under concurrent requests
        """

        if user and user.is_authenticated:
            cart = (
                Cart.objects.select_for_update()
                .filter(user=user, is_active=True)
                .first()
            )
            if cart:
                return cart

            try:
                with transaction.atomic():
                    return Cart.objects.create(
                        user=user,
                        session_id=None,
                        is_active=True,
                    )
            except IntegrityError:
                return Cart.objects.select_for_update().get(
                    user=user,
                    is_active=True,
                )

        if session_id:
            cart = (
                Cart.objects.select_for_update()
                .filter(session_id=session_id, is_active=True)
                .first()
            )
            if cart:
                return cart

            try:
                return Cart.objects.create(
                    session_id=session_id,
                    user=None,
                    is_active=True,
                )
            except IntegrityError:
                # Another request created it first
                return Cart.objects.get(
                    session_id=session_id,
                    is_active=True,
                )

        raise ValueError("Cart requires authenticated user or session_id")

    def get_variant(self, variant_id: str) -> ProductVariant:
        return get_object_or_404(
            ProductVariant.objects.select_related("product"),
            id=variant_id,
            is_active=True,
        )

    def get_mutable_cart(self, *, cart):
        locked_cart = Cart.objects.select_for_update().get(id=cart.id)
        if not locked_cart.is_active or locked_cart.is_locked:
            raise CartConflictError("Cart is no longer available for updates")
        return locked_cart

    @transaction.atomic
    def add_item(
        self, *, cart: Cart, variant: ProductVariant, quantity: int
    ) -> CartItem:
        cart = self.get_mutable_cart(cart=cart)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        item, created = CartItem.objects.select_for_update().get_or_create(
            cart=cart,
            product_variant=variant,
            defaults={
                "price": variant.price,
                "discount_price": variant.discount_price,
                "quantity": quantity,
            },
        )

        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        return item

    @transaction.atomic
    def update_item(self, *, cart: Cart, item_id: str, quantity: int) -> CartItem:
        cart = self.get_mutable_cart(cart=cart)
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")

        item = CartItem.objects.select_for_update().get(id=item_id, cart=cart)
        item.quantity = quantity
        item.save(update_fields=["quantity"])

        return item

    @transaction.atomic
    def remove_item(self, *, cart: Cart, item_id: str) -> None:
        cart = self.get_mutable_cart(cart=cart)

        CartItem.objects.select_for_update().get(id=item_id, cart=cart).delete()
