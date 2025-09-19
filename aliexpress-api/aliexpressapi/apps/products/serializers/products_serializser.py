# from rest_framework import serializers
# from django.conf import settings
# from apps.products.models.product_model import (
#     Product,
# )

# from .product_image_serializer import ProductImageSerializer
# from .product_variants_serializer import ProductVariantSerializer
# from .category_serializer import CategorySerializer
# from .brand_serializer import BrandSerializer


# class ProductSerializer(serializers.ModelSerializer):
#     # id = serializers.UUIDField(format="hex", read_only=True)  # ✅ Add this
#     # images = ProductImageSerializer(many=True, source="product_images", read_only=True)
#     # variants = ProductVariantSerializer(
#     #     many=True, source="productvariant_set", read_only=True
#     # )
#     category = CategorySerializer(read_only=True)
#     brand = BrandSerializer(read_only=True)
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "title",
#             "description",
#             "price",
#             "image",
#             # "images",
#             "category",
#             "brand",
#             # "variants",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["created_at", "updated_at"]
#         extra_kwargs = {
#             "image": {"required": True, "allow_null": True},
#             "description": {"required": True, "allow_blank": True},
#         }
#         depth = 3

#     def get_image(self, obj):
#         """
#         Returns the absolute image URL if available, otherwise None.
#         """
#         if not obj.image:
#             return None

#         try:
#             request = self.context.get("request")
#             image = obj.image.url
#             # image_url = obj.image.url

#             if request:
#                 return request.build_absolute_uri(image)
#             return f"{settings.MEDIA_URL}{image.lstrip('/')}"
#         except Exception:
#             # Optional: log the error if you have logging set up
#             # logger.warning(f"Image URL error for product {obj.pk}: {e}")
#             return None


# class ProductDetailSerializer(serializers.ModelSerializer):
#     images = ProductImageSerializer(many=True, source="product_images", read_only=True)
#     variants = ProductVariantSerializer(
#         many=True, source="productvariant_set", read_only=True
#     )
#     category = CategorySerializer(read_only=True)
#     brand = BrandSerializer(read_only=True)
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             "id",
#             "title",
#             "slug",
#             "description",
#             "sku",
#             "price",
#             "discount_price",
#             "currency",
#             "stock",
#             "is_active",
#             "rating",
#             "review_count",
#             "image",
#             "images",
#             "category",
#             "brand",
#             "variants",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = ["created_at", "updated_at"]
#         extra_kwargs = {
#             "image": {"required": True, "allow_null": True},
#             "description": {"required": True, "allow_blank": True},
#         }
#         depth = 3

#     def get_image(self, obj):
#         """
#         Returns the absolute image URL if available, otherwise None.
#         """
#         if not obj.image:
#             return None

#         try:
#             request = self.context.get("request")
#             image = obj.image.url
#             # image_url = obj.image.url

#             if request:
#                 return request.build_absolute_uri(image)
#             return f"{settings.MEDIA_URL}{image.lstrip('/')}"
#         except Exception:
#             # Optional: log the error if you have logging set up
#             # logger.warning(f"Image URL error for product {obj.pk}: {e}")
#             return None

# apps.products/serializers/products_serializser.py
from rest_framework import serializers
from apps.products.models.product_model import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "discount_price",
            "currency",
            "image",
            "stock",
            "is_active",
            "rating",
            "review_count",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
