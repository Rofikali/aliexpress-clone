# # from rest_framework import serializers
# # from apps.products.models.product_variant_model import (
# #     ProductVariant,
# # )

# # from .product_attribute_serializer import ProductAttributeSerializer


# # class ProductVariantSerializer(serializers.ModelSerializer):
# #     attributes = ProductAttributeSerializer(many=True, read_only=True)

# #     class Meta:
# #         model = ProductVariant
# #         fields = ["id", "product", "sku", "price", "stock", "attributes"]


# # from rest_framework import serializers
# # from apps.products.models.product_variant_model import (
# #     ProductVariant,
# #     ProductVariantValue,
# # )
# # from apps.products.models.product_attribute_model import ProductAttributeValue


# # class ProductVariantValueSerializer(serializers.ModelSerializer):
# #     attribute_name = serializers.CharField(source="attribute.name", read_only=True)
# #     value_text = serializers.CharField(source="value.value", read_only=True)

# #     class Meta:
# #         model = ProductVariantValue
# #         fields = ["id", "attribute", "attribute_name", "value", "value_text"]


# # class ProductVariantSerializer(serializers.ModelSerializer):
# # attributes = ProductVariantValueSerializer(many=True, read_only=True)

# # class Meta:
# #     model = ProductVariant
# #     fields = [
# #         "id",
# #         "product",
# #         "sku",
# #         "price",
# #         "discount_price",
# #         "currency",
# #         "stock",
# #         "image",
# #         "is_active",
# #         "attributes",
# #     ]

# from rest_framework import serializers
# from apps.products.models.product_variant import ProductVariant, ProductVariantValue


# class ProductVariantValueSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVariantValue
#         fields = [
#             "id",
#             "variant",
#             "attribute",
#             "value",
#             "created_at",
#             "updated_at",
#         ]


# class ProductVariantSerializer(serializers.ModelSerializer):
#     varints = ProductVariantValueSerializer(many=True, read_only=True)
#     # varints_attributes = serializers.SerializerMethodField()

#     class Meta:
#         model = ProductVariant
#         fields = [
#             "id",
#             "product",
#             "sku",
#             "price",
#             "discount_price",
#             "stock",
#             "varints",
#             "currency",
#             "image",
#             "is_active",
#             "created_at",
#             "updated_at",
#         ]


# apps/products/serializers/product_variants.py
from rest_framework import serializers
from django.conf import settings
from apps.products.models.product_variant import ProductVariant, ProductVariantValue


class ProductVariantValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source="attribute.name", read_only=True)

    class Meta:
        model = ProductVariantValue
        fields = [
            "id",
            "attribute",  # FK id (optional for frontend)
            "attribute_name",  # human readable name
            "value",
        ]


class ProductVariantSerializer(serializers.ModelSerializer):
    """
    Frontend-friendly variant serializer.
    - `attributes` gives [{id, name, value}] derived from related variant values.
    - `image` returns absolute URL if available.
    """

    attributes = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "sku",
            "price",
            "discount_price",
            "discount_percentage",
            "currency",
            "stock",
            "is_active",
            "image",
            "attributes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_attributes(self, obj):
        """
        Attempt to read prefetched related values in a few forms to be robust:
        - obj.varints (your current related_name)
        - obj.values (if you used `related_name="values"`)
        - fallback to reverse FK: productvariantvalue_set.all()
        Returns list of {id, name, value}
        """
        vals = getattr(obj, "varints", None)
        if vals is None:
            vals = getattr(obj, "values", None)
        if vals is None:
            # fallback
            vals = obj.productvariantvalue_set.all()

        result = []
        for v in vals:
            name = (
                getattr(v.attribute, "name", None)
                if getattr(v, "attribute", None)
                else None
            )
            result.append({"id": v.id, "name": name, "value": v.value})
        return result

    def get_image(self, obj):
        # if variant.image is an ImageField or string path
        try:
            img = getattr(obj, "image", None)
            if not img:
                return None
            request = self.context.get("request")
            url = img.url if hasattr(img, "url") else str(img)
            return request.build_absolute_uri(url) if request else url
        except Exception:
            return None

    def get_discount_percentage(self, obj):
        try:
            if obj.discount_price and obj.price and obj.price > 0:
                return round(((obj.price - obj.discount_price) / obj.price) * 100, 2)
        except Exception:
            pass
        return None
