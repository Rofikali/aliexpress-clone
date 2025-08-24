from rest_framework import serializers
from django.conf import settings
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    ProductVariant,
    ProductAttribute,
    Inventory,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "description"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image"]


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "value"]


class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "product", "sku", "price", "stock", "attributes"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "product", "quantity", "location"]


class ProductSerializer(serializers.ModelSerializer):
    # id = serializers.UUIDField(format="hex", read_only=True)  # ✅ Add this
    images = ProductImageSerializer(many=True, source="product_images", read_only=True)
    variants = ProductVariantSerializer(
        many=True, source="productvariant_set", read_only=True
    )
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "image",
            "images",
            "category",
            "brand",
            "variants",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
        extra_kwargs = {
            "image": {"required": True, "allow_null": True},
            "description": {"required": True, "allow_blank": True},
        }
        depth = 3

    def get_image(self, obj):
        """
        Returns the absolute image URL if available, otherwise None.
        """
        if not obj.image:
            return None

        try:
            request = self.context.get("request")
            image = obj.image.url
            # image_url = obj.image.url

            if request:
                return request.build_absolute_uri(image)
            return f"{settings.MEDIA_URL}{image.lstrip('/')}"
        except Exception:
            # Optional: log the error if you have logging set up
            # logger.warning(f"Image URL error for product {obj.pk}: {e}")
            return None
