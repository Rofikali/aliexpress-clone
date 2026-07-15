from apps.carts.context.unit_of_work import UnitOfWork
from apps.checkout.errors import EmptyCartError
from apps.checkout.repositories.checkout_repository import CheckoutRepository


class CheckoutService:
    def __init__(self, repo: CheckoutRepository):
        self.repo = repo

    def checkout(self, *, user, idempotency_key):
        existing_order = self.repo.get_order_by_idempotency_key(
            user=user,
            idempotency_key=idempotency_key,
        )
        if existing_order:
            return existing_order, False

        with UnitOfWork():
            cart = self.repo.get_active_cart_for_user(user=user)
            if cart is None:
                raise EmptyCartError("No active cart is available for checkout")

            existing_order = self.repo.get_order_by_idempotency_key(
                user=user,
                idempotency_key=idempotency_key,
            )
            if existing_order:
                return existing_order, False

            cart_items = self.repo.get_locked_cart_items(cart=cart)
            if not cart_items:
                raise EmptyCartError("Cart is empty")

            variants = self.repo.get_locked_variants(cart_items=cart_items)
            self.repo.assert_variants_are_checkoutable(
                cart_items=cart_items,
                variants=variants,
            )
            self.repo.reserve_inventory(cart_items=cart_items, variants=variants)

            order, created = self.repo.create_order(
                user=user,
                idempotency_key=idempotency_key,
                cart_items=cart_items,
                variants=variants,
            )

            if created:
                self.repo.deactivate_cart(cart)

        return order, created
