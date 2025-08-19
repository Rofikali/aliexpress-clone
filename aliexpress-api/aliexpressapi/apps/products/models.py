from django.db import models
import uuid

# Create your models here.
# -- CreateTable
# CREATE TABLE "Products" (
#     "id" SERIAL NOT NULL,
#     "title" TEXT NOT NULL,
#     "description" TEXT NOT NULL,
#     "url" TEXT NOT NULL,
#     "price" INTEGER NOT NULL,
#     "created_at" TIMESTAMPTZ(6) DEFAULT CURRENT_TIMESTAMP,

#     CONSTRAINT "Products_pkey" PRIMARY KEY ("id")
# );

# class Products(models.Model):
#     title = models.TextField(max_length=255)
#     description = models.TextField(max_length=1000)
#     # url = models.TextField()
#     image = models.ImageField(upload_to='products/Images/')
#     price = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'Products'
#         verbose_name = 'Product'
#         verbose_name_plural = 'Products'

#     def __str__(self):
#         return self.title

# class ProductImages(models.Model):
#     product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_images')
#     img_name = models.ImageField()
#     creted_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        db_index=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_category"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    logo = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_brand"

    def __str__(self):
        return self.name


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
    stock = models.IntegerField()
    is_active = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    review_count = models.IntegerField(default=0)
    seller = models.ForeignKey("accounts.User", on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)
    brand = models.ForeignKey(
        Brand, null=True, blank=True, on_delete=models.SET_NULL, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_product"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", db_index=True
    )
    image = models.ImageField(max_length=500, upload_to="products/images/")
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products_productimage"


class ProductVariant(models.Model):
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


class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes", db_index=True
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="attributes",
        db_index=True,
    )
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.CharField(max_length=100, db_index=True)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "products_productattribute"


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
    reference_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "products_inventory"
