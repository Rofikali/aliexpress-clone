# # from django.db import models
# # from django.conf import settings

# # # Create your models here.
# # class Cart(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
# #     created_at = models.DateTimeField(auto_now_add=True)
# #     updated_at = models.DateTimeField(auto_now=True)

# # class CartItem(models.Model):
# #     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
# #     product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
# #     quantity = models.PositiveIntegerField(default=1)
# #     added_at = models.DateTimeField(auto_now_add=True)

# # class Wishlist(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
# #     created_at = models.DateTimeField(auto_now_add=True)

# # class WishlistItem(models.Model):
# #     wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
# #     product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
# #     added_at = models.DateTimeField(auto_now_add=True)


# from django.db import models
# from django.conf import settings
# from django.core.validators import MinValueValidator
# from decimal import Decimal


# class Cart(models.Model):
#     STATUS_CHOICES = (
#         ("open", "Open"),
#         ("checked_out", "Checked Out"),
#         ("abandoned", "Abandoned"),
#     )

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts"
#     )
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     @property
#     def total_price(self):
#         return sum(item.subtotal for item in self.items.all())

#     def __str__(self):
#         return f"Cart({self.id}) - {self.user}"


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
#     unit_price = models.DecimalField(
#         max_digits=12, decimal_places=2, default=Decimal("0.00")
#     )
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("cart", "product")

#     @property
#     def subtotal(self):
#         return self.unit_price * self.quantity

#     def save(self, *args, **kwargs):
#         # snapshot product price at the moment of adding
#         if not self.unit_price:
#             self.unit_price = self.product.price
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.quantity} x {self.product}"


# class Wishlist(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlists"
#     )
#     name = models.CharField(max_length=100, default="My Wishlist")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Wishlist({self.id}) - {self.user}"


# class WishlistItem(models.Model):
#     wishlist = models.ForeignKey(
#         Wishlist, on_delete=models.CASCADE, related_name="items"
#     )
#     product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("wishlist", "product")

#     def __str__(self):
#         return f"{self.product} in {self.wishlist}"
