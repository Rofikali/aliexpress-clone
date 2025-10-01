# apps.products.models.product_attribute_model.py
import uuid
from django.db import models


class ProductAttribute(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sort_order", "name"]
        indexes = [models.Index(fields=["name"])]

    def __str__(self):
        return f"Product Attribute: {self.name}"


class ProductAttributeValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name="values", db_index=True
    )
    value = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("attribute", "value")
        ordering = ["attribute__sort_order", "value"]
        indexes = [models.Index(fields=["value"])]

    def __str__(self):
        return f"{self.attribute.name} = {self.value}"
