# from django.db import models
# import uuid
# from django.contrib.auth import get_user_model
# # from apps.products.models.product_model import Product
# from apps.products.models.product_variant_model import ProductVariant

# User = get_user_model()


# class ProductAttribute(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     variant = models.ForeignKey(
#         ProductVariant,
#         on_delete=models.CASCADE,
#         related_name="attributes",
#         db_index=True,
#     )
#     attribute_name = models.CharField(max_length=100)
#     attribute_value = models.CharField(max_length=255)
#     name = models.CharField(max_length=100, db_index=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     key = models.CharField(max_length=100, db_index=True)
#     value = models.CharField(max_length=255)

#     class Meta:
#         db_table = "products_productattribute"


class ProductAttribute(models.Model):
    """Defines an attribute type (e.g. Color, Size, Material)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)  # e.g. "Color"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_productattribute"

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """Defines possible values for a given attribute (e.g. Red, Blue, XL)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attribute = models.ForeignKey(
        ProductAttribute,
        on_delete=models.CASCADE,
        related_name="values",
        db_index=True,
    )
    value = models.CharField(max_length=100, db_index=True)  # e.g. "Red"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_productattributevalue"
        unique_together = ("attribute", "value")

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductVariantAttribute(models.Model):
    """Assigns a specific attribute value to a product variant (e.g. Variant X → Color=Red)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="variant_attributes",
        db_index=True,
    )
    attribute_value = models.ForeignKey(
        ProductAttributeValue,
        on_delete=models.CASCADE,
        related_name="variant_assignments",
        db_index=True,
    )

    class Meta:
        db_table = "products_productvariantattribute"
        unique_together = ("variant", "attribute_value")

    def __str__(self):
        return f"{self.variant.sku} → {self.attribute_value}"
