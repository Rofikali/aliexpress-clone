# # # # from rest_framework import serializers
# # # # from apps.products.models.product_variant_model import (
# # # #     ProductVariant,
# # # # )

# # # # from .product_attribute_serializer import ProductAttributeSerializer


# # # # class ProductVariantSerializer(serializers.ModelSerializer):
# # # #     attributes = ProductAttributeSerializer(many=True, read_only=True)

# # # #     class Meta:
# # # #         model = ProductVariant
# # # #         fields = ["id", "product", "sku", "price", "stock", "attributes"]


# # # # from rest_framework import serializers
# # # # from apps.products.models.product_variant_model import (
# # # #     ProductVariant,
# # # #     ProductVariantValue,
# # # # )
# # # # from apps.products.models.product_attribute_model import ProductAttributeValue


# # # # class ProductVariantValueSerializer(serializers.ModelSerializer):
# # # #     attribute_name = serializers.CharField(source="attribute.name", read_only=True)
# # # #     value_text = serializers.CharField(source="value.value", read_only=True)

# # # #     class Meta:
# # # #         model = ProductVariantValue
# # # #         fields = ["id", "attribute", "attribute_name", "value", "value_text"]


# # # # class ProductVariantSerializer(serializers.ModelSerializer):
# # # # attributes = ProductVariantValueSerializer(many=True, read_only=True)

# # # # class Meta:
# # # #     model = ProductVariant
# # # #     fields = [
# # # #         "id",
# # # #         "product",
# # # #         "sku",
# # # #         "price",
# # # #         "discount_price",
# # # #         "currency",
# # # #         "stock",
# # # #         "image",
# # # #         "is_active",
# # # #         "attributes",
# # # #     ]

# # # from rest_framework import serializers
# # # from apps.products.models.product_variant import ProductVariant


# # # class ProductVariantSerializer(serializers.ModelSerializer):
# # #     class Meta:
# # #         model = ProductVariant
# # #         fields = [
# # #             "id",
# # #             "product",
# # #             "sku",
# # #             "price",
# # #             "discount_price",
# # #             "stock",
# # #             "currency",
# # #             "image",
# # #             "is_active",
# # #             "created_at",
# # #             "updated_at",
# # #         ]


# # # apps/products/serializers/product_variants.py
# # from rest_framework import serializers


# # class VariantAttributeItemSerializer(serializers.Serializer):
# #     attribute_id = serializers.CharField()
# #     attribute_name = serializers.CharField()
# #     value_id = serializers.CharField()
# #     value = serializers.CharField()


# # class ProductVariantSerializer(serializers.Serializer):
# #     id = serializers.CharField()
# #     sku = serializers.CharField()
# #     price = serializers.DecimalField(max_digits=12, decimal_places=2)
# #     discount_price = serializers.DecimalField(
# #         max_digits=12, decimal_places=2, allow_null=True
# #     )
# #     currency = serializers.CharField()
# #     stock = serializers.IntegerField()
# #     is_active = serializers.BooleanField()
# #     image = serializers.CharField(allow_null=True)
# #     attributes = VariantAttributeItemSerializer(many=True)
# #     discount_percentage = serializers.SerializerMethodField()

# #     def get_discount_percentage(self, obj):
# #         try:
# #             p = float(obj.get("price") or 0)
# #             dp = obj.get("discount_price")
# #             if dp is None or p == 0:
# #                 return None
# #             dp = float(dp)
# #             return round(((p - dp) / p) * 100, 2)
# #         except Exception:
# #             return None

# from rest_framework import serializers
# from apps.products.models.product_variant import ProductVariantValue, ProductVariant

# class VariantAttributeItemSerializer(serializers.ModelSerializer):
#     attribute_id = serializers.UUIDField(source="attribute.id")
#     attribute_name = serializers.CharField(source="attribute.name")
#     value_id = serializers.UUIDField(source="value.id")
#     value = serializers.CharField(source="value.value")

#     class Meta:
#         model = ProductVariantValue
#         fields = [
#             "attribute_id",
#             "attribute_name",
#             "value_id",
#             "value",
#         ]


# class ProductVariantSerializer(serializers.ModelSerializer):
#     attributes = VariantAttributeItemSerializer(
#         many=True, read_only=True,
#         # source="attributes"
#     )
#     image = serializers.SerializerMethodField()
#     discount_percentage = serializers.SerializerMethodField()

#     class Meta:
#         model = ProductVariant
#         fields = [
#             "id",
#             "sku",
#             "price",
#             "discount_price",
#             "currency",
#             "stock",
#             "is_active",
#             "image",
#             "attributes",
#             "discount_percentage",
#         ]

#     def get_image(self, obj):
#         img = getattr(obj.image, "image", None)
#         return img.url if img else None

#     def get_discount_percentage(self, obj):
#         if not obj.discount_price:
#             return None
#         p = float(obj.price)
#         dp = float(obj.discount_price)
#         if p == 0:
#             return None
#         return round(((p - dp) / p) * 100, 2)


# apps/products/serializers/product_variants.py
from rest_framework import serializers
from apps.products.models.product_variant import ProductVariant, ProductVariantValue


class VariantAttributeItemSerializer(serializers.ModelSerializer):
    attribute_id = serializers.UUIDField(source="attribute.id", read_only=True)
    attribute_name = serializers.CharField(source="attribute.name", read_only=True)
    value_id = serializers.UUIDField(source="value.id", read_only=True)
    value = serializers.CharField(source="value.value", read_only=True)

    class Meta:
        model = ProductVariantValue
        fields = ["attribute_id", "attribute_name", "value_id", "value"]


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = VariantAttributeItemSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "sku",
            "price",
            "discount_price",
            "currency",
            "stock",
            "is_active",
            "image",
            "attributes",
            "discount_percentage",
        ]
        read_only_fields = ["id", "attributes", "discount_percentage", "image"]

    def get_image(self, obj):
        img = getattr(obj, "image", None)
        # if image FK points to ProductImages model with .image field:
        if img and hasattr(img, "image") and getattr(img, "image"):
            request = self.context.get("request")
            url = img.image.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_discount_percentage(self, obj):
        if not obj.discount_price:
            return None
        try:
            p = float(obj.price)
            dp = float(obj.discount_price)
            if p == 0:
                return None
            return round(((p - dp) / p) * 100, 2)
        except Exception:
            return None
