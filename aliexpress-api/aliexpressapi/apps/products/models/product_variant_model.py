from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models.product_model import Product
import uuid

User = get_user_model()


class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    VARIANT_TYPE_CHOICES = [
        ("size", "Size"),
        ("color", "Color"),
        ("material", "Material"),
        ("custom", "Custom"),
    ]
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants", db_index=True
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    variant_type = models.CharField(max_length=20, choices=VARIANT_TYPE_CHOICES)
    value = models.CharField(max_length=100)
    price_override = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    stock = models.IntegerField()
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_productvariant"

    def __str__(self):
        return f"{self.product}, {self.variant_type}"
