# import uuid
# from django.db import models
# from django.conf import settings

# # from apps.products.models import ProductVariant
# from apps.products.models.product_variant import ProductVariant

# User = settings.AUTH_USER_MODEL


# class Cart(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
#     session_id = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         unique=True,
#         help_text="Used for guest carts (anonymous users).",
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Cart({self.user.username})"

#     @property
#     def total_items(self):
#         return sum(item.quantity for item in self.items.all())

#     @property
#     def total_price(self):
#         return sum(item.subtotal for item in self.items.all())


# apps/carts/models/cart.py
import uuid
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="carts",
        null=True,
        blank=True,
    )

    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        db_index=True,
        help_text="Used for guest carts (anonymous users)",
    )
    # apps/carts/models/cart.py
    is_locked = models.BooleanField(default=False)


    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["session_id", "is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(user__isnull=False, is_active=True),
                name="carts_one_active_cart_per_user",
            )
        ]

    def __str__(self):
        owner = self.user_id or self.session_id
        return f"Cart({owner})"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
