# apps.products.models.product_variant_model.py
import uuid
from django.db import models
from apps.products.models.product import Product
from apps.products.models.product_images import ProductImages
from apps.products.models.product_attribute import (
    ProductAttribute,
    ProductAttributeValue,
)


class ProductVariant(models.Model):
    """SKU-level item customers purchase."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    stock = models.PositiveIntegerField(default=0, db_index=True)
    currency = models.CharField(max_length=3, default="USD")
    image = models.ForeignKey(
        ProductImages, null=True, blank=True, on_delete=models.SET_NULL
    )
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_productvariant"
        unique_together = ("product", "sku")
        indexes = [
            models.Index(fields=["product", "price"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.product.title} ({self.sku})"


class ProductVariantValue(models.Model):
    """Link variant to attribute/value (e.g., Color=Red)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="attributes"
    )
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("variant", "attribute")
        indexes = [
            models.Index(fields=["variant", "attribute"]),
        ]

    def __str__(self):
        return f"{self.id} - {self.attribute.name}: {self.value.value}"
