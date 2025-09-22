# from rest_framework import serializers
# from apps.products.models.product_variant_model import (
#     ProductVariant,
# )

# from .product_attribute_serializer import ProductAttributeSerializer


# class ProductVariantSerializer(serializers.ModelSerializer):
#     attributes = ProductAttributeSerializer(many=True, read_only=True)

#     class Meta:
#         model = ProductVariant
#         fields = ["id", "product", "sku", "price", "stock", "attributes"]


# from rest_framework import serializers
# from apps.products.models.product_variant_model import (
#     ProductVariant,
#     ProductVariantValue,
# )
# from apps.products.models.product_attribute_model import ProductAttributeValue


# class ProductVariantValueSerializer(serializers.ModelSerializer):
#     attribute_name = serializers.CharField(source="attribute.name", read_only=True)
#     value_text = serializers.CharField(source="value.value", read_only=True)

#     class Meta:
#         model = ProductVariantValue
#         fields = ["id", "attribute", "attribute_name", "value", "value_text"]


# class ProductVariantSerializer(serializers.ModelSerializer):
# attributes = ProductVariantValueSerializer(many=True, read_only=True)

# class Meta:
#     model = ProductVariant
#     fields = [
#         "id",
#         "product",
#         "sku",
#         "price",
#         "discount_price",
#         "currency",
#         "stock",
#         "image",
#         "is_active",
#         "attributes",
#     ]

from rest_framework import serializers
from apps.products.models.product_variant import ProductVariant


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "sku",
            "price",
            "discount_price",
            "stock",
            "currency",
            "image",
            "is_active",
            "created_at",
            "updated_at",
        ]
