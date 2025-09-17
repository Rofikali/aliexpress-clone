from django.db import models
import uuid
from django.contrib.auth import get_user_model
# from apps.products.models.product_model import Product
from apps.products.models.product_variant_model import ProductVariant

User = get_user_model()


class ProductAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # product = models.ForeignKey(
    #     Product, on_delete=models.CASCADE, related_name="attributes", db_index=True
    # )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes",
        db_index=True,
    )
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)
    name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=100, db_index=True)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "products_productattribute"
