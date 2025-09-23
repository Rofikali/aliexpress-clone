# # apps.products.models.product_model.py
# from django.db import models
# import uuid
# from django.contrib.auth import get_user_model
# from apps.products.models.category_model import Category
# from apps.products.models.brand_model import Brand

# User = get_user_model()


# class Product(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, db_index=True)
#     slug = models.SlugField(max_length=255, unique=True, db_index=True)
#     description = models.TextField()
#     sku = models.CharField(max_length=100, unique=True, db_index=True)
#     price = models.DecimalField(max_digits=12, decimal_places=2)
#     discount_price = models.DecimalField(
#         max_digits=12, decimal_places=2, null=True, blank=True
#     )
#     currency = models.CharField(max_length=3, default="USD")
#     image = models.ImageField(upload_to="products/images/", null=True, blank=True)
#     stock = models.IntegerField()
#     is_active = models.BooleanField(default=True)
#     rating = models.FloatField(default=0.0)
#     review_count = models.IntegerField(default=0)
#     seller = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
#     brand = models.ForeignKey(
#         Brand, null=True, blank=True, on_delete=models.SET_NULL, db_index=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = "products_product"

#     def __str__(self):
#         return f"(Title : {self.title}),  (SKU: {self.sku})"


# apps.products.models.product_model.py

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.products.models.category import Category
from apps.products.models.brand import Brand

User = get_user_model()


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    description = models.TextField()
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    currency = models.CharField(max_length=3, default="USD")
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, db_index=True, related_name="category_products"
    )
    brand = models.ForeignKey(
        Brand,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_product"
        indexes = [
            models.Index(fields=["title"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["seller", "category"]),
        ]

    def __str__(self):
        return f"(Title: {self.title}), (SKU: {self.sku})"
