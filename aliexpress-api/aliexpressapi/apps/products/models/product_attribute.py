# # # apps.products.models.product_attribute_model.py

# # from django.db import models
# # import uuid
# # from django.contrib.auth import get_user_model

# # User = get_user_model()


# # class ProductAttribute(models.Model):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     name = models.CharField(max_length=100, unique=True, db_index=True)
# #     sort_order = models.PositiveIntegerField(default=0)

# #     class Meta:
# #         # db_table = "products_productattribute"
# #         ordering = ["sort_order", "name"]

# #     def __str__(self):
# #         return f"Product Attribute Model: {self.name}"


# # class ProductAttributeValue(models.Model):
# #     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# #     attribute = models.ForeignKey(
# #         ProductAttribute, on_delete=models.CASCADE, related_name="values", db_index=True
# #     )
# #     value = models.CharField(max_length=100, db_index=True)

# #     class Meta:
# #         # db_table = "products_productattributevalue"
# #         unique_together = ("attribute", "value")
# #         ordering = ["attribute__sort_order", "value"]

# #     def __str__(self):
# #         return f"Product Attribute Value Model: {self.value}"


# import uuid
# from django.db import models


# class ProductAttribute(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=100, unique=True, db_index=True)
#     sort_order = models.PositiveIntegerField(default=0)

#     class Meta:
#         ordering = ["sort_order", "name"]
#         indexes = [
#             models.Index(fields=["name"]),
#         ]

#     def __str__(self):
#         return f"Product Attribute: {self.name}"


# class ProductAttributeValue(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     attribute = models.ForeignKey(
#         ProductAttribute, on_delete=models.CASCADE, related_name="values", db_index=True
#     )
#     value = models.CharField(max_length=100, db_index=True)

#     class Meta:
#         unique_together = ("attribute", "value")
#         ordering = ["attribute__sort_order", "value"]
#         indexes = [
#             models.Index(fields=["value"]),
#         ]

#     def __str__(self):
#         return f"{self.attribute.name} = {self.value}"

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
    creaeted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("attribute", "value")
        ordering = ["attribute__sort_order", "value"]
        indexes = [models.Index(fields=["value"])]

    def __str__(self):
        return f"{self.attribute.name} = {self.value}"
