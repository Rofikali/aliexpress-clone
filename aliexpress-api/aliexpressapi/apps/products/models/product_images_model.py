from django.db import models
import uuid
from django.contrib.auth import get_user_model
from apps.products.models.product_model import Product

User = get_user_model()


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images", db_index=True
    )
    image = models.ImageField(max_length=500, upload_to="products/images/")
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products_productimage"
