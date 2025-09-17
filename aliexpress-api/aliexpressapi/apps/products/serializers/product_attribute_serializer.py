from rest_framework import serializers
from apps.products.models.product_attribute_model import (
    ProductAttribute,
)


# class ProductAttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductAttribute
#         fields = ["id", "name", "value"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = [
            "id",
            # "product",
            "variant",
            "attribute_name",
            "attribute_value",
            "name",
            "key",
            "value",
            "created_at",
            "updated_at",
        ]
