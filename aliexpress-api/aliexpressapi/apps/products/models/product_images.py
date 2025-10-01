# apps.products.models.product_images_model.py

from attr import attributes
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from apps.products.models.product import Product

User = get_user_model()


class ProductImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images", db_index=True
    )
    image = models.ImageField(max_length=500, upload_to="products/images/")
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_productimage"

    def __str__(self):
        return f"{self.product.title} - Image: {self.image.url}"
