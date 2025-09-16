from django.db import models
import uuid
from django.contrib.auth import get_user_model
from apps.products.models.product_model import Product

User = get_user_model()


class Inventory(models.Model):
    REASON_CHOICES = [
        ("order", "Order"),
        ("restock", "Restock"),
        ("return", "Return"),
        ("adjustment", "Adjustment"),
    ]
    stock = models.IntegerField()
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    change = models.IntegerField()
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    quantity = models.IntegerField()
    location = models.CharField(max_length=255, blank=True)
    reference_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products_inventory"
