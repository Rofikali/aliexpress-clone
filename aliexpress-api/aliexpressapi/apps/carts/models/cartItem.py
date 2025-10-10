import uuid
from django.db import models
from django.conf import settings
from apps.products.models.product_variant import ProductVariant
from apps.carts.models.cart import Cart

User = settings.AUTH_USER_MODEL


class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product_variant")

    def __str__(self):
        return f"{self.product_variant.product.title} (x{self.quantity})"

    @property
    def subtotal(self):
        return (self.discount_price or self.price) * self.quantity
